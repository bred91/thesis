from utils.file_utils import load_commits
from utils.plot_utils import plot_categories, plot_categories_pie_chart
from utils.sqlite_utils import retrieve_all_summaries_to_be_validated
from utils.validation_utils import calculate_precision_recall_categorization, ground_truth_array


def retrieve_summaries():
    """
    Retrieve all summaries from the SQLite database that are marked for validation.
    """
    return retrieve_all_summaries_to_be_validated()

def validate_categorization():
    """
    Validate the categorization of commits by comparing the predicted categories with the ground truth.
    This function loads the few-shots categorized commits, plots the categories, and calculates precision, recall, and accuracy.
    """
    data_filepath_few_shots = 'commits_few_shots.pkl'
    commits_few_shots = load_commits('commits/'+data_filepath_few_shots)

    plot_categories(commits_few_shots, "few_shots")
    plot_categories_pie_chart(commits_few_shots, "few_shots")

    p, r, a = calculate_precision_recall_categorization(commits_few_shots, ground_truth_array)
    print("<---- Few-shots categorization performance ---->")
    print(f"Precision: {p}")
    print(f"Recall: {r}")
    print(f"Accuracy: {a}")
    print("<-------------------- Done -------------------->")


def main():
    # Retrieve all the summaries that will be validated
    summaries = retrieve_summaries()

    if not summaries:
        print("Error: No summaries to validate.")
        return

def maino():
    validate_categorization()

if __name__ == "__main__":
    maino()