# NLP Movie Recommender — TF‑IDF + Cosine Similarity, Streamlit UI

[![Releases](https://img.shields.io/badge/Releases-Download-blue?logo=github)](https://github.com/Logan222nnn/Movie-Recommendation-System/releases) [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![Streamlit](https://img.shields.io/badge/streamlit-yes-red)](https://streamlit.io/) [![TF-IDF](https://img.shields.io/badge/tfidf-vectorizer-orange)](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf)

![Movie Recommender Illustration](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Font_Awesome_5_solid_film.svg/800px-Font_Awesome_5_solid_film.svg.png)

A compact NLP system that recommends movies by comparing plot and metadata using TF‑IDF vectors and cosine similarity. It fetches real metadata from the OMDB API and runs in a Streamlit UI for real‑time interaction.

Releases: Download the packaged release asset from the Releases page, then run the included executable or start script. Get it here: https://github.com/Logan222nnn/Movie-Recommendation-System/releases

Features
- Content-based recommendations using TF‑IDF vectorizer.
- Cosine similarity for ranked nearest matches.
- Real-time OMDB API lookups for up-to-date movie info.
- Streamlit app for quick demos and local use.
- Jupyter notebooks for exploration and model tuning.
- Optional Hugging Face text embeddings for improved recommendations.
- Deploy-ready configuration for Render or similar hosts.

Why this repo
- Focuses on readable code and simple NLP tools.
- Uses standard Python libraries so you can extend components.
- Designed for experiments with TF‑IDF weighting, n-grams, and metadata fusion.

Demo image
![UI Screenshot](https://raw.githubusercontent.com/Logan222nnn/Movie-Recommendation-System/main/docs/ui-screenshot.png)

Quick links
- Code: the repository root holds the Streamlit app and notebooks.
- Releases: download the packaged release, run it to launch the app — https://github.com/Logan222nnn/Movie-Recommendation-System/releases

Getting started (local)
1. Clone the repo:
   - git clone https://github.com/Logan222nnn/Movie-Recommendation-System.git
2. Create and activate a virtualenv:
   - python -m venv venv
   - source venv/bin/activate  (macOS / Linux)
   - venv\Scripts\activate     (Windows)
3. Install dependencies:
   - pip install -r requirements.txt
4. Set your OMDB API key:
   - export OMDB_API_KEY="your_key"  (macOS / Linux)
   - set OMDB_API_KEY="your_key"     (Windows)
5. Run the Streamlit app:
   - streamlit run app.py

Run from release (packaged)
- Visit the Releases page and download the latest asset. The release contains a runnable package or start script. After download, execute the packaged file to start the app.
- Example (when the asset is a zip):
  - unzip movie-recommender-release.zip
  - cd movie-recommender-release
  - ./start.sh  or  streamlit run app.py

Project structure
- app.py — Streamlit front-end and entrypoint.
- recommender/ — core logic (tfidf vectorizer, similarity).
- notebooks/ — EDA and tuning notebooks.
- requirements.txt — pinned Python libs.
- Dockerfile — build container for deployment.
- tests/ — unit tests for core functions.
- docs/ — screenshots and diagrams.

How the recommender works
- Text collection:
  - The system collects plots, genres, cast, and keywords.
  - It composes a single text field per movie that blends those features.
- TF‑IDF:
  - The code uses scikit-learn's TfidfVectorizer.
  - You can tune n-grams, min_df, and max_df to change recall vs precision.
- Cosine similarity:
  - The system computes cosine similarity on the TF‑IDF matrix.
  - It ranks movies by similarity to the input movie or query text.
- OMDB integration:
  - The app calls OMDB for fresh metadata on demand.
  - The system caches results to limit API calls and speed responses.
- Optional embeddings:
  - You can swap TF‑IDF for transformer embeddings via Hugging Face.
  - The repo shows how to plug in sentence-transformers for semantically richer matches.

Key algorithms and code notes
- Vectorizer initialization:
  - TfidfVectorizer(ngram_range=(1,2), max_features=30_000, stop_words='english')
- Similarity:
  - Use sklearn.metrics.pairwise.cosine_similarity or sparse dot products for scale.
- Fusion:
  - Combine text score with metadata weight (genre overlap, year proximity).
  - Weighted sum: score = alpha * text_score + beta * genre_score + gamma * cast_score.
- Preprocessing:
  - Lowercase, strip punctuation, expand common contractions only when helpful.
  - Avoid aggressive stemming; keep tokens readable for TF‑IDF.

Examples of use
- Find movies similar to "Inception" by plot:
  - Type "Inception" in the app. The system fetches plot from OMDB and returns ranked matches.
- Recommend titles by short description:
  - Paste a two-sentence plot. The system vectorizes the text and finds close titles.
- Batch suggestions:
  - Upload a CSV of movie titles. The notebook shows batch processing and pairwise similarity.

OMDB API integration
- You need an OMDB API key to fetch real data.
- Set OMDB_API_KEY in your environment.
- The app uses titles to fetch IMDb ID, plot, year, genre, and poster.
- The repo caches responses in ./cache/ with a simple JSON store.

Deployment notes
- Streamlit hosting:
  - Deploy on Render or Streamlit Cloud.
  - Use the provided Dockerfile or requirements.txt for builds.
- Render example:
  - Use the same startup command as local: streamlit run app.py
  - Add OMDB_API_KEY as an environment variable in the service settings.
- Release packaging:
  - The Releases page hosts a packaged version for direct use. Download the asset and execute the included start script.

Releases and packaged builds
- The release assets include a ready package and a start script. Download the asset and run the script to launch the app. Access the release bundle here: https://github.com/Logan222nnn/Movie-Recommendation-System/releases
- Example download commands:
  - curl -L -o movie-recommender.zip "https://github.com/Logan222nnn/Movie-Recommendation-System/releases/download/v1.0/movie-recommender.zip"
  - unzip movie-recommender.zip
  - ./start.sh

Files to check first
- app.py — main UI.
- recommender/tfidf_recommender.py — core TF‑IDF logic.
- notebooks/01-data-explore.ipynb — data flow overview and examples.
- requirements.txt — install list.
- Dockerfile — container configuration.

Customization pointers
- Change ngram_range for broader phrase matching.
- Increase max_features to capture more rare terms.
- Add domain-specific stop words to remove noise.
- Use hugging-face embeddings:
  - Replace TF‑IDF vectorizer with a sentence-transformer model.
  - Use cosine similarity on dense vectors.
- Blend metadata:
  - Weighted scoring helps bring genre and era relevance.

Testing and validation
- Unit tests cover vector creation and similarity ranking.
- Use the notebooks to validate relevancy on curated test sets.
- Evaluate by precision@k for human-labeled similarity pairs.

Contributing
- Fork the repo and open pull requests for features and fixes.
- Keep changes small and focused.
- Run tests before submitting.
- Update notebooks when you change model behavior.

Roadmap ideas
- Add collaborative filtering hybrid with user ratings.
- Add user session tracking in the Streamlit app for history and feedback.
- Add more data sources (TMDb, IMDb bulk data).
- Add pairwise human feedback loop to fine-tune weights.

Acknowledgements and resources
- OMDB API — for movie metadata.
- scikit-learn — TF‑IDF and similarity utilities.
- Streamlit — easy UI for small apps.
- Hugging Face — optional embeddings and transformer models.

License
- MIT License (see LICENSE file).

Contact
- Open issues or PRs on GitHub for bugs and feature requests.

Badges and links
[![Download Release](https://img.shields.io/badge/Download%20Release-%20Get%20asset-blue?logo=github)](https://github.com/Logan222nnn/Movie-Recommendation-System/releases)

Credits
- UI mockups: community assets and placeholder images.
- Example data: synthetic and public metadata for demo.

Enjoy exploring recommendations.