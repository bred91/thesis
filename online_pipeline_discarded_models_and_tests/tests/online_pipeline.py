from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.vectorstores.base import VectorStoreRetriever

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

query = "When was introduced regex?"
result = qa_chain.invoke({"query": query})

print(f"Answer: {result['result']}, \nN Documents: {len(result['source_documents'])} \nSource Documents: {result['source_documents']}")

# v2
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Custom prompt: includes metadata in the context
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are given the following documents with metadata:\n"
        "{context}\n"
        "Answer the following question using the information above:\n"
        "{question}"
    )
)

# Patch the retriever to include metadata in the document content
class MetadataRetriever(VectorStoreRetriever):
    def _get_relevant_documents(self, query_str, *, run_manager=None, **kwargs):
        docs = super()._get_relevant_documents(query_str, run_manager=run_manager, **kwargs)
        for doc in docs:
            meta = "\n".join(f"{k}: {v}" for k, v in doc.metadata.items())
            doc.page_content = f"{meta}\n\n{doc.page_content}"
        return docs

retriever2 = MetadataRetriever(vectorstore=chroma)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever2,
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": prompt_template,
        "document_variable_name": "context",
        "document_separator": "\n\n",
    }
)

result2 = qa_chain.invoke({"query": query})
print(f"Answer: {result2['result']}, \n*\n*\nN Documents: {len(result2['source_documents'])} \nSource Documents: {result2['source_documents']}")