from utils.entities import Summary, Commit
from utils.sqlite_utils import retrieve_all_summaries_to_be_validated, retrieve_all_commits_to_be_validated, \
    retrieve_all_rq1_golden_standard
from validation.categorization import validate_categorization
from validation.rq1_g_eval import calculate_save_rq1_g_eval
from validation.rq1_quantitative import calculate_save_rq1_quantitative_evaluation


def retrieve_summaries() -> list[Summary]:
    """
    Retrieve all summaries from the SQLite database that are marked for validation.
    """
    return retrieve_all_summaries_to_be_validated()


def retrieve_commits() -> list[Commit]:
    """
    Retrieve all commits from the SQLite database that are associated with the summaries to be validated.
    """
    return retrieve_all_commits_to_be_validated()


def retrieve_rq1_golden_standard():
    """
    Retrieve the golden standard for RQ1 from the SQLite database.
    This is a hand-made set of summaries that are used as a reference for evaluation.
    """
    golden_standard = retrieve_all_rq1_golden_standard()
    res = {
        "commit_ids": [],
        "general": [],
        "technical": []
    }
    for gs in golden_standard:
        res["commit_ids"].append(gs["commit_id"])
        res["general"].append(gs["general"])
        res["technical"].append(gs["technical"])
    return res


def main():
    # categorization
    validate_categorization()

    # Load summaries from the SQLite database
    summaries: list[Summary] = retrieve_summaries()
    commits: list[Commit] = retrieve_commits()
    rq1_golden_standard = retrieve_rq1_golden_standard()

    # RQ1: Validate the quality of the summaries of the commits
    calculate_save_rq1_quantitative_evaluation(summaries, rq1_golden_standard, with_bert=True)

    calculate_save_rq1_g_eval(summaries, commits)


if __name__ == "__main__":
    main()
