function displayResult(elementId, data) {
    const resultDiv = document.getElementById(elementId);
    resultDiv.style.display = 'block';
    
    if (data.error) {
        resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        return;
    }

    if (elementId === 'topMoviesResult') {
        const movies = data.top_movies || [];
        if (movies.length === 0) {
            resultDiv.innerHTML = `<p>No top movies found.</p>`;
            return;
        }
        let html = '<h3>Top 10 Movies</h3><ul>';
        movies.forEach(movie => {
            html += `<li>${movie.title} (Rating: ${movie.rating || 'N/A'}) - IMDb ID: ${movie.imdb_id}</li>`;
        });
        html += '</ul>';
        resultDiv.innerHTML = html;
    } else {
        resultDiv.innerHTML = JSON.stringify(data, null, 2)
            .replace(/\n/g, '<br>')
            .replace(/  /g, '&nbsp;&nbsp;');
    }
}

function getMovieCast() {
    const movieName = document.getElementById('movieName').value;
    fetch(`/api/movie_cast?q=${encodeURIComponent(movieName)}`)
        .then(response => response.json())
        .then(data => displayResult('movieCastResult', data))
        .catch(error => displayResult('movieCastResult', { error: error.message }));
}

function searchByCast() {
    const castName = document.getElementById('castName').value;
    fetch(`/api/search/cast?q=${encodeURIComponent(castName)}`)
        .then(response => response.json())
        .then(data => displayResult('castMoviesResult', data))
        .catch(error => displayResult('castMoviesResult', { error: error.message }));
}

function getMovieRatings() {
    const imdbId = document.getElementById('movieIdRatings').value;
    fetch(`/api/movie_ratings?id=${encodeURIComponent(imdbId)}`)
        .then(response => response.json())
        .then(data => displayResult('ratingsResult', data))
        .catch(error => displayResult('ratingsResult', { error: error.message }));
}

function getMovieDirector() {
    const imdbId = document.getElementById('movieIdDirector').value;
    fetch(`/api/movie_director?id=${encodeURIComponent(imdbId)}`)
        .then(response => response.json())
        .then(data => displayResult('directorResult', data))
        .catch(error => displayResult('directorResult', { error: error.message }));
}

function getMovieGenre() {
    const imdbId = document.getElementById('movieIdGenre').value;
    fetch(`/api/movie_genre?id=${encodeURIComponent(imdbId)}`)
        .then(response => response.json())
        .then(data => displayResult('genreResult', data))
        .catch(error => displayResult('genreResult', { error: error.message }));
}

function getTopMovies() {
    fetch('/api/top_movies')
        .then(response => response.json())
        .then(data => displayResult('topMoviesResult', data))
        .catch(error => displayResult('topMoviesResult', { error: error.message }));
}