"""Load cleaned CSV reviews into the PostgreSQL `bank_reviews` database.

Usage:
  python -m scripts.load_reviews --csv data/bank_reviews_clean.csv

Environment variables used:
  PGHOST, PGPORT, PGUSER, PGPASSWORD
"""
import argparse
import pandas as pd
from sqlalchemy.orm import sessionmaker
from scripts.db_utils import get_engine
from scripts.models import Bank, Review


def parse_args():
    p = argparse.ArgumentParser(description="Load reviews CSV into DB")
    p.add_argument("--csv", default="data/bank_reviews_clean.csv",
                   help="Path to cleaned CSV")
    return p.parse_args()


def load(csv_path: str, chunk_size: int = 500):
    df = pd.read_csv(csv_path)
    engine = get_engine("bank_reviews")
    Session = sessionmaker(engine, future=True)
    session = Session()

    # preload existing banks
    bank_map = {b.name: b.id for b in session.query(Bank).all()}

    added = 0
    for idx, row in df.iterrows():
        bank_name = str(row.get("bank", "")).strip()
        if not bank_name:
            continue

        bank_id = bank_map.get(bank_name)
        if not bank_id:
            bank = Bank(name=bank_name, source=row.get("source"))
            session.add(bank)
            session.flush()
            bank_id = bank.id
            bank_map[bank_name] = bank_id

        # prepare review
        rating = None
        try:
            rating = int(row["rating"]) if pd.notna(
                row.get("rating")) else None
        except Exception:
            rating = None

        date_val = None
        try:
            date_val = pd.to_datetime(row.get("date")).date()
        except Exception:
            date_val = None

        review = Review(
            bank_id=bank_id,
            review=row.get("review", ""),
            rating=rating,
            date=date_val,
            source=row.get("source"),
        )
        session.add(review)
        added += 1

        if added % chunk_size == 0:
            session.commit()
            print(f"Inserted {added} reviews...")

    session.commit()
    session.close()
    print(f"Finished. Inserted {added} reviews into database.")


if __name__ == "__main__":
    args = parse_args()
    load(args.csv)
