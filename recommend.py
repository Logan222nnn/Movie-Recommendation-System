# recommend.py
import joblib
import logging
import pandas as pd
import requests
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Hugging Face model URLs
MODEL_FILES = {
    'df_cleaned.pkl': "https://huggingface.co/sankarans2001/Movie-Recommendation-System/resolve/main/df_cleaned.pkl?download=true",
    'cosine_sim.pkl': "https://huggingface.co/sankarans2001/Movie-Recommendation-System/resolve/main/cosine_sim.pkl?download=true"
}

def download_model_file(filename, url):
    """Download model file from Hugging Face if not exists locally"""
    if not os.path.exists(filename):
        logging.info(f"📥 Downloading {filename} from Hugging Face...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logging.info(f"✅ {filename} downloaded successfully")
        except Exception as e:
            logging.error(f"❌ Failed to download {filename}: {str(e)}")
            raise e
    else:
        logging.info(f"✅ {filename} already exists locally")

logging.info("🔁 Loading data...")
try:
    # Download model files from Hugging Face if needed
    for filename, url in MODEL_FILES.items():
        download_model_file(filename, url)
    
    # Load the models
    df = joblib.load('df_cleaned.pkl')
    cosine_sim = joblib.load('cosine_sim.pkl')
    
    logging.info("✅ Data loaded successfully.")
except Exception as e:
    logging.error("❌ Failed to load required files: %s", str(e))
    raise e

# Your existing function stays the same
def recommend_movies(movie_name, top_n=5):
    logging.info("🎬 Recommending movies for: '%s'", movie_name)
    idx = df[df['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        logging.warning("⚠️ Movie not found in dataset.")
        return None
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    logging.info("✅ Top %d recommendations ready.", top_n)
    
    # Create DataFrame with clean serial numbers starting from 1
    result_df = df[['title']].iloc[movie_indices].reset_index(drop=True)
    result_df.index = result_df.index + 1  # Start from 1 instead of 0
    result_df.index.name = "S.No."

    return result_df
