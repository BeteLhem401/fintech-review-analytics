"""Create the `bank_reviews` PostgreSQL database and tables.

Usage:
  python -m scripts.create_db

Environment variables used:
  PGHOST, PGPORT, PGUSER, PGPASSWORD

"""
import argparse
from scripts.db_utils import create_database, get_engine
from scripts.models import Base


def main():
    parser = argparse.ArgumentParser(
        description="Create bank_reviews database and tables")
    parser.add_argument("--no-create-db", action="store_true",
                        help="Skip CREATE DATABASE step")
    args = parser.parse_args()

    if not args.no_create_db:
        create_database("bank_reviews")

    engine = get_engine("bank_reviews")
    Base.metadata.create_all(engine)
    print("Tables created (if not exists) in 'bank_reviews'.")


if __name__ == "__main__":
    main()
