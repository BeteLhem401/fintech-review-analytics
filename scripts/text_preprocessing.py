import logging
import re
from typing import Optional

import pandas as pd

try:
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS as SPACY_STOP_WORDS
    _SPACY_AVAILABLE = True
except ImportError:  # pragma: no cover
    spacy = None
    SPACY_STOP_WORDS = set()
    _SPACY_AVAILABLE = False

LOGGER = logging.getLogger(__name__)
DEFAULT_EXTRA_STOPWORDS = {
    "app",
    "bank",
    "banks",
    "review",
    "reviews",
    "use",
    "used",
    "using",
    "please",
    "also",
}


class TextPreprocessor:
    def __init__(self, lemmatize: bool = True):
        self.lemmatize = lemmatize and _SPACY_AVAILABLE
        self.stopwords = set(SPACY_STOP_WORDS).union(DEFAULT_EXTRA_STOPWORDS)
        self.nlp = None

        if self.lemmatize:
            try:
                self.nlp = spacy.load("en_core_web_sm", exclude=["parser", "ner"])
            except Exception as exc:
                LOGGER.warning("spaCy model load failed: %s. Falling back to token-only preprocessing.", exc)
                self.lemmatize = False
                self.nlp = None

    def clean_text(self, text: Optional[str]) -> str:
        if text is None or pd.isna(text):
            return ""

        text = str(text).lower()
        text = re.sub(r"[^a-z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        if self.lemmatize and self.nlp:
            doc = self.nlp(text)
            tokens = [
                token.lemma_.strip()
                for token in doc
                if token.is_alpha and not token.is_stop and token.lemma_.strip() not in self.stopwords
            ]
        else:
            tokens = [
                token
                for token in text.split()
                if token not in self.stopwords and len(token) > 1
            ]

        cleaned = " ".join(tokens)
        return cleaned

    def process_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str = "review",
        output_column: str = "clean_review",
    ) -> pd.DataFrame:
        if text_column not in df.columns:
            raise ValueError(f"Expected text column '{text_column}' in DataFrame")

        df[output_column] = df[text_column].apply(self.clean_text)
        LOGGER.info("Completed text preprocessing for %d rows", len(df))
        return df
