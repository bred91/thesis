import os
import sqlite3

import pandas as pd

from utils.logging_handler import SQLiteHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'db_sqllite', 'sqlite.db')

db_handler = SQLiteHandler(DB_PATH)
conn = sqlite3.connect(db_handler.db_path)

query_general = """
    SELECT accuracy, completeness, usefulness, readability, overall
    FROM rq1_qualitative_evaluations
    WHERE summary_type = 'general' and evaluation_type = 'g_eval'
"""

df_general = pd.read_sql_query(query_general, conn)

metrics_general = ['accuracy', 'completeness', 'usefulness', 'readability', 'overall']

print("<---General Summary Metrics--->")
for metric in metrics_general:
    if metric in df_general.columns:
        serie = df_general[metric].dropna()
        print(f"\nMetric: {metric}")
        print(f"Median: {serie.median():.2f}")
        print("Quantiles:")
        for q in [0.25, 0.5, 0.75]:
            print(f"  {int(q*100)}° quantile: {serie.quantile(q):.2f}")


query_technical = """
    SELECT accuracy, completeness, usefulness, readability, technological_depth, overall
    FROM rq1_qualitative_evaluations
    WHERE summary_type = 'technical' and evaluation_type = 'g_eval'
"""

df_technical = pd.read_sql_query(query_technical, conn)

metrics_technical = ['accuracy', 'completeness', 'usefulness', 'readability', 'technical_depth', 'overall']

print("<---Technological Summary Metrics--->")
for metric in metrics_technical:
    if metric in df_technical.columns:
        serie = df_technical[metric].dropna()
        print(f"\nMetric: {metric}")
        print(f"Median: {serie.median():.2f}")
        print("Quantiles:")
        for q in [0.25, 0.5, 0.75]:
            print(f"  {int(q*100)}° quantile: {serie.quantile(q):.2f}")

conn.close()
