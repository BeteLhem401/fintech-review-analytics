-- Schema for bank_reviews database

CREATE TABLE IF NOT EXISTS banks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    source VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(id) ON DELETE CASCADE,
    review TEXT NOT NULL,
    rating INTEGER,
    date DATE,
    source VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
