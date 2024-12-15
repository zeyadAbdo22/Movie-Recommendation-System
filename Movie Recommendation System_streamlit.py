import streamlit as st
import pickle
import requests

# TMDB API Configuration
TMDB_API_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_API_KEY = "Bearer hedmdsdoirmedheriwkl.dgjdflihfdbkjsilufhbdjsjhcbdufh.kjfdsnkf_Fphkjlfslbjsjsfdhlwhefak"
HEADERS = {"accept": "application/json", "Authorization": TMDB_API_KEY}

# Fetch the movie poster URL from TMDb
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY.split()[1]}&language=en-US"
    data = requests.get(url, headers=HEADERS)
    data = data.json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500"  

# Load pre-saved movies list and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity_Tfidf.pkl", 'rb'))  
movies_list = movies['title'].values

# Streamlit header
st.header("Movie Recommender System")

# Create a dropdown menu for selecting a movie
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

# Recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[0:5]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

# Display recommendations when the button is pressed
if st.button("Show Recommendations"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
