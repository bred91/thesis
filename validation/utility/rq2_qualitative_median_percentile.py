import os
import sqlite3
import pandas as pd

from utils.logging_handler import SQLiteHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'db_sqllite', 'sqlite.db')

db_handler = SQLiteHandler(DB_PATH)
conn = sqlite3.connect(db_handler.db_path)

query_rq2_g_eval = """
    SELECT accuracy, completeness, usefulness, readability, overall
    FROM rq2_qualitative_evaluations
    WHERE evaluation_type = 'g_eval'
"""

df_rq2_g_eval = pd.read_sql_query(query_rq2_g_eval, conn)

metrics = ['accuracy', 'completeness', 'usefulness', 'readability', 'overall']

print("<---RQ2 Qualitative Evaluations (g_eval)--->")
for metric in metrics:
    if metric in df_rq2_g_eval.columns:
        serie = df_rq2_g_eval[metric].dropna()
        print(f"\nMetric: {metric}")
        print(f"Median: {serie.median():.2f}")
        print("Quantiles:")
        for q in [0.25, 0.5, 0.75]:
            print(f"  {int(q*100)}° quantile: {serie.quantile(q):.2f}")


query_rq2_human = """
    SELECT accuracy, completeness, usefulness, readability, overall
    FROM rq2_qualitative_evaluations
    WHERE evaluation_type = 'human'
"""

df_rq2_human = pd.read_sql_query(query_rq2_human, conn)

print("\n<---RQ2 Qualitative Evaluations (human)--->")
for metric in metrics:
    if metric in df_rq2_human.columns:
        serie = df_rq2_human[metric].dropna()
        print(f"\nMetric: {metric}")
        print(f"Median: {serie.median():.2f}")
        print("Quantiles:")
        for q in [0.25, 0.5, 0.75]:
            print(f"  {int(q*100)}° quantile: {serie.quantile(q):.2f}")

conn.close()
