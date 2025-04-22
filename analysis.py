import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

LOG_FILE = "logs/solver_log.csv"


def load_log():
    if not os.path.exists(LOG_FILE):
        raise FileNotFoundError(f"Log file not found: {LOG_FILE}")
    return pd.read_csv(LOG_FILE)


def plot_runtime_by_solver(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="solver", y="runtime_sec", hue="status")
    plt.title("Runtime by Solver")
    plt.ylabel("Runtime (seconds)")
    plt.xlabel("Solver")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_success_rate(df):
    success_map = df["assignment_found"] == "Yes"
    success_rates = df.groupby("solver")["assignment_found"].apply(lambda x: (x == "Yes").mean()).reset_index(name="success_rate")
    plt.figure(figsize=(8, 5))
    sns.barplot(data=success_rates, x="solver", y="success_rate")
    plt.title("Success Rate by Solver")
    plt.ylim(0, 1)
    plt.ylabel("Success Rate")
    plt.tight_layout()
    plt.show()


def plot_runtime_vs_ratio(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="clause_var_ratio", y="runtime_sec", hue="solver", style="assignment_found")
    plt.title("Runtime vs Clause-to-Variable Ratio")
    plt.xlabel("Clause-to-Variable Ratio")
    plt.ylabel("Runtime (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def run_all():
    df = load_log()
    print("\nSummary Stats:\n", df.groupby("solver")["runtime_sec"].describe())
    plot_runtime_by_solver(df)
    plot_success_rate(df)
    plot_runtime_vs_ratio(df)


if __name__ == "__main__":
    run_all()