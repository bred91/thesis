import matplotlib.pyplot as plt
from collections import defaultdict

def plot_categories(commits, shot_method):
    commit_counts = defaultdict(lambda: defaultdict(int))

    def get_quarter(date):
        month = date.month
        quarter_in = (month - 1) // 3 + 1  # Calculate the quarter (1 to 4)
        return f"{date.year}-Q{quarter_in}"

    for idx, commit in commits.items():
        if commit['llama_category'] == '':
            continue
        quarter = get_quarter(commit['date'])
        category = commit['llama_category']
        commit_counts[category][quarter] += 1

    categories = commit_counts.keys()
    quarters = sorted({quarter for category_data in commit_counts.values() for quarter in category_data})  # Sorted unique quarters

    plt.figure(figsize=(10, 6))
    for category in categories:
        counts = [commit_counts[category][quarter] if quarter in commit_counts[category] else 0 for quarter in quarters]
        plt.plot(quarters, counts, marker='o', label=category)

    plt.title('Commit Classification Over Time')
    plt.xlabel('Quarter')
    plt.ylabel('Number of Commits')
    plt.legend(title='Category for Llama')
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.tight_layout()

    # Show the plot
    plt.show()

    plt.savefig(f"plot_categories_{shot_method}.svg", format="svg")


def plot_categories_pie_chart(commits,shot_method):
    commit_counts = defaultdict(int)

    for idx, commit in commits.items():
        if commit['llama_category'] == '':
            continue
        category = commit['llama_category']
        commit_counts[category] += 1

    categories = list(commit_counts.keys())
    counts = [commit_counts[category] for category in categories]

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Commit Classification Pie Chart')
    plt.show()
    plt.savefig(f"plot_categories_pie_chart_{shot_method}.svg", format="svg")
