import logging
import sys
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from scripts.sentiment_analysis import SentimentAnalyzer
from scripts.text_preprocessing import TextPreprocessor
from scripts.thematic_analysis import ThemeExtractor

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

RAW_CANDIDATES: List[Path] = [
    Path("data") / "raw" / "bank_reviews_raw.csv",
    Path("data") / "raw" / "bank_reviews_clean.csv",
    Path("data") / "bank_reviews_clean.csv",
    Path("scripts") / "bank_reviews_raw.csv",
    Path("scripts") / "bank_reviews_clean.csv",
]
OUTPUT_PATH = Path("data") / "processed" / "sentiment_results.csv"


def find_source_file() -> Path:
    for candidate in RAW_CANDIDATES:
        if candidate.exists():
            LOGGER.info("Using source file: %s", candidate)
            return candidate

    raise FileNotFoundError(
        "No source dataset found. Expected one of: "
        + ", ".join(str(candidate) for candidate in RAW_CANDIDATES)
    )


def load_data(source_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(
            source_path,
            encoding="utf-8",
            encoding_errors="replace",
            on_bad_lines="skip",
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to load data from {source_path}: {exc}") from exc


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.drop_duplicates().copy()
    df = df.dropna(subset=["review", "bank"])

    df["review"] = df["review"].astype(str).str.strip()
    df["bank"] = df["bank"].astype(str).str.strip()
    df["rating"] = pd.to_numeric(df.get("rating"), errors="coerce")
    df["date"] = pd.to_datetime(df.get("date"), errors="coerce").dt.strftime("%Y-%m-%d")

    return df


def ensure_output_path(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_results(df: pd.DataFrame, path: Path) -> None:
    ensure_output_path(path)
    df.to_csv(path, index=False, encoding="utf-8")
    LOGGER.info("Saved processed dataset to %s", path)


def run_pipeline() -> None:
    source_path = find_source_file()
    df = load_data(source_path)
    df = clean_reviews(df)

    if df.empty:
        raise RuntimeError("No valid reviews found after cleaning.")

    preprocessor = TextPreprocessor(lemmatize=True)
    df = preprocessor.process_dataframe(df, text_column="review", output_column="clean_review")

    sentiment = SentimentAnalyzer()
    df = sentiment.analyze_dataframe(df, text_column="clean_review")

    theme_extractor = ThemeExtractor()
    top_keywords = theme_extractor.extract_top_keywords(df["clean_review"].astype(str).tolist(), top_n=30)
    df = theme_extractor.process(df, text_column="clean_review", output_column="identified_theme")

    output_columns = [
        "review",
        "clean_review",
        "rating",
        "date",
        "bank",
        "source",
        "sentiment_label",
        "sentiment_score",
        "identified_theme",
    ]

    missing_columns = [col for col in output_columns if col not in df.columns]
    if missing_columns:
        raise RuntimeError(f"Missing required columns before save: {missing_columns}")

    save_results(df[output_columns], OUTPUT_PATH)
    LOGGER.info("Top keywords extracted: %s", ", ".join(top_keywords[:10]))


if __name__ == "__main__":
    run_pipeline()
