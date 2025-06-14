import json
import sqlite3
from datetime import datetime

from utils.logging_handler import SQLiteHandler

db_handler = SQLiteHandler("db_sqllite/sqlite.db")

def save_commits_to_sqlite(commits):
    """
    Save a list of commits to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    # Bulk insert commits into the database
    cursor.executemany("""
        INSERT OR IGNORE INTO commits (commit_hash, author, date, message, files, diffs) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (
            commit.get("hash", ""),
            commit.get("author", ""),
            commit.get("date", "").strftime('%Y-%m-%d %H:%M:%S') if isinstance(commit.get("date"), datetime) else commit.get("date", ""),
            commit.get("message", ""),
            commit.get("files", ""),
            commit.get("diffs", "")
        ) for commit in commits.values()
    ])

    conn.commit()
    conn.close()

def save_summaries_to_sqlite(
        commit_id,
        experiment_name,
        date,
        llama_category,
        llama_summary,
        llama_summary_retrieved_docs,
        llama_tech_summary,
        llama_tech_summary_retrieved_docs
    ):
        """
        Save a summary to the SQLite database.
        """
        conn = sqlite3.connect(db_handler.db_path)
        cursor = conn.cursor()

        # Insert summary of a commit into the database
        cursor.execute(
            """
            INSERT INTO summaries (commit_id, experiment_name, date, llama_category, llama_summary, 
                                   llama_summary_retrieved_docs, llama_tech_summary, 
                                   llama_tech_summary_retrieved_docs) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                commit_id,
                experiment_name,
                date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(date, datetime) else date,
                llama_category,
                llama_summary,
                json.dumps(serialize_docs(llama_summary_retrieved_docs)),
                llama_tech_summary,
                json.dumps(serialize_docs(llama_tech_summary_retrieved_docs))
            )
        )

        conn.commit()
        conn.close()

def serialize_docs(docs):
    # Convert each Document to a dict
    return [doc.__dict__ if hasattr(doc, '__dict__') else str(doc) for doc in docs]