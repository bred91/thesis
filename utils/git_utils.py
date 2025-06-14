from git import Repo

def extract_git_commits(repo_path, branch='master'):
    """
    Extracts commit information from a Git repository.
    """
    repo = Repo(repo_path)
    commits = list(repo.iter_commits(branch))
    commits_dict = {}

    commits.reverse()

    for i, commit in enumerate(commits):
        commits_dict[i] = {
            'hash': commit.hexsha,
            'author': f"{commit.author.name} <{commit.author.email}>",
            'date': commit.authored_datetime,
            'message': commit.message.strip(),
            'files': list(commit.stats.files.keys()),
            'diffs': {},
            'llama_summary': '',
            'llama_category': '',
            'llama_tech_summary': ''
        }

        diffs = commit.diff(commit.parents[0] if commit.parents else None, create_patch=True)

        for diff in diffs:
            file_diff = diff.diff.decode('utf-8')
            file_name = f"{diff.a_path} -> {diff.b_path}" if diff.a_path != diff.b_path else diff.a_path
            commits_dict[i]['diffs'][file_name] = filter_diff_lines(file_diff)

    print(f"Extracted {len(commits_dict)} commits")
    return commits_dict

def filter_diff_lines(diff_text):
    """
    Filtra le righe di un diff Git, mantenendo solo quelle che iniziano con '+' o '-',
    escludendo le intestazioni dei file ('+++', '---').

    Args:
        diff_text (str): Il testo del diff Git.

    Returns:
        str: Le righe filtrate del diff.
    """
    filtered_lines = []
    for line in diff_text.splitlines():
        # Include lines that start with '+' or '-' but exclude '+++' or '---'
        if (line.startswith('+') or line.startswith('-')) and not line.startswith('+++') and not line.startswith('---'):
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)