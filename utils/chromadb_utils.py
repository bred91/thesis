import datetime

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from utils.config import EMBEDDING_MODEL, CHROMA_PERSIST_DIR, COMMITS_COLLECTION_NAME, CHROMA_METADATA, \
    GENERAL_DOCS_COLLECTION_NAME
from utils.enums import SummaryType

chroma_commits = Chroma(
    collection_name=COMMITS_COLLECTION_NAME,
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
)

chroma_general_docs = Chroma(
    collection_name=GENERAL_DOCS_COLLECTION_NAME,
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
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

    chroma_commits.add_documents([Document(page_content=doc_text, metadata=metadata)], ids=[str(idx)])


def retrieve_top_commits_by_summary_type(query_text, summary_type:SummaryType, n_results=3) -> list[tuple[Document, float]]:
    results = chroma_commits.similarity_search_with_relevance_scores(
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
    chroma_commits.reset_collection()
    chroma_general_docs.reset_collection()


def save_general_document_to_chromadb(docs: dict) -> None:
    """
    Save a general document to the ChromaDB collection.
    """
    documents = [
        Document(
            page_content=doc['content'],
            metadata={
                "filename": doc['filename'],
                "insert_date": doc['insert_date']
            }
        ) for doc in docs.values()
    ]
    chroma_general_docs.add_documents(documents)


def retrieve_general_docs(query_text: str, n_results=5) -> list[Document]:
    """
    Retrieve general documents from the ChromaDB collection based on a query.

    Args:
        query_text (str): The query text to search for.
        n_results (int): The number of results to return.

    Returns:
        list[Document]: A list of retrieved documents.
    """
    return chroma_general_docs.similarity_search(
        query=query_text,
        k=n_results
    )