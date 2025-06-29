from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

chroma = Chroma(
    collection_name="commits",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="./chromadb_v1",
    collection_metadata={"hnsw:space": "cosine"},
)

retriever = chroma.as_retriever(search_type="similarity", search_k=3)

llm = ChatOllama(
    model="llama3.1:8b-instruct-q8_0",
    temperature=0.0,
    num_ctx=32768,      # fixed context size
)

retrieval_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)