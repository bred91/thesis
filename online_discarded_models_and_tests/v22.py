from langchain.chains import (
    create_retrieval_chain,
    create_history_aware_retriever,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import OllamaLLM, OllamaEmbeddings

chroma = Chroma(
    collection_name="commits",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    collection_metadata={"hnsw:space": "cosine"},
    persist_directory="./chromadb_v1",
)

llm = OllamaLLM(model="llama3.1:8b-instruct-q8_0", temperature=0.0)

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

# retriever “semplice”
base_retriever = chroma.as_retriever()

# 1) retriever che riscrive la query in base alla cronologia
rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "Riscrivi la seguente domanda in una forma autonoma, includendo tutte le informazioni utili tratte dalla chat history.\n"
         "Chat history:\n{chat_history}\n\nDomanda: {input}\nRiscritta:"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm,               # lo stesso LLM va bene
    base_retriever,
    rewrite_prompt,
)

# 2) catena di combinazione documenti (come prima)
combine_docs_chain = create_stuff_documents_chain(
    llm,
    main_prompt,
    document_prompt=doc_prompt,
    document_separator="\n\n",
    document_variable_name="context",
)

# 3) catena RAG finale
rag_chain = create_retrieval_chain(history_aware_retriever, combine_docs_chain)

# ---------------------------------------------------------
chat_history = []

while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "/exit":
        break

    result = rag_chain.invoke(
        {
            "input": user_input,
            "chat_history": chat_history,
        }
    )

    print("\n=== Answer ===\n")
    print(result["answer"])

    # Aggiorna la cronologia con oggetti BaseMessage
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=result["answer"]))
