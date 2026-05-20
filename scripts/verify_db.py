"""Run verification SQL queries against the `bank_reviews` database."""
from scripts.db_utils import get_engine


def run_checks():
    engine = get_engine("bank_reviews")
    with engine.connect() as conn:
        print("-- Counts --")
        res = conn.execute("SELECT COUNT(*) FROM banks")
        print("banks:", res.scalar())
        res = conn.execute("SELECT COUNT(*) FROM reviews")
        print("reviews:", res.scalar())

        print("\n-- Top banks by review count --")
        rows = conn.execute(
            "SELECT b.name, COUNT(r.*) AS cnt FROM banks b JOIN reviews r ON b.id = r.bank_id GROUP BY b.id ORDER BY cnt DESC LIMIT 10"
        )
        for name, cnt in rows:
            print(f"{name}: {cnt}")

        print("\n-- Sample reviews --")
        samples = conn.execute(
            "SELECT r.id, b.name, r.rating, r.date, substring(r.review,1,120) FROM reviews r JOIN banks b ON b.id = r.bank_id ORDER BY r.id DESC LIMIT 10")
        for row in samples:
            print(row)


if __name__ == "__main__":
    run_checks()
