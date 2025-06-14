ground_truth_array = [ "Dependency Update","Dependency Update",
  "Performance Improvement", "Performance Improvement", "Bug Fix", "Feature Update", "Bug Fix", "Performance Improvement", "Performance Improvement",
  "Bug Fix", "Bug Fix", "Feature Update", "Feature Update", "Refactoring", "Feature Update", "Bug Fix", "Feature Update", "Feature Update", "Feature Update",
  "Refactoring", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix", "Refactoring", "Bug Fix", "Feature Update", "Bug Fix", "Feature Update", "Feature Update",
  "Refactoring", "Feature Update", "Bug Fix", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix" ,"Bug Fix", "Feature Update", "Performance Improvement", "Bug Fix",
  "Bug Fix", "Bug Fix", "Build/CI Change", "Bug Fix", "Bug Fix", "Bug Fix", "Feature Update", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix", "Feature Update",
  "Other", "Bug Fix", "Bug Fix", "Refactoring", "Feature Update", "Bug Fix", "Feature Update", "Feature Update", "Performance Improvement", "Performance Improvement",
  "Feature Update", "Build/CI Change", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix",
  "Feature Update", "Performance Improvement", "Bug Fix", "Feature Update", "Feature Update", "Performance Improvement", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix", "Bug Fix",
  "Feature Update", "Feature Update", "Feature Update", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix", "Feature Update", "Bug Fix", "Bug Fix", "Bug Fix",
  "Feature Update", "Refactoring"
][::-1]

def calculate_precision_recall_categorization(commits, ground_truth):
  """
  Returns the precision and recall of the commits.
  Note that ground_truth is a list where ground_truth[i] is the category of the i-th commit.
  Should be handcrafted or GPT generated.
  """

  tp = 0
  tn = 0
  fp = 0
  fn = 0

  last_102_commits = len(commits) - 102
  #print(ground_truth)
  print("Commits:")

  for i, commit in commits.items():
    if i==0:
        print(commit)
    if i <= last_102_commits:
      continue

    predicted = commit['llama_category']
    actual = ground_truth[i-last_102_commits]
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