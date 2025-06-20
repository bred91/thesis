import json
import sqlite3
from datetime import datetime

from utils.config import SQL_PERSIST_DIR
from utils.logging_handler import SQLiteHandler

db_handler = SQLiteHandler(SQL_PERSIST_DIR)

def save_commits_to_sqlite(commits):
    """
    Save a list of commits to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    # Bulk insert of commits into the database
    cursor.executemany("""
        INSERT OR IGNORE INTO commits (commit_hash, author, date, message, files, diffs) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (
            commit.get("hash", ""),
            commit.get("author", ""),
            commit.get("date", "").strftime('%Y-%m-%d %H:%M:%S') if isinstance(commit.get("date"), datetime) else commit.get("date", ""),
            commit.get("message", ""),
            json.dumps(commit['files']),
            json.dumps(commit['diffs'])
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
                                   llama_summary_retrieved_docs, llama_summary_retrieved_docs_count, 
                                   llama_summary_retrieved_docs_scores, llama_tech_summary,                                 
                                   llama_tech_summary_retrieved_docs, llama_tech_summary_retrieved_docs_count,
                                   llama_tech_summary_retrieved_docs_scores) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                commit_id,
                experiment_name,
                date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(date, datetime) else date,
                llama_category,
                llama_summary,
                json.dumps(serialize_docs(llama_summary_retrieved_docs)),
                len(llama_summary_retrieved_docs),
                json.dumps([score for _, score in llama_summary_retrieved_docs]),
                llama_tech_summary,
                json.dumps(serialize_docs(llama_tech_summary_retrieved_docs)),
                len(llama_tech_summary_retrieved_docs),
                json.dumps([score for _, score in llama_tech_summary_retrieved_docs])
            )
        )

        conn.commit()
        conn.close()

def serialize_docs(docs):
    # Convert each Document to a dict
    return [doc[0].__dict__ if hasattr(doc[0], '__dict__') else str(doc[0]) for doc in docs]


def delete_all_summaries():
    """
    Delete all summaries from the SQLite database and reset autoincrement ID.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM summaries")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='summaries'")
    conn.commit()
    conn.close()