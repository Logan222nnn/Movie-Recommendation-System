# app.py
import json
import streamlit as st
import base64
import os

# Direct import (models will be downloaded automatically from Hugging Face)
from recommend import df, recommend_movies
from omdb_utils import get_movie_details

# Get API key from environment variable (for deployment) or config file (for local)
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

if not OMDB_API_KEY:
    try:
        config = json.load(open("config.json"))
        OMDB_API_KEY = config["OMDB_API_KEY"]
    except FileNotFoundError:
        st.error("❌ OMDB API key not found! Please set OMDB_API_KEY environment variable.")
        st.stop()

# Background function
def set_background_image(image_file):
    if os.path.exists(image_file):
        img_data = base64.b64encode(open(image_file, "rb").read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_data}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)

# Set background (with error handling)
set_background_image('background_image.jpg')

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommendation System")

# Movie selection
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

if st.button("🚀 Recommend Similar Movies"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")
            for _, row in recommendations.iterrows():
                movie_title = row['title']
                # Get enhanced movie details
                plot, poster, genre, imdb_rating, actors, director, awards = get_movie_details(movie_title, OMDB_API_KEY)

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=120)
                        else:
                            st.write("❌ No Poster Found")
                    
                    with col2:
                        st.markdown(f"### {movie_title}")
                        
                        # Display all the new information
                        if plot != "N/A":
                            st.markdown(f"**Plot:** _{plot}_")
                        
                        if genre != "N/A":
                            st.markdown(f"**Genre:** {genre}")
                        
                        if imdb_rating != "N/A":
                            st.markdown(f"**IMDb Rating:** ⭐ {imdb_rating}/10")
                        
                        if director != "N/A":
                            st.markdown(f"**Director:** {director}")
                        
                        if actors != "N/A":
                            st.markdown(f"**Actors:** {actors}")
                        
                        if awards != "N/A":
                            st.markdown(f"**Awards:** 🏆 {awards}")
                        
                        st.markdown("---")

# Creator credit
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; font-style: italic; margin-top: 50px;'>
    <p>🎬 Created by <strong>Sankaran S</strong> 🎬</p>
</div>
""", unsafe_allow_html=True)
