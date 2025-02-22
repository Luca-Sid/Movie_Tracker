from tmdb import get_similar_movies
import mysql_handler as db


def recommend(user_id):
    """
    1. Get the list of movies the user has watched.
    2. For each watched movie, fetch its 'similar' movies from TMDB.
    3. Merge the results by storing only the movie_id, rating, and count.
    4. Sort recommendations primarily by count and then by rating.
    """
    # 1. Fetch user's watched movie IDs from the database
    watched_movie_ids = [movie['movie_id'] for movie in db.get_watched_movies(user_id)]

    # A structure to store recommended movies keyed by TMDB movie ID.
    # Each entry will have the structure: {'movie_id': id, 'rating': vote_average, 'count': occurrence_count}
    recommended_movies_map = {}

    # 2. For each watched movie, get similar titles
    for movie_id in watched_movie_ids:
        similar = get_similar_movies(movie_id)
        # 3. Merge results, skipping any already-watched movies
        for movie_data in similar:
            sim_id = movie_data.get("id")
            if sim_id and sim_id not in watched_movie_ids:
                rating = movie_data.get("vote_average", 0)
                # If already present, increase the count; otherwise, create a new entry.
                if sim_id in recommended_movies_map:
                    recommended_movies_map[sim_id]['count'] += 1
                else:
                    recommended_movies_map[sim_id] = {
                        'movie_id': sim_id,
                        'rating': rating,
                        'count': 1
                    }

    # 4. Convert the map to a list and sort by count (primary) and rating (secondary), both descending.
    recommended_movies = list(recommended_movies_map.values())
    recommended_movies.sort(key=lambda x: (x['count'], x['rating']), reverse=True)

    return recommended_movies


# ------------------------
# Demo usage (standalone):
# ------------------------
if __name__ == "__main__":
    # In a real Flask app, you'd have a proper db_session or ORM session
    user_id = 1

    recommendations = recommend(user_id)
    print("Recommendations:")
    # print(recommendations)
    import tmdb
    for movie in recommendations[:5]:  # Show top 5
        movie_data = tmdb.get_movie_details(movie.get('movie_id'))
        print(f"- {movie_data.get('title')} (TMDB ID: {movie.get('movie_id')}, Count: {movie.get('count')}, Rating: {movie.get('rating')})")
