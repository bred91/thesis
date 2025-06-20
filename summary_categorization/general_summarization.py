import logging

from langchain_core.documents import Document

from utils.chromadb_utils import format_retrieved_docs, retrieve_top_commits_by_summary_type
from utils.config import SEED
from utils.enums import SummaryType
from utils.llm_utils import clean_text_paragraph

logger = logging.getLogger("DBLogger")
logger.setLevel(logging.DEBUG)


def generate_prompt_summarization_few_shots(commit):
    prompt = f"""
        You are a helpful assistant. Provide a concise description of what has been done in the following commits.

        Example 1:
        Commit Informations:
        - Hash (unique identifier): 1a2b3c4d
        - Author: John Doe
        - Date: 2025-01-01 10:00:00
        Commit Message - this provides a brief summary of the changes:
        Refactored the user authentication module to improve performance and readability.
        Changed Files - files modified in this commit:
        auth.py, user_model.py
        Diffs - lines of code changed in each file:
        auth.py:
        ```diff
        - def authenticate_user(username, password):
        -     if username and password:
        -         return check_credentials(username, password)
        + def authenticate_user(user_credentials):
        +     return validate_user(user_credentials)
        ```
        user_model.py:
        ```diff
        + def validate_user(credentials):
        +     # New validation logic for login
        +     return is_valid(credentials)
        ```
        Answer:
        Refactored the user authentication system to improve both performance and readability.
        Key changes include replacing the `authenticate_user` function to accept a `user_credentials` object instead of separate username and password arguments, simplifying the interface and making the code less error-prone.
        Additionally, a new `validate_user` function was introduced in `user_model.py` to centralize login validation logic, improving modularity and enabling easier future updates.
        These changes make the authentication process more robust and align with modern software design principles.

        Example 2:
        Commit Informations:
        - Hash (unique identifier): 5e6f7g8h
        - Author: Jane Smith
        - Date: 2025-01-02 14:30:00
        Commit Message - this provides a brief summary of the changes:
        Added a new feature for exporting reports to CSV.
        Changed Files - files modified in this commit:
        report_exporter.py, utils/csv_writer.py
        Diffs - lines of code changed in each file:
        report_exporter.py:
        ```diff
        + def export_to_csv(data, filename):
        +     with open(filename, 'w') as file:
        +         writer = csv.writer(file)
        +         writer.writerow(data.keys())
        +         writer.writerows(data.values())
        ```
        utils/csv_writer.py:
        ```diff
        + import csv
        ```
        Answer:
        Added a new feature for exporting reports to CSV format, enabling users to easily extract structured data.
        Key changes include introducing the `export_to_csv` function in `report_exporter.py`, which uses Python’s built-in CSV library to create files with appropriate headers and rows based on the input data.
        The `utils/csv_writer.py` module was also updated to include CSV-related utilities, promoting code reuse and reducing duplication across the project.
        This enhancement significantly improves the usability of the reporting system, particularly for end users who need seamless integration with external tools like Excel.

        Example 3:
        Commit Informations:
        - Hash (unique identifier): b2c4d6e8
        - Author: Alice Brown
        - Date: 2024-03-15 16:42:10
        Commit Message - this provides a brief summary of the changes:
        Fixed scope handling for function declarations in JavaScript compilation.
        Changed Files - files modified in this commit:
        jscompiler.c
        Diffs - lines of code changed in each file:
        jscompiler.c:
        ```diff
        - static void compile_function_body(JF, js_Ast *name, js_Ast *params, js_Ast *body, int is_fun_exp);
        + static void compile_function_body(JF, js_Ast *name, js_Ast *params, js_Ast *body);
        - static js_Function *create_function(js_State *J, int line, js_Ast *name, js_Ast *params, js_Ast *body, int script, int strict, int is_fun_exp);
        + static js_Function *create_function(js_State *J, int line, js_Ast *name, js_Ast *params, js_Ast *body, int script, int strict);
        ```
        Answer:
        Addressed an issue with scope handling for function declarations in the JavaScript compiler.
        The key change involved removing the `is_fun_exp` parameter from the `compile_function_body` and `create_function` methods, simplifying the handling of function declaration bindings.
        This improves code clarity and correctness, ensuring that function declarations adhere to the expected scope rules.
        These updates pave the way for further improvements, such as making function expression bindings immutable, which aligns with the long-term goals for the compiler's behavior.


        Now analyze the following commit:

        Commit Informations:
        - Hash (unique identifier): {commit['hash']}
        - Author: {commit['author']}
        - Date: {commit['date'].strftime('%Y-%m-%d %H:%M:%S')}
        Commit Message - this provides a brief summary of the changes:
        {commit['message']}
        Changed Files - files modified in this commit:
        {', '.join(commit['files'])}
        Diffs - lines of code changed in each file:
        {chr(10).join([f"{file_name}: {diff[:1000]}" for file_name, diff in commit['diffs'].items()])}

        Use all the informations available to analyze the changes focusing on the purpose, key changes, and significance.
        Exclude unnecessary technical details and make it easy to understand for a project manager or developer.

        Do not repeat the prompt. Do no repeat any of the information provided above. Do not include lines of code
        Answer:
    """
    prompt = clean_text_paragraph(prompt)
    return prompt


def ask_model_summarization(prompt, ollama_client, model):
    """
    Ask the Ollama model to summarize a git commit.

    Args:
        prompt (str): The input prompt for the model.
        ollama_client: The Ollama client instance.
        model (str): The model name to use (e.g., "llama3").
    """
    response = ollama_client.generate(
        model=model,
        prompt=prompt,
        options={
            "num_predict": 200,      # Maximum number of tokens to generate
            "temperature": 0,
            "top_p": 1,              # Nucleus sampling: 1 = no restriction, <1 = only most probable tokens
            "seed": SEED,
        }
    )
    answer = response['response'].split("Answer:")[-1]
    return answer

def generate_general_summary(commit, idx, llama_model, ollama_client) -> list[tuple[Document, float]]:
    """
    Generate a general summary for a git commit using the LLM.
    This function retrieves similar commits from the database and uses them to enhance the summary generation.

    Args:
        commit (dict): The commit data containing information like hash, author, date, message, files, and diffs.
        idx (int): The index of the commit in the dataset.
        llama_model (str): The name of the LLM model to use for summarization.
        ollama_client: The Ollama client instance for interacting with the model.

    Returns:
        list[tuple[Document, float]]: A list of tuples containing retrieved documents and their relevance scores.
    """

    logger.debug(f"Summarizing (General) commit {idx}")
    prompt = generate_prompt_summarization_few_shots(commit)
    summary_retrieved_docs: list[tuple[Document, float]] = (
        retrieve_top_commits_by_summary_type(prompt, SummaryType.GENERAL, n_results=3))

    if summary_retrieved_docs:
        logger.debug(
            f"Retrieved {len(summary_retrieved_docs)} docs for commit {idx}: {''.join(format_retrieved_docs(summary_retrieved_docs))}")
        prompt += "\n\nPrevious similar commits:\n" + "\n".join([doc[0].page_content for doc in summary_retrieved_docs])
    else:
        logger.debug(f"No similar commits found for commit {idx}")

    commit['llama_summary'] = ask_model_summarization(prompt, ollama_client, llama_model)
    return summary_retrieved_docs