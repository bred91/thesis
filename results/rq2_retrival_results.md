# RQ2 Retrival Results


### Retrival (K=5)
| Metric  | Value  |
|---------|--------|
| P@5     | 0.3810 |
| NDCG@5  | 0.8436 |
| MAP     | 0.8130 |
| MRR     | 0.8847 |

### Called Tools
OK = all expected tools called
PARTIAL = some expected tools called
KO = no expected tools called

| Status  | Count |
|---------|-------|
| OK      | 45    |
| PARTIAL | 5     |
| KO      | 0     |


### Debug (KO / PARTIAL)
| qid    | status         | called                                             | expected                                             |
|--------|----------------|----------------------------------------------------|------------------------------------------------------|
| qid=36 | status=PARTIAL | called=['nl_to_sql_commit_context', 'commit_code'] | expected=['commit_code']                             |
| qid=47 | status=PARTIAL | called=['nl_to_sql_commit_context']                | expected=['nl_to_sql_commit_context', 'commit_code'] |
| qid=48 | status=PARTIAL | called=['nl_to_sql_commit_context']                | expected=['nl_to_sql_commit_context', 'commit_code'] |
| qid=49 | status=PARTIAL | called=['nl_to_sql_commit_context']                | expected=['nl_to_sql_commit_context', 'commit_code'] |
| qid=50 | status=PARTIAL | called=['nl_to_sql_commit_context']                | expected=['nl_to_sql_commit_context', 'commit_code'] |