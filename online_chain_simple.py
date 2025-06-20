from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate

# -- Vector store & retriever --------------------------------------------------
chroma = Chroma(
    collection_name="commits",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    collection_metadata={"hnsw:space": "cosine"},
    persist_directory="./chromadb_v1",
)
retriever = chroma.as_retriever()

# -- LLM -----------------------------------------------------------------------
llm = OllamaLLM(model="llama3.1:8b-instruct-q8_0", num_ctx=32768, temperature=0.0)

# -- System Prompt ---------------------------------------------------------
SYSTEM = """
You are a helpful assistant that answers questions based on the provided context.
You will receive a series of documents, each with metadata including a commit hash, date, message, and content.
If you do not know the answer, you should say "I don't know".
<context>
{context}
</context>
"""
main_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM.strip()),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# -- Prompt for individual documents ---------------------------------------------
doc_prompt = PromptTemplate(
    input_variables=["page_content", "commit_hash", "index", "author", "date", "message", "type"],
    template=(
        "COMMIT: {commit_hash}\n"
        "INDEX: {index}\n"
        "AUTHOR: {author}\n"
        "DATE: {date}\n"
        "TYPE: {type}\n"
        "MSG : {message}\n"
        "{page_content}"
    ),
)

# -- Create the retrieval chain ---------------------------------------------
combine_docs_chain = create_stuff_documents_chain(
    llm,
    main_prompt,
    document_prompt=doc_prompt,
    document_separator="\n\n",
    document_variable_name="context",
)

rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# -- Query ---------------------------------------------------------------------
query = "When was introduced the lexing of regular expressions??"

chat_history = []

print("Chat RAG - type /exit to quit\n")
while True:
    query = input("You: ")
    if query.strip().lower() == "/exit":
        break

    result = rag_chain.invoke({"input": query, "chat_history": chat_history})
    print("\n=== Answer ===\n")
    print(result["answer"])

    # Update chat history
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": result["answer"]})
