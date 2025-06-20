import sqlite3

from langchain_core.runnables import RunnableSequence
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from utils.config import MODEL_NAME, NUM_CTX, EMBEDDING_MODEL, COMMITS_COLLECTION_NAME, CHROMA_PERSIST_DIR, \
    GENERAL_DOCS_COLLECTION_NAME, CHROMA_METADATA

# -------------------- LLM & Embeddings --------------------
llm = ChatOllama(
    model=MODEL_NAME,
    num_ctx=NUM_CTX,
    temperature=0.0
)

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

# -------------------- Vector Stores --------------------
# Commits (summaries, code diffs & messages)
commit_store = Chroma(
    collection_name=COMMITS_COLLECTION_NAME,
    embedding_function=embeddings,
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
)
retriever_commits = commit_store.as_retriever(search_kwargs={"k": 5})

# General documentation
doc_store = Chroma(
    collection_name=GENERAL_DOCS_COLLECTION_NAME,
    embedding_function=embeddings,
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
)
retriever_docs = doc_store.as_retriever(search_kwargs={"k": 5})

# -------------------- Helper --------------------

def _format_commit(doc) -> str:
    """Pretty‑print a commit document (metadata + first chunk of content)."""
    m = doc.metadata
    return (
        f"COMMIT: {m.get('commit_hash', '')}\n"
        f"INDEX:  {m.get('index', '')}\n"
        f"AUTHOR: {m.get('author', '')}\n"
        f"DATE:   {m.get('date', '')}\n"
        f"TYPE:   {m.get('type', '')}\n"
        f"MSG  : {m.get('message', '')}\n"
        f"---\n{doc.page_content[:1_000]}"  # truncate long diffs
    )

# -------------------- Tools --------------------
# Tool 1 - Commit Code Search
@tool(
    name_or_callable="commit_code",
    description="""
        Use this tool to retrieve information about functions, code, source files, code changes, or commits.
    """
)
def commit_code(query: str) -> str:
    """Retrieves information about commits from the MuJS repository."""
    # Retrieves relevant documents based on the query
    docs = retriever_commits.invoke(query)
    if not docs:
        return "No relevant commits found."

    formatted = [_format_commit(d) for d in docs]
    return "\n\n".join(formatted)


# Tool 2 - General Project Information
@tool(
    name_or_callable="general_project_info",
    description="""
        Use this tool to retrieve general information about the project.
    """
)
def general_project_info(query: str) -> str:
    """Retrieves only general project information from the MuJS documentation."""
    docs = retriever_docs.invoke(query)
    if not docs:
        return "No relevant documentation found."

    return "\n---\n".join(d.page_content for d in docs)


SQLITE_PATH = "./db_sqllite/sqlite.db"

few_shots = [
    ("How many commits were made on 2025-05-12?", "SELECT COUNT(*) FROM commits WHERE date = '2025-05-12';"),
    ("List the commit hashes authored by Alice Smith.", "SELECT commit_hash FROM commits WHERE author LIKE '%Alice Smith%';"),
    ("Show the latest commit message for commit hash abcd1234.", "SELECT message FROM commits WHERE commit_hash = 'abcd1234' LIMIT 1;"),
    ("Which author has contributed the highest number of commits?", "SELECT author, COUNT(*) AS cnt FROM commits GROUP BY author ORDER BY cnt DESC LIMIT 1;"),
    ("Give me every distinct date when the commit message mentions 'refactor'.", "SELECT DISTINCT date FROM commits WHERE message LIKE '%refactor%';"),
    ("What files were modified in commit ef01dead?", "SELECT files FROM commits WHERE commit_hash LIKE '%ef01dead%';"),
    ("When was the first commit created?", "SELECT MIN(date) FROM commits;"),
    ("How many commits were made in 2025?", "SELECT COUNT(*) FROM commits WHERE date LIKE '2025%';"),
    ("How many commits were done by X?", "SELECT COUNT(*) FROM commits WHERE author LIKE '%X%';"),
]
_examples = "\n".join(f"Question: {q}\nSQL: {s}" for q, s in few_shots)

sql_prompt = PromptTemplate(
    input_variables=["question"],
    template=f"""
        {_examples}

        You are an expert SQLite assistant.
        Translate the user's question into the SHORTEST valid SQL query that queries ONLY the table `commits`\n(id, commit_hash, author, date, message, files, diffs).
        For author matching, use LIKE.\n\n⚠️  Reply *only* with the SQL query.
        Question: {{question}}\nSQL:""",
)

sql_chain = sql_prompt | llm

# Tool 3 - Natural‑language → SQL
@tool(
    name_or_callable="nl_to_sql_commit_context", 
    description="""
        Use this tool to query the `commits` table for filtered/aggregated/counted data 
        about commit hashes, authors, dates, messages, files, diffs, and related counts.
    """
)
def nl_to_sql_commit_context(question: str) -> str:
    """
    Process a natural-language question about summaries and execute the corresponding SQL query.
    1. Convert a natural-language question into SQL via LLM.
    2. Execute the SELECT on SQLite and return the results.
    """
    sql_query = sql_chain.invoke(question).content.strip()

    if not sql_query.lower().startswith("select"):
        return (
            "For safety I only execute SELECT statements.\n"
            f"Generated query: {sql_query}"
        )

    try:
        conn = sqlite3.connect(SQLITE_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        header = [col[0] for col in cursor.description]

        if not rows:
            return f"SQL:\n{sql_query}\n\nNo rows returned."

        formatted_rows = "\n".join(", ".join(map(str, r)) for r in rows)
        return (
            f"SQL:\n{sql_query}\n\nResults (header → {header}):\n{formatted_rows}"
        )
    except Exception as e:
        return f"Error executing:\n{sql_query}\n\n{e}"

# -------------------- Agent --------------------

# Checkpointer for saving conversation state
# InMemorySaver is used to save the conversation state in memory.
# This allows the agent to maintain context across multiple interactions.
checkpointer = InMemorySaver()

# React Agent using LangGraph
agent = create_react_agent(
    model=llm,
    tools=[commit_code, general_project_info, nl_to_sql_commit_context],
    prompt="""
        You are a helpful assistant for the MuJS project.  
        - Use the `commit_code` tool to answer any question about code, source files, functions, code changes, commits or relationships between them.
        - Use the `general_project_info` tool only for questions about general project information, documentation, or high-level overviews.  
        - Use the `nl_to_sql_commit_context` tool only for questions that require aggregated or filtered information about commits, code and source files.  
            (authors, dates, commit hashes, messages, files, diffs, counts).
        - If you are unsure about what tool to use, call both `nl_to_sql_commit_context` and `commit_code`  
        - If you do not know the answer, reply with "I don't know".
        
        Examples:  
        - "How does function X work?" → use `commit_code`  
        - "What changed in commit Y?" → use `commit_code`  
        - "What is MuJS?" → use `general_project_info`
        - "How many commits on 2025-05-12?" → use `nl_to_sql_commit_context`
        - "Show the latest commit." → use `nl_to_sql_commit_context`        
        """,
    checkpointer=checkpointer,
    debug=True,
)

def main() -> None:
    thread_id = "main_session"  
    config = RunnableConfig(configurable={"thread_id": thread_id})

    print("MuJS ReAct Agent. Type `/exit` to quit.\n(Enter \033[1m/exit\033[0m to exit.)")
    print("MuJS ReAct Agent. Type `/exit` to quit.")
    while True:
        user_input = input("You: ")
        if not user_input or user_input.strip().lower() == "/exit":
            break
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
        print("Assistant:", response["messages"][-1].content)

if __name__ == "__main__":
    main()
