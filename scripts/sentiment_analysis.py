import logging
from typing import Tuple

import pandas as pd
from transformers import Pipeline, pipeline

LOGGER = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        self.model: Pipeline = pipeline("sentiment-analysis", model=self.model_name)

    def predict(self, text: str) -> Tuple[str, float]:
        if text is None or str(text).strip() == "":
            return "neutral", 0.0

        result = self.model(str(text)[:512])[0]
        label = str(result.get("label", "neutral")).lower()
        score = float(result.get("score", 0.0))

        if label not in {"positive", "negative"}:
            label = "neutral"

        return label, score

    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = "clean_review") -> pd.DataFrame:
        if text_column not in df.columns:
            raise ValueError(f"Expected text column '{text_column}' in DataFrame")

        labels = []
        scores = []
        for text in df[text_column].astype(str).fillna(""):
            label, score = self.predict(text)
            labels.append(label)
            scores.append(score)

        df["sentiment_label"] = labels
        df["sentiment_score"] = scores
        LOGGER.info("Completed sentiment analysis for %d rows", len(df))
        return df
