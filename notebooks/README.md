# Notebooks

This folder contains Jupyter notebooks used for data collection, preprocessing, and analysis for the fintech review analytics project.

## scraping_analysis.ipynb

### Task 1 Progress
Completed:
- Scraped Google Play Store reviews for:
  - CBE
  - BOA
  - Dashen Bank
- Collected:
  - Review text
  - Rating
  - Date
  - Bank name
  - Source
- Cleaned and preprocessed the dataset
- Removed duplicates and missing values
- Normalized dates to `YYYY-MM-DD`
- Saved cleaned data as CSV

### Task 2 Progress
Planned work:
- Perform sentiment analysis using VADER and DistilBERT
- Classify reviews as positive, negative, or neutral
- Extract keywords and themes using TF-IDF or spaCy
- Identify common issues and feature requests
- Create visualizations for sentiment and themes

### Technologies
- Python
- pandas
- google-play-scraper
- matplotlib
- seaborn
- nltk
- transformers
- scikit-learn
