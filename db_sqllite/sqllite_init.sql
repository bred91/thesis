-- SQLite database schema for the project

-- logs table to store log entries
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TEXT,
    level TEXT,
    message TEXT
);

-- commits table to store commit information
CREATE TABLE IF NOT EXISTS commits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commit_hash TEXT UNIQUE,
    author TEXT,
    date TEXT,
    message TEXT,
    files TEXT,
    diffs TEXT
);

-- summaries table to store summaries related to commits for a specific experiment
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commit_id INTEGER,
    experiment_name TEXT,
    date TEXT,
    llama_category TEXT,
    llama_summary TEXT,
    llama_summary_retrieved_docs TEXT,
    llama_summary_retrieved_docs_count INTEGER,
    llama_summary_retrieved_docs_scores TEXT,
    llama_tech_summary TEXT,
    llama_tech_summary_retrieved_docs TEXT,
    llama_tech_summary_retrieved_docs_count INTEGER,
    llama_tech_summary_retrieved_docs_scores TEXT,
    
    FOREIGN KEY (commit_id) REFERENCES commits(id)
)

