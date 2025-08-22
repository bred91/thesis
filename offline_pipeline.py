import concurrent.futures
import copy
import datetime
import logging
import os
import subprocess

import ollama
import torch
from langchain_core.documents import Document
from tqdm import tqdm

from summary_categorization.categorization import categorize
from summary_categorization.general_summarization import generate_general_summary
from summary_categorization.technical_summarization import generate_technical_summary
from utils.chromadb_utils import save_commit_to_chromadb, delete_all_documents, save_general_document_to_chromadb
from utils.commit_utils import filter_trivial_commits, normalize_commit_data
from utils.config import SQL_PERSIST_DIR, MUJS_REMOTE_URL, MUJS_LOCAL_PATH, OLLAMA_CLIENT_HOST, SEED, \
    OFFLINE_MODEL_NAME, OFFLINE_PIPELINE_TEST_NAME
from utils.enums import SummaryType
from utils.file_utils import load_commits, save_commits, full_path
from utils.git_utils import extract_git_commits, extract_mujs_docs
from utils.logging_handler import SQLiteHandler
from utils.semantic_code_utils import build_mujs_code_index
from utils.sqlite_utils import save_commits_to_sqlite, save_summaries_to_sqlite, delete_all_summaries

torch.manual_seed(SEED)

current_directory = os.getcwd()

logger = logging.getLogger("DBLogger")
logger.setLevel(logging.DEBUG)

db_handler = SQLiteHandler(SQL_PERSIST_DIR)

formatter = logging.Formatter('%(message)s')
db_handler.setFormatter(formatter)

logger.addHandler(db_handler)

def main():
    remote_path = MUJS_REMOTE_URL
    local_path = MUJS_LOCAL_PATH
    ollama_client = ollama.Client(host=OLLAMA_CLIENT_HOST)
    llama_model = OFFLINE_MODEL_NAME

    # Avoid warning related to parallelization
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    if not os.path.isdir(local_path):
      subprocess.run(["git", "clone", remote_path, local_path], check=True) #!git clone {remote_path}

    data_filepath_raw_data = 'commits_raw.pkl'          # raw data file with all commits
    data_filepath_few_shots = 'commits_few_shots.pkl'   # few-shots data file
    commits_folder = 'commits'

    # To resume experiments
    commits = load_commits(commits_folder + '/' + data_filepath_raw_data)
    commits_few_shots = load_commits(data_filepath_few_shots)

    if commits is None: # If there are no checkpoints, initialize commits extraction
        commits = extract_git_commits(local_path)     # Extract commits from repository
        commits = filter_trivial_commits(commits)     # Filter trivial commits
        commits = normalize_commit_data(commits)      # Normalize commits
        commits = {i: value for i, value in enumerate(commits.values())} # Adjust idxs

        save_commits(commits, full_path(current_directory + '/' + commits_folder, "raw"))
        save_commits_to_sqlite(commits)

    if commits_few_shots is None:
        commits_few_shots = copy.deepcopy(commits)

    delete_all_summaries()
    delete_all_documents()

    # process general documents
    general_docs: list[dict]  = extract_mujs_docs()
    for i, doc in enumerate(general_docs):
        save_general_document_to_chromadb({i: doc})

    # process code documents
    build_mujs_code_index()

    # process commits
    for i, (idx, commit) in tqdm(enumerate(commits_few_shots.items())):
        idx_plus_one = idx + 1
        # Initialize fields if not present
        summary_retrieved_docs: list[tuple[Document, float]] = []
        tech_summary_retrieved_docs: list[tuple[Document, float]] = []

        # Run summarization and classification only on unprocessed commits
        # Categorization
        if not commit['llama_category']:
            categorize(commit, idx_plus_one, llama_model, ollama_client)

        # General summary
        if not commit['llama_summary']:
            summary_retrieved_docs = generate_general_summary(commit, idx_plus_one, llama_model, ollama_client)

        # Technical summary
        if not commit['llama_tech_summary']:
            tech_summary_retrieved_docs = generate_technical_summary(commit, idx_plus_one, llama_model, ollama_client)

        # save summaries and categories
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(save_commits, commits_few_shots,
                                full_path(current_directory + '/' + commits_folder, "few_shots")),
                executor.submit(save_summaries_to_sqlite, idx_plus_one, OFFLINE_PIPELINE_TEST_NAME, datetime.datetime.now(),
                                commit['llama_category'],
                                commit['llama_summary'], summary_retrieved_docs,
                                commit['llama_tech_summary'], tech_summary_retrieved_docs),
                executor.submit(save_commit_to_chromadb, commit, idx_plus_one, SummaryType.GENERAL),
                executor.submit(save_commit_to_chromadb, commit, idx_plus_one, SummaryType.TECHNICAL)
            ]
            concurrent.futures.wait(futures)

    logger.debug("All commits processed and saved successfully.")


if __name__ == "__main__":
    main()
