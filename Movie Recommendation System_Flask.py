from flask import Flask, request, jsonify, render_template
import pickle
import requests

app = Flask(__name__)

# TMDB API Configuration
TMDB_API_KEY = "dgjdfli86516hfdbkjsisdlufhbdjsjhcbdufh"  

# Load pre-saved movies list and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity_Tfidf.pkl", 'rb'))  
movies_list = movies['title'].values

# Function to fetch movie poster URL from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path', '')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500"  # Return placeholder if no poster is found

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[0:10]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

# Home route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html', movies=movies_list)

# API endpoint for movie recommendations
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    # Parse JSON data from the request
    data = request.get_json()
    movie = data['movie']
    
    # Get recommendations
    recommended_titles, recommended_posters = recommend(movie)
    
    # Return recommendations as JSON
    return jsonify({"titles": recommended_titles, "posters": recommended_posters})

if __name__ == '__main__':
    app.run(debug=True)
