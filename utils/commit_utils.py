import re

def filter_trivial_commits(commits_dict, trivial_patterns=None, min_diff_lines=5):
    """
    Filters out trivial commits based on patterns and diff size.
    To add a new trivial pattern, add it to the trivial_patterns list below.
    """

    if trivial_patterns is None:
        trivial_patterns = [
            r"merge branch",        # Merging branches
            r"fix typo",            # Fixing typos
            r"readme",              # Updating documentation
            r"minor",               # General minor changes
            r"release"              # Release versions
            r"cleanup"              # Cleanups
        ]

    filtered_commits = {}
    filtered_number = 0

    for index, commit in commits_dict.items():
        # Check commit message for trivial patterns
        if any(re.search(pattern, commit['message'], re.IGNORECASE) for pattern in trivial_patterns):
            filtered_number += 1
            continue

        # Check diff size (number of lines changed)
        total_diff_lines = sum(len(diff.splitlines()) for diff in commit['diffs'].values())
        if total_diff_lines < min_diff_lines:
            filtered_number += 1
            continue

        # If commit passes all filters, include it
        filtered_commits[index] = commit

    print(f"Filtered {filtered_number} commits")
    return filtered_commits


def normalize_commit_data(commit_data):
    """
    Normalize all commit messages in a dictionary of git data.
    """

    def normalize_message(message):
        """
        Normalize a single git commit message.
        """
        # Remove leading/trailing whitespace and ensure capitalization
        normalized = message.strip().capitalize()

        # Replace multiple spaces or tabs with a single space
        normalized = re.sub(
          r'\s+', ' ', normalized)

        # Remove repetitive or excessive comments like "!!!!!" or "..."
        normalized = re.sub(r'[!?.]{2,}', '.', normalized)

        # Eliminate redundant phrases or filler words
        redundant_phrases = [
            r"\bthis commit\b", r"\bminor fix\b", r"\bsmall update\b",
            r"\bquick fix\b", r"\btemporary change\b", r"\btest commit\b"
        ]
        for phrase in redundant_phrases:
            normalized = re.sub(phrase, '', normalized, flags=re.IGNORECASE).strip()

        # Simplify common patterns
        normalized = re.sub(r'\bAdded\b', 'Add', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'\bRemoved\b', 'Remove', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'\bFixed\b', 'Fix', normalized, flags=re.IGNORECASE)

        # Standardize specific keywords
        normalized = re.sub(r'\bBugfix\b', 'Bug fix', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'\bRefactored\b', 'Refactor', normalized, flags=re.IGNORECASE)

        # Ensure the message ends with a period if it doesn't already
        if not normalized.endswith('.'):
            normalized += '.'

        return normalized

    # Iterate through each commit and normalize the message
    for index, commit in commit_data.items():
        if "message" in commit:
            commit["message"] = normalize_message(commit["message"])

    print("Normalize commits done")
    return commit_data

