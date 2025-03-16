from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

# IMDb API configuration
IMDB_SEARCH_URL = "https://imdb8.p.rapidapi.com/title/find"
IMDB_CAST_URL = "https://imdb8.p.rapidapi.com/title/get-full-credits"
IMDB_DETAILS_URL = "https://imdb8.p.rapidapi.com/title/get-ratings"
IMDB_TOP_MOVIES_URL = "https://imdb8.p.rapidapi.com/title/get-top-rated-movies"
IMDB_META_URL = "https://imdb8.p.rapidapi.com/title/get-overview-details"

HEADERS = {
    'x-rapidapi-key': 'd9045911f0msha288e25cc902400p1dd65ejsn15a51e9fa5c0',  # Replace with your RapidAPI key
    'x-rapidapi-host': 'imdb8.p.rapidapi.com',
}

@app.route('/')
def home():
    return render_template('index.html')

# Existing endpoint: Search movie by name and get cast
@app.route('/api/movie_cast', methods=['GET'])
def get_movie_cast():
    movie_name = request.args.get('q')
    if not movie_name:
        return jsonify({'error': 'Movie name is required'}), 400
    
    try:
        params = {'q': movie_name}
        search_response = requests.get(IMDB_SEARCH_URL, headers=HEADERS, params=params)
        search_response.raise_for_status()
        search_data = search_response.json()
        results = search_data.get('results', [])
        if not results:
            return jsonify({'error': 'No movies found'}), 404
        
        movie = results[0]
        imdb_id = movie.get('id', '').replace('/title/', '').replace('/', '')
        
        params = {'tconst': imdb_id}
        cast_response = requests.get(IMDB_CAST_URL, headers=HEADERS, params=params)
        cast_response.raise_for_status()
        cast_data = cast_response.json()
        
        if 'cast' not in cast_data:
            return jsonify({'error': 'No cast details found'}), 404

        top_cast = [
            {
                'name': member.get('name', 'Unknown'),
                'character': member.get('characters', ['Unknown'])[0]
            }
            for member in cast_data.get('cast', [])[:5]
        ]

        return jsonify({
            'title': movie.get('title', 'Unknown'),
            'imdb_id': imdb_id,
            'top_cast': top_cast,
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch data: {str(e)}'}), 500

# Existing endpoint: Search movies by cast member name
@app.route('/api/search/cast', methods=['GET'])
def search_by_cast():
    cast_name = request.args.get('q')
    if not cast_name:
        return jsonify({'error': 'Cast name is required'}), 400
    
    try:
        params = {'q': cast_name}
        response = requests.get(IMDB_SEARCH_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = data.get('results', [])
        movies = [
            {
                'title': result.get('title', 'Unknown'),
                'imdb_id': result.get('id', '').replace('/title/', '').replace('/', '')
            }
            for result in results if 'title' in result
        ]
        return jsonify({'movies': movies[:3]})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to search cast: {str(e)}'}), 500

# New endpoint: Fetch movie ratings
@app.route('/api/movie_ratings', methods=['GET'])
def get_movie_ratings():
    imdb_id = request.args.get('id')
    if not imdb_id:
        return jsonify({'error': 'IMDb ID is required'}), 400
    
    try:
        params = {'tconst': imdb_id}
        response = requests.get(IMDB_DETAILS_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        
        rating = data.get('rating', 'N/A')
        votes = data.get('ratingCount', 'N/A')
        
        return jsonify({
            'imdb_id': imdb_id,
            'rating': rating,
            'votes': votes
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch ratings: {str(e)}'}), 500

# New endpoint: Fetch movie director
@app.route('/api/movie_director', methods=['GET'])
def get_movie_director():
    imdb_id = request.args.get('id')
    if not imdb_id:
        return jsonify({'error': 'IMDb ID is required'}), 400
    
    try:
        params = {'tconst': imdb_id}
        response = requests.get(IMDB_CAST_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        
        crew = data.get('crew', {}).get('director', [])
        director = crew[0].get('name', 'Unknown') if crew else 'Unknown'
        
        return jsonify({
            'imdb_id': imdb_id,
            'director': director
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch director: {str(e)}'}), 500

# New endpoint: Fetch movie genre
@app.route('/api/movie_genre', methods=['GET'])
def get_movie_genre():
    imdb_id = request.args.get('id')
    if not imdb_id:
        return jsonify({'error': 'IMDb ID is required'}), 400
    
    try:
        params = {'tconst': imdb_id}
        response = requests.get(IMDB_META_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        
        genres = data.get('genres', ['Unknown'])
        
        return jsonify({
            'imdb_id': imdb_id,
            'genres': genres
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch genres: {str(e)}'}), 500

# New endpoint: Fetch top 10 movies
@app.route('/api/top_movies', methods=['GET'])
def get_top_movies():
    try:
        response = requests.get(IMDB_TOP_MOVIES_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        # Since data is a list, slice it directly to get the top 10
        top_movies = [
            {
                'title': movie.get('title', 'Unknown'),
                'imdb_id': movie.get('id', '').replace('/title/', '').replace('/', ''),
                'rating': movie.get('chartRating', 'N/A')
            }
            for movie in data[:10]  # Take the first 10 items from the list
        ]
        
        return jsonify({'top_movies': top_movies})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch top movies: {str(e)}'}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5010)