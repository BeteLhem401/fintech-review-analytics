# Fintech Review Analytics

This project analyzes customer reviews from Google Play Store for three major Ethiopian banks:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The goal is to scrape reviews, preprocess the data, perform sentiment and thematic analysis, and generate business insights.

---

## 🚀 Project Setup

1. Clone the repository:

   ````bash
   git clone https://github.com/BeteLhem401/fintech-review-analytics.git
   cd fintech-review-analytics

   ## PostgreSQL Setup (Task 3)

   This project can load the cleaned reviews CSV into a PostgreSQL database named `bank_reviews`.

   Prerequisites:
   - Install PostgreSQL and ensure the server is running.
   - Python dependencies: install from `requirements.txt`.

   1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ````

   2. Configure database connection using environment variables (examples):
   - Linux / macOS (bash):

   ```bash
   export PGHOST=localhost
   export PGPORT=5432
   export PGUSER=postgres
   export PGPASSWORD=your_password
   ```

   - Windows (PowerShell):

   ```powershell
   $env:PGHOST = 'localhost'
   $env:PGPORT = '5432'
   $env:PGUSER = 'postgres'
   $env:PGPASSWORD = 'your_password'
   ```

   3. Create the `bank_reviews` database and tables:

   ```bash
   python -m scripts.create_db
   ```

   4. Load the cleaned CSV into the database (default path used):

   ```bash
   python -m scripts.load_reviews --csv data/bank_reviews_clean.csv
   ```

   5. Run verification queries:

   ```bash
   python -m scripts.verify_db
   ```

  
