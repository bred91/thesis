import datetime

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from utils.enums import SummaryType

chroma = Chroma(
    collection_name="commits",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    collection_metadata={"hnsw:space": "cosine"},
    persist_directory="./chromadb_v1",
)

def save_commit_to_chromadb(commit, idx, summary_type: SummaryType):
    # Use commit message and summary as the document text
    doc_text: str
    if summary_type == SummaryType.GENERAL:
        doc_text = f"{commit.get('llama_summary', '')}"
    else:
        doc_text = f"{commit.get('llama_tech_summary', '')}"

    metadata = {
        "commit_hash": commit.get("hash", ""),
        "index": idx,
        "author": commit.get("author", ""),
        "date": commit.get("date", "").strftime('%Y-%m-%d %H:%M:%S') if isinstance(commit.get("date"), datetime.datetime)
                            else commit.get("date", ""),
        "message": commit.get("message", ""),
        "type": summary_type.value,
    }

    chroma.add_documents([Document(page_content=doc_text, metadata=metadata)], ids=[str(idx)])


def retrieve_top_commits_by_summary_type(query_text, summary_type:SummaryType, n_results=3) -> list[tuple[Document, float]]:
    results = chroma.similarity_search_with_relevance_scores(
        query=query_text,
        k=n_results,
        score_threshold=0.7,
        filter={
            "type": summary_type.value
        }
    )

    return results

def format_retrieved_docs(retrieved_docs):
    return ''.join(
        f"\nScore: {score}\nContent: {doc.page_content}" for doc, score in retrieved_docs
    )

def delete_all_documents():
    """
    Delete all documents from the ChromaDB collection.
    """
    chroma.reset_collection()