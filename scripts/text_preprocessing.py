import re
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

class TextPreprocessor:

    def __init__(self):
        pass

    def clean_text(self, text):
        if pd.isna(text):
            return ""

        text = str(text).lower()
        text = re.sub(r"[^a-zA-Z\s]", "", text)

        doc = nlp(text)

        tokens = [
            token.lemma_
            for token in doc
            if not token.is_stop and token.is_alpha
        ]

        return " ".join(tokens)

    def process_dataframe(self, df, text_column="review"):
        df[text_column] = df[text_column].apply(self.clean_text)
        return df