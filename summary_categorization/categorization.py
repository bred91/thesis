import logging

from utils.config import SEED
from utils.llm_utils import clean_text_paragraph

logger = logging.getLogger("DBLogger")
logger.setLevel(logging.DEBUG)

CATEGORIES = [
    "Feature Update",
    "Bug Fix",
    "Documentation Update",
    "Refactoring",
    "Performance Improvement",
    "Test Addition/Update",
    "Dependency Update",
    "Build/CI Change",
    "Style Update",
    "Other"
]

categories_text = '\n'.join([f"{i + 1}. {category}" for i, category in enumerate(CATEGORIES)])

def generate_prompt_categorization_few_shots(commit):
    """
    Generate a prompt for categorizing a Git commit.
    """

    prompt = f"""
    You are tasked with categorizing commits based on their purpose and significance. Use the following categories:

      {categories_text}

      Each commit has the following details:
      - **Commit Informations:**
        - **Hash (unique identifier):**
        - **Author (person who did the commit)**
        - **Date(date in which the commit was done)**
        - **Commit Message (breif explanation of what’s been changed inside the commit)**
        - **Changed Files: (list of files affected from the commit)*
        - **Diffs (Lines of code changed in each file)**

      **Instructions:**
      1. Review the commit information carefully, including the message, modified files, and code diffs.
      2. Classify the commit into one of the provided categories.
      3. Provide a single category from the list based on the purpose and significance of the changes.

      **Example 1 :**

      Commit Informations:
      - Hash (unique identifier): 1a2b3c4d
      - Author: John Doe
      - Date: 2025-01-01 10:00:00
      - Commit Message: Refactored the user authentication module to improve performance and readability.
      - Changed Files: auth.py, user_model.py
      - Diffs:
        auth.py:
        ```diff
        - def authenticate_user(username, password):
        -     if username and password:
        -         return check_credentials(username, password)
        + def authenticate_user(user_credentials):
        +     return validate_user(user_credentials)
      user_model.py:
      + def validate_user(credentials):
      +     # New validation logic for login
      +     return is_valid(credentials)
      **category**: Refactoring

      **Example 2 :**
      Commit Informations:
      - Hash (unique identifier): 3c2b1a4f
      - Author: Alex Brown
      - Date: 2025-01-03 12:00:00
      - Commit Message: Updated the README with installation instructions and new feature descriptions.
      - Changed Files: README.md
      - Diffs:
      README.md:
      ```diff
      + ## Installation
      + Run the following command to install:
      + pip install mypackage
      **category**: Documentation Update

      **Example 3 : **
      Commit Informations:
      - Hash (unique identifier): 9f8e7d6c
      - Author: Jane Smith
      - Date: 2025-01-02 15:00:00
      - Commit Message: Fixed incorrect handling of null values in user profile updates.
      - Changed Files: profile.py
      - Diffs:
      profile.py:
      ```diff
      - if user['name']:
      + if user.get('name') is not None:
      **category**: Bug Fix


      Now, analyze the following commit:

      Commit Informations:

      Hash (unique identifier): {commit['hash']}
      Author: {commit['author']}
      Date: {commit['date'].strftime('%Y-%m-%d %H:%M:%S')}
      Commit Message: {commit['message']}
      Changed Files: {', '.join(commit['files'])}
      Diffs: {chr(10).join([f"{file_name}: {diff[:1000]}" for file_name, diff in commit['diffs'].items()])}
      Provide the category based on the purpose and significance of the commit.
      Category:

    """

    prompt = clean_text_paragraph(prompt)
    return prompt


def refine_answer(answer):
    """
    Ensure the answer contains only the category name.
    """

    for category in CATEGORIES:
        if category.lower() in answer.lower():
            return category
    return "Other"


def ask_model_categorization(prompt, ollama_client, model):
    """
    Ask the Ollama model to categorize a git commit.

    Args:
        prompt (str): The input prompt for the model.
        ollama_client: The Ollama client instance.
        model (str): The model name to use (e.g., "llama3").
    """
    response = ollama_client.generate(
        model=model,
        prompt=prompt,
        options={
            "num_predict": 20,      # Maximum number of tokens to generate
            "temperature": 0,       # Deterministic output
            "top_p": 0.8,             # Nucleus sampling: 1 = no restriction
            "seed": SEED,            # Fixed seed for reproducibility
        },
    )
    answer = response['response'].split("Category:")[-1]
    return refine_answer(answer)


def categorize(commit, idx, llama_model, ollama_client):
    logger.debug(f"Categorizing commit {idx}")
    prompt = generate_prompt_categorization_few_shots(commit)
    commit['llama_category'] = ask_model_categorization(prompt, ollama_client, llama_model)