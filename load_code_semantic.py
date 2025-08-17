from langchain_chroma import Chroma
from langchain_community.document_loaders.git import GitLoader
from langchain_ollama import OllamaEmbeddings

from utils.config import CHROMA_PERSIST_DIR, CHROMA_METADATA, EMBEDDING_MODEL, MUJS_LOCAL_PATH, MUJS_BRANCH, \
    SEMANTIC_CODE_COLLECTION

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)


def build_mujs_code_index():
    loader = GitLoader(
        repo_path=MUJS_LOCAL_PATH,
        clone_url=None,
        branch=MUJS_BRANCH,
        file_filter=lambda fp: fp.endswith((".c", ".h", "*.md")) or fp == "Makefile",
    )
    docs = loader.load()

    store = Chroma(
        collection_name=SEMANTIC_CODE_COLLECTION,
        embedding_function=embeddings,
        collection_metadata=CHROMA_METADATA,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    store.reset_collection()
    store.add_documents(docs)
    return store

def main():
    build_mujs_code_index()

if __name__ == "__main__":
    main()
