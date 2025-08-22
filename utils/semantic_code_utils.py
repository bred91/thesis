import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders.git import GitLoader
from langchain_ollama import OllamaEmbeddings

from utils.config import CHROMA_PERSIST_DIR, CHROMA_METADATA, MUJS_ABSOLUTE_PATH, MUJS_BRANCH, \
    SEMANTIC_CODE_COLLECTION, EMBEDDING_MODEL

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)


def build_mujs_code_index():
    loader = GitLoader(
        repo_path=MUJS_ABSOLUTE_PATH,
        clone_url=None,
        branch=MUJS_BRANCH,
        file_filter=lambda fp: fp.endswith((".c", ".h", ".md")) or fp == "Makefile",
    )
    docs = loader.load()

    for d in docs:
        src = d.metadata.get("source") or d.metadata.get("file_path") or ""
        full_name = os.path.basename(src)
        stem = Path(full_name).stem.lower()
        ext = Path(full_name).suffix.lower()
        # update metadata
        d.metadata.update({
            "path": src,                # original path if available
            "file_name": full_name,     # e.g., "opnames.h"
            "stem": stem,               # e.g., "opnames"
            "ext": ext,                 # e.g., ".h"
        })
        d.page_content = f"FILE NAME: {src}\n---\nCONTENT:{d.page_content}"

    # store docs in chroma
    store = Chroma(
        collection_name=SEMANTIC_CODE_COLLECTION,
        embedding_function=embeddings,
        collection_metadata=CHROMA_METADATA,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    store.reset_collection()
    store.add_documents(docs)
    return store

#todo: remove
def main():
    build_mujs_code_index()


if __name__ == "__main__":
    main()
