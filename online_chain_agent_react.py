import sqlite3

from langchain.agents import initialize_agent, AgentType
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.tools import Tool
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

from utils.config import MODEL_NAME, EMBEDDING_MODEL, COMMITS_COLLECTION_NAME, CHROMA_PERSIST_DIR, SQL_PERSIST_DIR, \
    GENERAL_DOCS_COLLECTION_NAME, NUM_CTX, CHROMA_METADATA

# ---- Model and Memory ----
ollama_llm = ChatOllama(
    model=MODEL_NAME,
    num_ctx=NUM_CTX,
    temperature=0.0
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ---- Vector Store and Retrievers ----
# commits
chroma_commits = Chroma(
    collection_name=COMMITS_COLLECTION_NAME,
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
)
retriever_commits = chroma_commits.as_retriever(search_kwargs={"k": 5})

SQLITE_PATH = SQL_PERSIST_DIR
conn   = sqlite3.connect(SQLITE_PATH)
cursor = conn.cursor()

few_shots = [
    (
        "How many commits were made on 2025-05-12?",
        "SELECT COUNT(*) FROM commits WHERE date = '2025-05-12';"
    ),
    (
        "List the commit hashes authored by Alice Smith.",
        "SELECT commit_hash FROM commits WHERE author LIKE '%Alice Smith%';"
    ),
    (
        "Show the latest commit message for commit hash abcd1234.",
        "SELECT message FROM commits WHERE commit_hash = 'abcd1234' LIMIT 1;"
    ),
    (
        "Which author has contributed the highest number of commits?",
        "SELECT author, COUNT(*) AS cnt FROM commits "
        "GROUP BY author ORDER BY cnt DESC LIMIT 1;"
    ),
    (
        "Give me every distinct date when the commit message mentions 'refactor'.",
        "SELECT DISTINCT date FROM commits WHERE message LIKE '%refactor%';"
    ),
    (
        "What files were modified in commit ef01dead?",
        "SELECT files FROM commits WHERE commit_hash LIKE '%ef01dead%';"
    ),
    (
        "When was the first commit created?",
        "SELECT MIN(date) FROM summaries;"
    ),
    (
        "How many commits were made in 2025?",
        "SELECT COUNT(*) FROM commits WHERE date LIKE '2025%';"
    ),
    (
        "How many commits were done by X?",
        "SELECT COUNT(*) FROM commits WHERE author LIKE '%X%';"
    ),
]

examples = "\n".join(
    f"Question: {q}\nSQL: {s}" for q, s in few_shots
)

# 3) Prompt template: translate NL → SQL (SQLite dialect) and output *only* the query
sql_prompt = PromptTemplate(
    input_variables=["question"],
    template=f"""{examples}

        You are an expert SQLite assistant.
        Translate the user's question into the SHORTEST valid SQL query
        that queries ONLY the table `commits`
        (id, commit_hash, author, date, message, files, diffs).
        
        For authors, use LIKE format.
        
        ⚠️  Reply **only** with the SQL query—no commentary, no ``` fencing.
        
        Question: {{question}}
        SQL:
    """
)

sql_chain = LLMChain(llm=ollama_llm, prompt=sql_prompt)

# general docs
chroma_docs = Chroma(
    collection_name=GENERAL_DOCS_COLLECTION_NAME,
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
)
retriever_docs = chroma_docs.as_retriever(search_kwargs={"k": 5})

def format_doc(doc):
    meta = doc.metadata
    return (
        f"COMMIT: {meta.get('commit_hash', '')}\n"
        f"INDEX: {meta.get('index', '')}\n"
        f"AUTHOR: {meta.get('author', '')}\n"
        f"DATE: {meta.get('date', '')}\n"
        f"TYPE: {meta.get('type', '')}\n"
        f"MSG : {meta.get('message', '')}\n"
        f"{doc.page_content}"
    )

# ---- Tool Definitions ----
def retrieve_commits_context(query: str) -> str:
    """Retrieves information about commits from the MuJS repository."""
    docs = retriever_commits.invoke(query)
    return "\n\n".join([format_doc(doc) for doc in docs])

def retrieve_general_context(query: str) -> str:
    """Retrieves only general project information from the MuJS documentation."""
    # docs = retriever_docs.get_relevant_documents(query)
    # return "\n".join(doc.page_content for doc in docs)
    return "MUJS docs_extra non è ancora implementato."

def nl_to_sql_commit_context(question: str) -> str:
    """
    Process a natural-language question about summaries and execute the corresponding SQL query.
    1. Convert a natural-language question into SQL via LLM.
    2. Execute the SELECT on SQLite and return the results.
    """
    sql_query = sql_chain.run(question).strip()

    # Allow only SELECT statements for safety
    if not sql_query.lower().startswith("select"):
        return ("I can execute SELECT queries only for safety.\n"
                f"Generated query: {sql_query}")

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        header = [col[0] for col in cursor.description]

        if not rows:
            return f"SQL:\n{sql_query}\n\nNo rows returned."

        formatted_rows = "\n".join(", ".join(map(str, r)) for r in rows)
        return (f"SQL:\n{sql_query}\n\n"
                f"Results (header → {header}):\n{formatted_rows}")

    except Exception as e:
        return f"Error executing:\n{sql_query}\n\n{e}"

tool_commits = Tool(
    name="commit_code",
    func=retrieve_commits_context,
    description="Use this tool to retrieve information about functions, code, source files, code changes, or commits."
)

tool_docs = Tool(
    name="general_project_info",
    func=retrieve_general_context,
    description="Use this tool to retrieve general information about the project."
)

tool_sql = Tool(
    name="summary_db_sql",
    func=nl_to_sql_commit_context,
    description=("Use this tool to query the `commits` table for filtered/aggregated/counted data about commit hashes, "
                 "authors, dates, messages, files, diffs, and related counts.")
)

tools = [tool_commits, tool_docs, tool_sql]

# ---- Inizializzazione dell'agente ----
agent = initialize_agent(
    tools,
    ollama_llm,
    #agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    system_message_prompt_template=SystemMessagePromptTemplate.from_template(
        """
        You are a helpful assistant for the MuJS project.  
        - Use the `commit_code` tool to answer any question about code, source files, functions, code changes, or commits.  
        - Use the `general_project_info` tool only for questions about general project information, documentation, or high-level overviews.  
        - Use the `summary_db_sql` tool only for questions that require aggregated or filtered information about commits, code and source files.  
            (authors, dates, commit hashes, messages, files, diffs, counts).  
        - If you do not know the answer, reply with "I don't know".
        
        Examples:  
        - "How does function X work?" → use `commit_code`  
        - "What changed in commit Y?" → use `commit_code`  
        - "What is MuJS?" → use `general_project_info`
        - "How many commits on 2025-05-12?" → use `summary_db_sql`
        - "Show the latest commit." → use `summary_db_sql`
        
        """
    ),
)


if __name__ == "__main__":
    print("Type 'exit' to quit.")
    while True:
        question = input("You: ")
        if question.strip().lower() == "exit":
            break
        response = agent.invoke(question)
        print(f"Assistant: {response['output']}")
