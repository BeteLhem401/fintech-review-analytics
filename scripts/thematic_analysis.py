import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class ThemeExtractor:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1,2),
            max_features=50
        )

        self.themes = {
            "Account Access Issues": ["login", "password", "otp", "access"],
            "Transaction Performance": ["transfer", "slow", "delay", "payment"],
            "UI & Design": ["ui", "interface", "design", "easy"],
            "Customer Support": ["support", "help", "response", "service"],
            "Feature Requests": ["feature", "add", "fingerprint", "update"]
        }

    def extract_keywords(self, texts):
        X = self.vectorizer.fit_transform(texts)
        return self.vectorizer.get_feature_names_out()

    def assign_theme(self, text):

        text = str(text).lower()

        for theme, keywords in self.themes.items():
            for kw in keywords:
                if kw in text:
                    return theme

        return "Other"

    def process(self, df, text_column="review"):
        df["identified_theme"] = df[text_column].apply(self.assign_theme)
        return df