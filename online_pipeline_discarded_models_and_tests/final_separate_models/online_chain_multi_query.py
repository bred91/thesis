from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

from utils.config import COMMITS_COLLECTION_NAME, EMBEDDING_MODEL, CHROMA_PERSIST_DIR, MODEL_NAME, NUM_CTX, SEED, \
    CHROMA_METADATA

chroma = Chroma(
    collection_name=COMMITS_COLLECTION_NAME,
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
)

# Base LLM for Q&A and document summarization
llm_main    = OllamaLLM(model=MODEL_NAME, temperature=0.0, num_ctx=NUM_CTX, seed=SEED)
llm_queries = OllamaLLM(model=MODEL_NAME, temperature=0.3, num_ctx=NUM_CTX, seed=SEED)

# Advanced retriever with multi-query support
# base retriever
base_retriever = chroma.as_retriever(
    search_type="similarity",  # similarity search
    search_kwargs={"k": 3}     # top-k documents
)

# MultiQueryRetriever for generating alternative queries
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm_queries,
    include_original=True,
)

# System prompt for the main LLM
SYSTEM = """
You are a helpful assistant that answers questions about the MuJS project based on the provided context.
You will receive a series of documents, each with metadata including a commit hash, date,
message, and content. If you do not know the answer, you should say "I don't know".
<context>
{context}
</context>
""".strip()

main_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# Prompt Template for individual documents
doc_prompt = PromptTemplate(
    input_variables=["page_content", "commit_hash", "index", "author",
                     "date", "message", "type"],
    template=(
        "COMMIT: {commit_hash}\n"
        "INDEX : {index}\n"
        "AUTHOR: {author}\n"
        "DATE  : {date}\n"
        "TYPE  : {type}\n"
        "MSG   : {message}\n"
        "{page_content}"
    ),
)

# Stuff Documents Chain
# Combines the documents into a single context for the main LLM
combine_docs_chain = create_stuff_documents_chain(
    llm=llm_main,
    prompt=main_prompt,
    document_prompt=doc_prompt,
    document_separator="\n\n",
    document_variable_name="context",
)

# Create the final RAG chain
# This chain will use the multi-query retriever and the document combining chain
rag_chain = create_retrieval_chain(
    retriever=multi_retriever,
    combine_docs_chain=combine_docs_chain,
)

chat_history = []

print("Chat RAG - type /exit to quit\n")
while True:
    query = input("You: ")
    if query.strip().lower() == "/exit":
        break

    result = rag_chain.invoke({"input": query, "chat_history": chat_history})
    print("\n=== Answer ===\n")
    print(result["answer"])
    print("\n=== Used Documents ===\n")
    print(f"Number of documents: {len(result['context'])}\n")

    # Update chat history
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": result["answer"]})
