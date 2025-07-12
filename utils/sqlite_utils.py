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


def retrieve_all_summaries_to_be_validated():
    """
    Retrieve all summaries that will be validated from the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM summaries") # todo: add filtering for 50/100 summaries to be validated
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    summaries = []
    for row in rows:
        summary = {
            "id": row[0],
            "commit_id": row[1],
            "experiment_name": row[2],
            "date": row[3],
            "llama_category": row[4],
            "llama_summary": row[5],
            "llama_summary_retrieved_docs": json.loads(row[6]),
            "llama_summary_retrieved_docs_count": row[7],
            "llama_summary_retrieved_docs_scores": json.loads(row[8]),
            "llama_tech_summary": row[9],
            "llama_tech_summary_retrieved_docs": json.loads(row[10]),
            "llama_tech_summary_retrieved_docs_count": row[11],
            "llama_tech_summary_retrieved_docs_scores": json.loads(row[12])
        }
        summaries.append(summary)

    conn.close()
    return summaries