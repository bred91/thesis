few_shots = [
    (
        "How many commits were made on 2025-05-12?",
        "SELECT COUNT(*) FROM commits WHERE date = '2025-05-12%';"
    ),
    (
        "List the commit hashes authored by Alice Smith.",
        "SELECT commit_hash FROM commits WHERE author LIKE '%Alice%Smith%' OR author LIKE '%Smith%Alice%';"
    ),
    (
        "Show the latest commit message",
        "SELECT message FROM commits ORDER BY date LIMIT 1;"
    ),
    (
        "Retrieve the details of the commit with hash ef01dead",
        "SELECT * FROM commits WHERE commit_hash LIKE '%ef01dead%';"
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
        "How many commits were done by Alice Smith?",
        "SELECT COUNT(*) FROM commits WHERE author LIKE '%Alice%Smith%' OR author LIKE '%Smith%Alice%';"
    ),
    (
        "How many times the file `jsarray.c` was modified during the last year?",
        "SELECT COUNT(*) FROM commits WHERE files LIKE '%jsarray.c%' AND date >= date('now', '-1 year');"
    ),
    (
        "When the file `jsarray.c` was added to the project?",
        "SELECT date FROM commits WHERE files LIKE '%jsarray.c%' ORDER BY date LIMIT 1;"
    ),
    (
        "Retrieve me the commit where the issue #123 was fixed.",
        "SELECT * FROM commits WHERE message LIKE '%issue%123%' OR message LIKE '%fixes%123%' OR message LIKE '%resolved%123%';"
    )
]

graph_agent_react_nl2sql_examples_examples = "\n".join(f"Question: {q}\nSQL: {s}" for q, s in few_shots)