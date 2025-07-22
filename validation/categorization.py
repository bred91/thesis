from utils.file_utils import load_commits
from utils.plot_utils import plot_categories, plot_categories_pie_chart

ground_truth_array = [  # "Dependency Update","Dependency Update",
                         "Performance Improvement", "Performance Improvement", "Bug Fix", "Feature Update", "Bug Fix",
                         "Performance Improvement", "Performance Improvement",
                         "Bug Fix", "Bug Fix", "Feature Update", "Feature Update", "Refactoring", "Feature Update",
                         "Bug Fix", "Feature Update", "Feature Update", "Feature Update",
                         "Refactoring", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix", "Refactoring", "Bug Fix",
                         "Feature Update", "Bug Fix", "Feature Update", "Feature Update",
                         "Refactoring", "Feature Update", "Bug Fix", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix",
                         "Bug Fix", "Feature Update", "Performance Improvement", "Bug Fix",
                         "Bug Fix", "Bug Fix", "Build/CI Change", "Bug Fix", "Bug Fix", "Bug Fix", "Feature Update",
                         "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix", "Feature Update",
                         "Other", "Bug Fix", "Bug Fix", "Refactoring", "Feature Update", "Bug Fix", "Feature Update",
                         "Feature Update", "Performance Improvement", "Performance Improvement",
                         "Feature Update", "Build/CI Change", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix",
                         "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix",
                         "Feature Update", "Performance Improvement", "Bug Fix", "Feature Update", "Feature Update",
                         "Performance Improvement", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix",
                         "Feature Update", "Feature Update", "Feature Update", "Bug Fix", "Feature Update", "Bug Fix",
                         "Bug Fix", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix",
                         "Feature Update", "Refactoring"
                     ][::-1]


def calculate_precision_recall_categorization(commits, ground_truth, verbose=False):
    """
    Returns the precision and recall of the commits.
    Note that ground_truth is a list where ground_truth[i] is the category of the i-th commit.
    Should be handcrafted or GPT generated.
    """

    tp = tn = fp = fn = 0
    baseline = 480
    delta = 100
    eval_keys = [k for k in commits.keys() if baseline <= k < baseline + delta]
    eval_commits = [commits[k] for k in eval_keys]

    # print(ground_truth)
    if verbose:
        print("Commits:")

    for i, commit in enumerate(eval_commits):
        predicted = commit['llama_category']
        actual = ground_truth[i]

        if verbose:
            print(f"Commit {i}: Predicted: {predicted}, Actual: {actual}")

            if predicted != actual:
                print(commit)

        if predicted == actual:
            if predicted == 'Other':
                tn += 1
            else:
                tp += 1
        else:
            if predicted == 'Other':
                fn += 1
            else:
                fp += 1

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0

    return precision, recall, accuracy


def validate_categorization():
    """
    Validate the categorization of commits by comparing the predicted categories with the ground truth.
    This function loads the few-shots categorized commits, plots the categories, and calculates precision, recall, and accuracy.
    """
    data_filepath_few_shots = 'commits_few_shots.pkl'
    commits_few_shots = load_commits('commits/' + data_filepath_few_shots)

    plot_categories(commits_few_shots, "few_shots")
    plot_categories_pie_chart(commits_few_shots, "few_shots")

    p, r, a = calculate_precision_recall_categorization(commits_few_shots, ground_truth_array)
    print("<---- Few-shots categorization performance ---->")
    print(f"Precision: {p}")
    print(f"Recall: {r}")
    print(f"Accuracy: {a}")
    print("<-------------------- Done -------------------->")
