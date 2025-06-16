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
from utils.chromadb_utils import save_commit_to_chromadb, delete_all_documents
from utils.commit_utils import filter_trivial_commits, normalize_commit_data
from utils.enums import SummaryType
from utils.file_utils import load_commits, save_commits, full_path
from utils.git_utils import extract_git_commits
from utils.logging_handler import SQLiteHandler
from utils.plot_utils import plot_categories, plot_categories_pie_chart
from utils.sqlite_utils import save_commits_to_sqlite, save_summaries_to_sqlite, delete_all_summaries
from utils.validation_utils import calculate_precision_recall_categorization, ground_truth_array

torch.manual_seed(42)

current_directory = os.getcwd()

logger = logging.getLogger("DBLogger")
logger.setLevel(logging.DEBUG)

db_handler = SQLiteHandler("db_sqllite/sqlite.db")

formatter = logging.Formatter('%(message)s')
db_handler.setFormatter(formatter)

logger.addHandler(db_handler)

def main():
    remote_path = 'https://github.com/ccxvii/mujs.git'
    local_path = './mujs'
    #pipe_llama = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct", pad_token_id=128001, device = device_used )
    ollama_client = ollama.Client(host='http://localhost:11434')
    llama_model = 'llama3.1:8b-instruct-q8_0'

    # Avoid warning related to parallelization
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    if not os.path.isdir(local_path):
      subprocess.run(["git", "clone", remote_path, local_path], check=True) #!git clone {remote_path}

    data_filepath_raw_data = 'commits_raw.pkl'##### Open the right file   #### DELETE AT MOST USING ONLY RAW DATA
    data_filepath_few_shots = 'commits_few_shots.pkl'##### Open the right file   #### DELETE AT MOST USING ONLY RAW DATA
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

    for i, (idx, commit) in tqdm(enumerate(commits_few_shots.items())):

        # Initialize fields if not present
        summary_retrieved_docs: list[tuple[Document, float]] = []
        tech_summary_retrieved_docs: list[tuple[Document, float]] = []

        # Run summarization and classification only on unprocessed commits
        # Categorization
        if not commit['llama_category']:
            categorize(commit, idx, llama_model, ollama_client)

        # General summary
        if not commit['llama_summary'] and i < 100: # todo: remove this condition for the final version
            summary_retrieved_docs = generate_general_summary(commit, idx, llama_model, ollama_client)

        # Technical summary
        if not commit['llama_tech_summary'] and i < 100: # todo: remove this condition for the final version
            tech_summary_retrieved_docs = generate_technical_summary(commit, idx, llama_model, ollama_client)
            pass

        # save summaries and categories
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(save_commits, commits_few_shots,
                                full_path(current_directory + '/' + commits_folder, "few_shots")),
                executor.submit(save_summaries_to_sqlite, idx, "test1", datetime.datetime.now(),
                                commit['llama_category'],
                                commit['llama_summary'], summary_retrieved_docs,
                                commit['llama_tech_summary'], tech_summary_retrieved_docs),
                executor.submit(save_commit_to_chromadb, commit, idx, SummaryType.GENERAL),
                executor.submit(save_commit_to_chromadb, commit, idx, SummaryType.TECHNICAL)
            ]
            concurrent.futures.wait(futures)
        # save_commits(commits_few_shots, full_path(current_directory  + '/' + commits_folder, "few_shots"))
        # save_summaries_to_sqlite(idx, "test1", datetime.datetime.now(), commit['llama_category'],
        #                          commit['llama_summary'], summary_retrieved_docs,
        #                          commit['tech_summary'],
        #                          tech_summary_retrieved_docs)
        # save_commit_to_chromadb(commit, idx, SummaryType.GENERAL)
        # save_commit_to_chromadb(commit, idx, SummaryType.TECHNICAL)

    plot_categories(commits_few_shots, "few_shots")
    plot_categories_pie_chart(commits_few_shots, "few_shots")

    p, r, a = calculate_precision_recall_categorization(commits_few_shots, ground_truth_array)
    print("Few-shots categorization performance")
    print(f"Precision: {p}")
    print(f"Recall: {r}")
    print(f"Accuracy: {a}")
    pass




if __name__ == "__main__":
    main()
