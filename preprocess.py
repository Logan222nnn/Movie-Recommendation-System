# preprocess.py
import pandas as pd
import re
import nltk
import joblib
import logging
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("preprocess.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Starting preprocessing...")

nltk.download('punkt')

# Load and sample dataset
try:
    df = pd.read_csv("original_movies_data.csv")
    logging.info("Dataset loaded successfully. Total rows: %d", len(df))
except Exception as e:
    logging.error("Failed to load dataset: %s", str(e))
    raise e

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", str(text))
    text = text.lower()
    tokens = word_tokenize(text)
    return " ".join(tokens)


# filter the required columns for recommendation
required_columns = ["genres", "keywords", "overview", "title", "tagline"]

df = df[required_columns]

df = df.fillna('')

df['combined'] = df['genres'] + ' ' + df['keywords'] + ' ' + df['overview'] + ' ' + df['tagline']

logging.info("🧹 Cleaning text...")
df['cleaned_text'] = df['combined'].apply(preprocess_text)
logging.info("Text cleaned.")


# Vectorization
logging.info("🔠 Vectorizing using TF-IDF...")
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df['cleaned_text'])
logging.info("TF-IDF matrix shape: %s", tfidf_matrix.shape)

# Cosine similarity
logging.info("Calculating cosine similarity...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
logging.info("Cosine similarity matrix generated.")

# Save everything
joblib.dump(df, 'df_cleaned.pkl')
joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl')
joblib.dump(cosine_sim, 'cosine_sim.pkl')
logging.info("Data saved to disk.")

logging.info("Preprocessing complete.")