# omdb_utils.py
import requests

def get_movie_details(title, api_key):
    url = f"http://www.omdbapi.com/?t={title}&plot=short&apikey={api_key}"
    res = requests.get(url).json()
    
    if res.get("Response") == "True":
        # Extract all the details you want
        plot = res.get("Plot", "N/A")
        poster = res.get("Poster", "N/A")
        genre = res.get("Genre", "N/A")
        imdb_rating = res.get("imdbRating", "N/A")
        actors = res.get("Actors", "N/A")
        director = res.get("Director", "N/A")
        awards = res.get("Awards", "N/A")
        
        return plot, poster, genre, imdb_rating, actors, director, awards
    
    return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
