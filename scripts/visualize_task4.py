import logging
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

INPUT_PATH = Path("data") / "processed" / "sentiment_results.csv"
PLOTS_DIR = Path("plots")


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_results(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Processed data not found: {path}")

    return pd.read_csv(path, encoding="utf-8", encoding_errors="replace")


def save_figure(fig: plt.Figure, path: Path) -> None:
    ensure_directory(path.parent)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    LOGGER.info("Saved plot: %s", path)


def plot_sentiment_distribution_by_bank(df: pd.DataFrame) -> tuple[plt.Figure, Path]:
    table = df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)
    table = table.reindex(columns=[col for col in ["negative", "positive", "neutral"] if col in table.columns], fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 6))
    table.plot(kind="bar", stacked=True, ax=ax, color=["#d62728", "#2ca02c", "#7f7f7f"][: len(table.columns)])
    ax.set_title("Sentiment Distribution by Bank")
    ax.set_xlabel("Bank")
    ax.set_ylabel("Review Count")
    ax.legend(title="Sentiment")

    return fig, PLOTS_DIR / "sentiment_distribution_by_bank.png"


def plot_rating_distribution_by_bank(df: pd.DataFrame) -> tuple[plt.Figure, Path]:
    rating_df = df.copy()
    rating_df["rating"] = pd.to_numeric(rating_df["rating"], errors="coerce")
    rating_df = rating_df.dropna(subset=["rating"])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(
        data=rating_df,
        x="rating",
        hue="bank",
        ax=ax,
        palette="tab10",
        order=sorted(rating_df["rating"].unique()),
    )
    ax.set_title("Rating Distribution by Bank")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    ax.legend(title="Bank")

    return fig, PLOTS_DIR / "rating_distribution_by_bank.png"


def plot_theme_frequency_by_bank(df: pd.DataFrame) -> tuple[plt.Figure, Path]:
    theme_counts = df.groupby(["bank", "identified_theme"]).size().reset_index(name="count")
    top_themes = df["identified_theme"].value_counts().nlargest(10).index.tolist()
    theme_counts = theme_counts[theme_counts["identified_theme"].isin(top_themes)]

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(
        data=theme_counts,
        x="count",
        y="identified_theme",
        hue="bank",
        ax=ax,
        dodge=True,
    )
    ax.set_title("Theme Frequency by Bank")
    ax.set_xlabel("Count")
    ax.set_ylabel("Theme")
    ax.legend(title="Bank")

    return fig, PLOTS_DIR / "theme_frequency_by_bank.png"


def plot_top_themes_overall(df: pd.DataFrame) -> tuple[plt.Figure, Path]:
    counts = df["identified_theme"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index, palette="viridis", ax=ax)
    ax.set_title("Top 10 Themes Overall")
    ax.set_xlabel("Count")
    ax.set_ylabel("Theme")

    return fig, PLOTS_DIR / "top_10_themes_overall.png"


def most_negative_bank(df: pd.DataFrame) -> Optional[str]:
    summary = (
        df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)
        .assign(total=lambda x: x.sum(axis=1))
    )
    if "negative" not in summary.columns:
        return None
    summary["negative_pct"] = summary["negative"] / summary["total"]
    return summary["negative_pct"].idxmax()


def best_performing_bank(df: pd.DataFrame) -> Optional[str]:
    summary = (
        df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)
        .assign(total=lambda x: x.sum(axis=1))
    )
    if "positive" not in summary.columns:
        return None
    summary["positive_pct"] = summary["positive"] / summary["total"]
    return summary["positive_pct"].idxmax()


def most_common_complaint_theme(df: pd.DataFrame) -> Optional[str]:
    if "identified_theme" not in df.columns or df["identified_theme"].empty:
        return None
    return df["identified_theme"].mode().iloc[0]


def print_insights(df: pd.DataFrame) -> None:
    negative_bank = most_negative_bank(df)
    best_bank = best_performing_bank(df)
    common_theme = most_common_complaint_theme(df)

    print("Insights:\n")
    print(f"- Most negative bank: {negative_bank or 'N/A'}")
    print(f"- Most common complaint theme: {common_theme or 'N/A'}")
    print(f"- Best performing bank by sentiment: {best_bank or 'N/A'}")


def run_visualization() -> None:
    df = load_results(INPUT_PATH)
    ensure_directory(PLOTS_DIR)
    sns.set_theme(style="whitegrid")

    plot_functions = [
        plot_sentiment_distribution_by_bank,
        plot_rating_distribution_by_bank,
        plot_theme_frequency_by_bank,
        plot_top_themes_overall,
    ]

    for plot_func in plot_functions:
        fig, path = plot_func(df)
        save_figure(fig, path)

    print_insights(df)


if __name__ == "__main__":
    run_visualization()
