# app.py
# Final version using Intent-Based Keyword Search with the TMDB API.

import streamlit as st
import random
from tmdbv3api import TMDb, Discover, Search

# --- Local Imports ---
from emotion_detector import get_user_intent

# --- TMDB API Configuration ---
tmdb = TMDb()
tmdb.api_key = '4ddd2120b5bf89c4b7fe3459180259ef' 
tmdb.language = 'en'

# --- Advanced Data Fetching (Keyword-Based) ---

def get_keyword_id(keyword_string):
    """Searches TMDB for a keyword and returns its ID."""
    search = Search()
    # The keyword string is passed as a positional argument, not a keyword argument.
    results = search.keywords(keyword_string)
    if results:
        return results[0].id
    return None

def fetch_movies_by_intent(intent, limit=10):
    """
    Finds movies based on plot keywords derived from the user's intent.
    """
    intent_to_keywords = {
        'a romantic love story': 'love',
        'a lighthearted and funny comedy': 'comedy',
        'an exciting action-packed adventure': 'action',
        'a serious and emotional drama': 'drama',
        'a scary and suspenseful thriller': 'suspense',
        'a futuristic science fiction story': 'future'
    }
    
    search_keyword = intent_to_keywords.get(intent)
    
    if not search_keyword:
        return []

    keyword_id = get_keyword_id(search_keyword)
    
    if not keyword_id:
        return []

    discover = Discover()
    response = discover.discover_movies({
        'sort_by': 'popularity.desc',
        'with_keywords': str(keyword_id),
        'vote_count.gte': 100,
    })
    
    movie_list = list(response)
    return movie_list[:limit]

# --- Streamlit User Interface ---
st.set_page_config(page_title="MoodFlix", page_icon="🎬", layout="wide")
st.title("🎬 MoodFlix: Intent-Based Movie Recommender")
st.write("Describe the kind of movie you want to watch, and we'll find it for you!")

# placeholder_sentences = [
#     "I'm in the mood for a beautiful love story.",
#     "I want to watch something that will make me laugh out loud.",
#     "Show me some intense and suspenseful movies.",
#     "I feel like watching a serious and thought-provoking drama.",
# ]
# random_placeholder = random.choice(placeholder_sentences)
user_input = st.text_area(
    "What kind of movie are you looking for?",
    height=100
)

if st.button("Recommend Me a Movie!"):
    if user_input and user_input.strip():
        with st.spinner('Understanding your request... 🤔'):
            detected_intent, confidence_score = get_user_intent(user_input)
        
        confidence_text = f"{confidence_score:.0%}"
        st.success(f"We're {confidence_text} sure you're looking for: **{detected_intent}**")
        st.progress(confidence_score)
        
        with st.spinner('Finding the perfect movies for you... 🍿'):
            recommended_movies = fetch_movies_by_intent(detected_intent, limit=10)
        
        if recommended_movies:
            st.subheader("Based on your request, you might like these:")
            for movie in recommended_movies:
                col1, col2 = st.columns([1, 4])
                with col1:
                    if movie.poster_path:
                        st.image(f"https://image.tmdb.org/t/p/w500{movie.poster_path}", width=150)
                    else:
                        st.image("https://via.placeholder.com/150x225.png?text=No+Poster", width=150)
                
                with col2:
                    st.subheader(movie.title)
                    st.caption(f"Rating: {movie.vote_average} ⭐")
                    st.write(movie.overview)
        else:
            st.warning("Sorry, we couldn't find any movies that matched your request. Please try describing it differently.")
    else:
        st.error("Please describe the kind of movie you want to watch.")