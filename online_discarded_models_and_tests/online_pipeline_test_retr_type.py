from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

chroma = Chroma(
    collection_name="commits",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    collection_metadata={"hnsw:space": "cosine"},
    persist_directory="./chromadb_v1",
)

retriever = chroma.as_retriever()

llm = OllamaLLM(model="llama3.1:8b-instruct-q8_0")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True
)

query = "Whenwas introduced with regex?"
result = qa_chain.invoke({"query": query})

print("stuff chain")
print(f"Answer: {result['result']}, \nN Documents: {len(result['source_documents'])} \nSource Documents: {result['source_documents']}")

qa_chain_map_reduce = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="map_reduce",
    return_source_documents=True
)
result_map_reduce = qa_chain_map_reduce.invoke({"query": query})

print("\n************map_reduce chain")
print(f"Answer: {result_map_reduce['result']}, \nN Documents: {len(result_map_reduce['source_documents'])} \nSource Documents: {result_map_reduce['source_documents']}")

qa_chain_refine = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="refine",
    return_source_documents=True
)
result_refine = qa_chain_refine.invoke({"query": query})

print("\n************refine chain")
print(f"Answer: {result_refine['result']}, \nN Documents: {len(result_refine['source_documents'])} \nSource Documents: {result_refine['source_documents']}")

qa_chain_map_rerank = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="map_rerank",
    return_source_documents=True
)
result_map_rerank = qa_chain_map_rerank.invoke({"query": query})

print("\n************map_rerank chain")
print(f"Answer: {result_map_rerank['result']}, \nN Documents: {len(result_map_rerank['source_documents'])} \nSource Documents: {result_map_rerank['source_documents']}")


