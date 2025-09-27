import os
import sqlite3
import pandas as pd

from utils.logging_handler import SQLiteHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'db_sqllite', 'sqlite.db')

db_handler = SQLiteHandler(DB_PATH)
conn = sqlite3.connect(db_handler.db_path)

query_rq2 = """
    SELECT rouge_1, rouge_2, rouge_l, bleu, meteor, bert_precision, bert_recall, bert_f1
    FROM rq2_quantitative_evaluations
"""

df_rq2 = pd.read_sql_query(query_rq2, conn)

metrics = ['rouge_1', 'rouge_2', 'rouge_l', 'bleu', 'meteor', 'bert_precision', 'bert_recall', 'bert_f1']

print("<---RQ2 Summary Metrics--->")
for metric in metrics:
    if metric in df_rq2.columns:
        serie = df_rq2[metric].dropna()
        print(f"\nMetric: {metric}")
        print(f"Median: {serie.median():.4f}")
        print("Quantiles:")
        for q in [0.25, 0.5, 0.75]:
            print(f"  {int(q*100)}° quantile: {serie.quantile(q):.4f}")

conn.close()
