import evaluate

from utils.entities import QuestionAnswer

# Note: trec_eval supports only certain K values
# ALLOWED_K -> {5,10,15,20,30,100,200,500,1000}
K = 5

trec = evaluate.load("trec_eval")


def _parse_list(x):
    """Parses a string or list into a list of strings."""
    # None
    if x is None:
        return []

    # string
    if isinstance(x, str):
        # split the string by \n
        parts = x.split('\n')
        return [p.strip() for p in parts if p.strip()]

    print(f"WARNING: unexpected type {type(x)} in _parse_list")
    print(f"Value: {x}")

    return []


def _dedup_preserve_order(seq):
    """Deduplicates a list while preserving order."""
    seen, out = set(), []
    for s in seq:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def evaluate_tool_called(called: list[str], expected: list[str]) -> str:
    """Evaluates the tool calls."""
    set_c, set_e = set(called), set(expected)

    if set_c == set_e:
        return "OK"
    elif set_c & set_e:
        return "PARTIAL"
    else:
        return "KO"


def calculate_retrieval_and_tool_metrics(questions_answers: list[QuestionAnswer]):
    # building TREC qrel/run
    qrel_rows = []  # qrel: query, q0, docid, rel
    run_rows = []  # run: query, q0, docid, rank, score, system

    tool_counts = {"OK": 0, "PARTIAL": 0, "KO": 0}
    tool_debug = []

    for row in questions_answers:
        # ------- Retrieval evaluation --------
        q_id = int(row.question_id)

        docs_expected = _parse_list(row.docs_expected)
        docs_retrieved = _parse_list(row.docs_retrieved)

        # 1) Build a per-query surrogate ID map from the UNION (order preserved)
        unified = _dedup_preserve_order(docs_retrieved + [x for x in docs_expected if x not in set(docs_retrieved)])
        id_map = {text: str(i + 1) for i, text in enumerate(unified)}  # surrogate ids: "1","2",...

        # 2) QREL: binary relevance (1) using surrogate IDs
        for text in _dedup_preserve_order(docs_expected):
            doc_id = id_map[text]
            qrel_rows.append({"query": q_id, "q0": "q0", "docid": doc_id, "rel": 1})

        # 3) RUN: dedup retrieved, assign sequential ranks, use surrogate IDs
        dedup_retrieved = _dedup_preserve_order(docs_retrieved)
        for rank, text in enumerate(dedup_retrieved, start=1):
            doc_id = id_map[text]
            run_rows.append({
                "query": q_id, "q0": "q0", "docid": doc_id,
                "rank": rank, "score": 1.0 / rank, "system": "rq2"
            })

        # ---------- Tool evaluation ----------
        tools_called = _parse_list(row.tool_called)
        tools_expected = _parse_list(row.tool_expected)

        status = evaluate_tool_called(tools_called, tools_expected)
        tool_counts[status] += 1

        if status != "OK":
            tool_debug.append({"question_id": q_id, "status": status,
                               "called": tools_called, "expected": tools_expected})

    # dict -> list conversion
    def _rows_to_dict(rows_list, keys):
        if rows_list:
            return {k: [r[k] for r in rows_list] for k in keys}
        return {k: [] for k in keys}

    q_rel = _rows_to_dict(qrel_rows, ["query", "q0", "docid", "rel"])
    run = _rows_to_dict(run_rows, ["query", "q0", "docid", "rank", "score", "system"])

    # metric calculation
    res = trec.compute(predictions=[run], references=[q_rel])

    print(f"=== RETRIVAL RESULTS (K={K}) ===")
    print(f"P@{K}:    {res.get(f'P@{K}', None)}")
    print(f"NDCG@{K}: {res.get(f'NDCG@{K}', None)}")
    print(f"MAP:      {res.get('map', None)}")
    print(f"MRR:      {res.get('recip_rank', None)}")

    print("\n=== CALLED TOOLS RESULTS ===")
    print(f"OK:      {tool_counts['OK']}")
    print(f"PARTIAL: {tool_counts['PARTIAL']}")
    print(f"KO:      {tool_counts['KO']}")

    # debug of the KO/PARTIAL cases
    if tool_debug:
        print("\n=== TOOL DEBUG (KO / PARTIAL) ===")
        for d in sorted(tool_debug, key=lambda x: x["question_id"]):
            print(f"qid={d['question_id']} | status={d['status']} | called={d['called']} | expected={d['expected']}")