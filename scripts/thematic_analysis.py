import logging
from typing import Dict, List, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

LOGGER = logging.getLogger(__name__)

DEFAULT_THEMES: Dict[str, List[str]] = {
    "login issues": [
        "login",
        "password",
        "otp",
        "access",
        "signin",
        "sign in",
        "sign-in",
        "unlock",
    ],
    "transaction problems": [
        "transfer",
        "payment",
        "transaction",
        "withdraw",
        "deposit",
        "failed",
        "declined",
        "charge",
        "refund",
        "balance",
    ],
    "ui/ux feedback": [
        "ui",
        "interface",
        "design",
        "layout",
        "experience",
        "navigation",
        "confusing",
        "hard",
        "easy",
        "button",
    ],
    "performance issues": [
        "slow",
        "lag",
        "freeze",
        "crash",
        "timeout",
        "loading",
        "delay",
        "buffer",
    ],
    "customer support": [
        "support",
        "help",
        "service",
        "response",
        "agent",
        "call",
        "ticket",
        "complaint",
        "care",
    ],
}


class ThemeExtractor:
    def __init__(
        self,
        ngram_range: tuple = (1, 3),
        max_features: int = 100,
        themes: Optional[Dict[str, List[str]]] = None,
    ):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=ngram_range,
            max_features=max_features,
        )
        self.themes = themes or DEFAULT_THEMES

    def extract_top_keywords(self, texts: List[str], top_n: int = 20) -> List[str]:
        cleaned_texts = [str(text) for text in texts if text is not None]
        if not cleaned_texts:
            return []

        matrix = self.vectorizer.fit_transform(cleaned_texts)
        scores = matrix.mean(axis=0).A1
        features = self.vectorizer.get_feature_names_out()
        keyword_scores = sorted(
            zip(features, scores), key=lambda pair: pair[1], reverse=True
        )
        top_keywords = [keyword for keyword, _ in keyword_scores[:top_n]]
        LOGGER.info("Extracted top keywords: %s", top_keywords[:10])
        return top_keywords

    def assign_theme(self, text: Optional[str]) -> str:
        text_value = str(text).lower() if text is not None else ""
        for theme, keywords in self.themes.items():
            for keyword in keywords:
                if keyword in text_value:
                    return theme
        return "other"

    def process(
        self,
        df: pd.DataFrame,
        text_column: str = "clean_review",
        output_column: str = "identified_theme",
    ) -> pd.DataFrame:
        if text_column not in df.columns:
            raise ValueError(f"Expected text column '{text_column}' in DataFrame")

        df[output_column] = df[text_column].apply(self.assign_theme)
        LOGGER.info("Assigned themes for %d rows", len(df))
        return df
