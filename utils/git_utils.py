import datetime
import glob
import os

from git import Repo

from utils.config import MUJS_DOCS_LOCAL_PATH, MUJS_BRANCH


def extract_git_commits(repo_path, branch=MUJS_BRANCH):
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

        diffs = commit.diff(commit.parents[0] if commit.parents else None, create_patch=True, R=True)

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


def extract_mujs_docs() -> list[dict]:
    """
    Extracts documentation from MuJS HTML files.
    Reads all HTML files in the mujs/docs directory and extracts the text content.
    and extracts the text content.

    Returns:
        list: A list of dictionaries containing the filename and content of each document.
    """
    docs = []
    pattern = os.path.join(os.path.dirname(os.path.dirname(__file__)), MUJS_DOCS_LOCAL_PATH, '*.html')
    abs_pattern = os.path.abspath(pattern)
    files = glob.glob(abs_pattern)

    if not files:
        print('No HTML files found. Check MUJS_DOCS_LOCAL_PATH:', MUJS_DOCS_LOCAL_PATH)

    for file in files:
        with open(file, encoding='utf-8') as f:
            html = f.read()
            docs.append(
                {
                    'filename': os.path.basename(file),
                    'insert_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'content': html
                }
            )
    return docs


def format_code(doc):
    """
    Formats a code document to include path and a snippet of the content.

    Args:
        doc (Document): The document containing code content.

    Returns:
        str: A formatted string with the file path and a snippet of the content.
    """
    path = doc.metadata.get("file_path", "<unknown>")
    content = doc.page_content.strip()
    snippet = content[:10000] + ("..." if len(content) > 1000 else "")

    return f"FILE: {path}\n---\n{snippet}"