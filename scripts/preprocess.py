import pandas as pd

df = pd.read_csv("data/raw/bank_reviews_raw.csv")

# Remove duplicates
df = df.drop_duplicates()

# Remove missing values
df = df.dropna(subset=["review", "rating"])

# Normalize dates
df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

# Save cleaned data
df.to_csv("data/raw/bank_reviews_clean.csv", index=False)

print(df.info())
print(df.head())