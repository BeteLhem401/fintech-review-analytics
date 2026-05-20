import os
from urllib.parse import quote_plus

import psycopg2
from sqlalchemy import create_engine


def get_connection_params():
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "")
    return host, port, user, password


def get_db_url(db_name=None):
    host, port, user, password = get_connection_params()
    db = db_name or os.getenv("PGDATABASE", "bank_reviews")
    pwd = quote_plus(password) if password else ""
    if pwd:
        return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    return f"postgresql+psycopg2://{user}@{host}:{port}/{db}"


def get_engine(db_name=None, echo=False):
    url = get_db_url(db_name)
    return create_engine(url, echo=echo, future=True)


def create_database(db_name: str = "bank_reviews"):
    host, port, user, password = get_connection_params()
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone() is not None
        if not exists:
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"Created database '{db_name}'")
        else:
            print(f"Database '{db_name}' already exists")
        cur.close()
    finally:
        if conn:
            conn.close()
