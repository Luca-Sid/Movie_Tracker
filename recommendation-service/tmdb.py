import requests
from KEYS import TMDB_API_KEY as API_KEY

BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_details(movie_id):
    # Movie Details Endpoint
    movie_details_url = f"{BASE_URL}/movie/{movie_id}"

    # Credits Endpoint (for directors)
    credits_url = f"{BASE_URL}/movie/{movie_id}/credits"

    try:
        # Fetch movie details
        movie_response = requests.get(movie_details_url, params={"api_key": API_KEY})
        movie_response.raise_for_status() # Raises error if HTTP Status not 200 (OK)
        movie_details = movie_response.json()

        # Fetch credits
        credits_response = requests.get(credits_url, params={"api_key": API_KEY})
        credits_response.raise_for_status()
        credits = credits_response.json()

        # In the crew section takes all the cast members that have director as a job
        directors = ', '.join([member['name'] for member in credits['crew'] if member['job'] == 'Director'])

        movie_info = {
            "movie_id": movie_details.get('id'),
            "title": movie_details.get("title"),
            "overview": movie_details.get("overview"),
            "directors": directors,
            "release_date": movie_details.get("release_date"),
            "poster_path": movie_details.get("poster_path"),
            "genres": [genre["name"] for genre in movie_details.get("genres", [])],
        }
        return movie_info

    except Exception as e:
        print(f"Error while getting movie info:\n{e}")
        return None



def get_similar_movies(movie_id, max_pages=1):
    """
    Fetch 'recommended' (similar) movies for a given movie_id from TMDB.
    By default, it fetches only the first page of results.
    """
    similar_movies = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/movie/{movie_id}/recommendations"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "page": page
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            similar_movies.extend(results)
        else:
            # Break out if TMDB returns a bad status
            print(f"Error fetching similar movies for {movie_id}: {response.text}")
            break

    return similar_movies
