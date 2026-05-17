import pandas as pd
from transformers import pipeline

class SentimentAnalyzer:

    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def predict(self, text):
        if not text or str(text).strip() == "":
            return "NEUTRAL", 0.0

        result = self.model(str(text[:512]))[0]

        label = result["label"]
        score = result["score"]

        return label, score

    def analyze_dataframe(self, df, text_column="review"):
        labels = []
        scores = []

        for text in df[text_column]:
            label, score = self.predict(text)
            labels.append(label)
            scores.append(score)

        df["sentiment_label"] = labels
        df["sentiment_score"] = scores

        return df