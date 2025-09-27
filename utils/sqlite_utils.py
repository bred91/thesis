import json
import sqlite3
from datetime import datetime

from utils.config import SQL_PERSIST_DIR, OFFLINE_PIPELINE_TEST_NAME
from utils.entities import Summary, Commit, DetailedRq1QuantitativeResults, QuestionAnswer, \
    DetailedRq2QuantitativeResults
from utils.logging_handler import SQLiteHandler

db_handler = SQLiteHandler(SQL_PERSIST_DIR)


def save_commits_to_sqlite(commits):
    """
    Save a list of commits to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    # Bulk insert of commits into the database
    cursor.executemany(
        """
        INSERT OR IGNORE INTO commits (commit_hash, author, date, message, files, diffs)
        VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (
                commit.get("hash", ""),
                commit.get("author", ""),
                commit.get("date", "").strftime('%Y-%m-%d %H:%M:%S') if isinstance(commit.get("date"), datetime)
                else commit.get("date", ""),
                commit.get("message", ""),
                json.dumps(commit['files']),
                json.dumps(commit['diffs'])
            )
            for commit in commits.values()
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


def retrieve_all_summaries_to_be_validated() -> list[Summary]:
    """
    Retrieve all summaries that will be validated from the SQLite database.

    Returns:
        list[Summary]: A list of Summary objects containing commit details, its summaries and related information.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM summaries WHERE id >= 481 and id < 581")
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    summaries: list[Summary] = []
    for row in rows:
        summary = Summary(
            summary_id=row[0],
            commit_id=row[1],
            experiment_name=row[2],
            date=row[3],
            llama_category=row[4],
            llama_summary=row[5],
            llama_summary_retrieved_docs=json.loads(row[6]),
            llama_summary_retrieved_docs_count=row[7],
            llama_summary_retrieved_docs_scores=json.loads(row[8]),
            llama_tech_summary=row[9],
            llama_tech_summary_retrieved_docs=json.loads(row[10]),
            llama_tech_summary_retrieved_docs_count=row[11],
            llama_tech_summary_retrieved_docs_scores=json.loads(row[12])
        )
        summaries.append(summary)

    conn.close()
    return summaries


def retrieve_all_commits_to_be_validated() -> list[Commit]:
    """
    Retrieve all commits that will be validated from the SQLite database.

    Returns:
        list[dict]: A list of dictionaries containing commit details.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM commits WHERE id >= 481 and id < 581")
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    commits = []
    for row in rows:
        commit = Commit(
            commit_id=row[0],
            commit_hash=row[1],
            author=row[2],
            date=row[3],
            message=row[4],
            files=json.loads(row[5]),
            diffs=json.loads(row[6])
        )
        commits.append(commit)

    conn.close()
    return commits


def save_r1_quantitative_results(quantitative_results: list[DetailedRq1QuantitativeResults]) -> None:
    """
    Save a list of quantitative results to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    # Bulk insert of evaluations into the database
    cursor.executemany("""
                       INSERT INTO rq1_quantitative_evaluations (commit_id, exp_name, "date", summary_type, rouge_1,
                                                                 rouge_2, rouge_l,
                                                                 bleu, meteor, bert_precision, bert_recall, bert_f1)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, [
                           (
                               result.commit_id,
                               OFFLINE_PIPELINE_TEST_NAME,
                               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               result.summary_type,
                               result.rouge_1,
                               result.rouge_2,
                               result.rouge_L,
                               result.bleu,
                               result.meteor,
                               result.bert_precision,
                               result.bert_recall,
                               result.bert_f1
                           )
                           for result in quantitative_results
                       ])

    conn.commit()
    conn.close()


def save_rq1_g_evals(evaluation_list) -> None:
    """
    Save a list of evaluations to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    # Bulk insert of evaluations into the database
    cursor.executemany("""
                       INSERT INTO rq1_qualitative_evaluations (commit_id, evaluation_type, exp_name, "date",
                                                                summary_type, accuracy,
                                                                completeness, usefulness, readability,
                                                                technological_depth, overall, justification,
                                                                error, raw_response)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, [
                           (
                               evaluation["commit_id"],
                               evaluation.get("evaluation_type", "g_eval"),
                               OFFLINE_PIPELINE_TEST_NAME,
                               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               evaluation["summary_type"],
                               evaluation.get("accuracy", None),
                               evaluation.get("completeness", None),
                               evaluation.get("usefulness", None),
                               evaluation.get("readability", None),
                               evaluation.get("technical_depth", None),
                               evaluation.get("overall", None),
                               evaluation.get("justification", None),
                               evaluation.get("error", None),
                               evaluation.get("raw_response", None)
                           )
                           for evaluation in evaluation_list
                       ])

    conn.commit()
    conn.close()


def retrieve_all_rq1_golden_standard() -> list[dict]:
    """
    Retrieve the golden standard for RQ1 from the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rq1_golden_standard")
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    golden_standard = []

    for row in rows:
        golden_standard.append({
            "commit_id": row[1],
            "general": row[2],
            "technical": row[3],
        })

    conn.close()
    return golden_standard


def retrieve_all_rq2_questions_answers() -> list[QuestionAnswer]:
    """
    Retrieve all RQ2 questions and answers from the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT qa.id AS question_id,
                          qa.question,
                          a.id  AS answer_id,
                          a.answer,
                          a.answer_expected,
                          a.tool_called,
                          a.tool_expected,
                          a.docs_retrieved,
                          a.docs_expected,
                          a.debug_text
                   FROM rq2_questions AS qa
                            LEFT JOIN rq2_answers AS a ON qa.id = a.question_id
                   WHERE a.answer IS NOT NULL
                   """)
    rows = cursor.fetchall()

    # Convert rows to a list of QuestionAnswer objects
    questions_answers: list[QuestionAnswer] = []
    for row in rows:
        question_answer = QuestionAnswer(
            question_id=row[0],
            question=row[1],
            answer_id=row[2],
            answer=row[3],
            answer_expected=row[4],
            tool_called=row[5],
            tool_expected=row[6],
            docs_retrieved=row[7],
            docs_expected=row[8],
            debug_text=row[9]
        )
        questions_answers.append(question_answer)

    conn.close()
    return questions_answers


def save_rq2_answer(question_id: int, answer: str) -> None:
    """
    Save an RQ2 answer to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE rq2_answers SET answer_expected = ? WHERE question_id = ?",
        (answer, question_id)
    )

    conn.commit()
    conn.close()


def save_rq2_qualitative_result(question_id: int, answer_id: int, evaluation_type: str, accuracy: int,
                                completeness: int,
                                usefulness: int, readability: int, overall: float, justification: str) -> None:
    """
    Save an RQ2 qualitative result to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO rq2_qualitative_evaluations (question_id, answer_id, evaluation_type, accuracy,
                                                            completeness, usefulness, readability, overall,
                                                            justification)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """,
                   (
                       question_id,
                       answer_id,
                       evaluation_type,
                       accuracy,
                       completeness,
                       usefulness,
                       readability,
                       overall,
                       justification
                   )
                   )

    conn.commit()
    conn.close()


def save_rq2_g_evals(evaluation_list) -> None:
    """
    Save a list of RQ2 G-Eval evaluations to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    # Bulk insert of evaluations into the database
    cursor.executemany("""
                       INSERT INTO rq2_qualitative_evaluations (question_id, answer_id, evaluation_type, accuracy,
                                                                completeness, usefulness, readability, overall,
                                                                justification, is_hallucinated)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, [
                           (
                               evaluation["question_id"],
                               evaluation["answer_id"],
                               evaluation.get("evaluation_type", "g_eval"),
                               evaluation.get("accuracy", None),
                               evaluation.get("completeness", None),
                               evaluation.get("usefulness", None),
                               evaluation.get("readability", None),
                               evaluation.get("overall", None),
                               evaluation.get("justification", None),
                               evaluation.get("is_hallucinated", None),
                           )
                           for evaluation in evaluation_list
                       ])

    conn.commit()
    conn.close()


def save_r2_quantitative_results(detailed_results: list[DetailedRq2QuantitativeResults]) -> None:
    """
    Save a list of RQ2 quantitative results to the SQLite database.
    """
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()

    # Bulk insert of evaluations into the database
    cursor.executemany("""
                       INSERT INTO rq2_quantitative_evaluations (question_id, answer_id, exp_name, "date", rouge_1,
                                                                 rouge_2, rouge_l,
                                                                 bleu, meteor, bert_precision, bert_recall, bert_f1)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, [
                           (
                               result.question_id,
                               result.answer_id,
                               OFFLINE_PIPELINE_TEST_NAME,
                               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               result.rouge_1,
                               result.rouge_2,
                               result.rouge_L,
                               result.bleu,
                               result.meteor,
                               result.bert_precision,
                               result.bert_recall,
                               result.bert_f1
                           )
                           for result in detailed_results
                       ])

    conn.commit()
    conn.close()
