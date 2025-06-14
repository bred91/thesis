import os
import pickle


def full_path(data_filepath, name_file):
  path = os.path.join(data_filepath, f"commits_{name_file}.pkl")
  return path


def save_commits(commits, file_path):
    """
    Save commits to a file using pickle, creating directories if they do not exist.
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Now save the commits to the file
    with open(file_path, "wb") as file:
        pickle.dump(commits, file)
    #print(f"Commits saved to {file_path}")


def load_commits(file_path):
    """
    Load commits from a file if available.
    """
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return pickle.load(file)
    return None


def save_variable(variable, file_path):
    """
    Save a variable to a file using pickle, creating directories if they do not exist.

    :param variable: The variable to save.
    :param file_path: The path of the file to save the variable to.
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Now save the variable to the file
    with open(file_path, "wb") as file:
        pickle.dump(variable, file)
    print(f"Variable saved to {file_path}")