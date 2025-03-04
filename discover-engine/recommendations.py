from tmdb import get_similar_movies, get_movie_details
import database as db


def recommend(user_id):
    watched_movie_ids = [movie['movie_id'] for movie in db.get_watched_movies(user_id)]

    # {'movie_id': id, 'count': occurrence_count, 'rating': vote_average, 'popularity': popularity}
    recommended_movies_map = {}

    # For each watched movie, get similar movies
    for movie_id in watched_movie_ids:
        similar = get_similar_movies(movie_id)
        # Merge results, avoid any already-watched movies
        for movie_data in similar:
            sim_id = movie_data.get("id")
            if sim_id and sim_id not in watched_movie_ids:
                # If already present, increase the count; otherwise, create a new entry.
                if sim_id in recommended_movies_map:
                    recommended_movies_map[sim_id]['count'] += 1
                else:
                    rating = movie_data.get("vote_average", 0)
                    popularity = movie_data.get("popularity")
                    recommended_movies_map[sim_id] = {
                        'movie_id': sim_id,
                        'count': 1,
                        'rating': rating,
                        'popularity': popularity
                    }

    # Convert the map to a list and sort by count (primary), popularity and rating
    recommended_movies = list(recommended_movies_map.values())
    recommended_movies.sort(key=lambda x: (x['count'],x['popularity'], x['rating']), reverse=True)

    # Return movie details of the three best results
    return [get_movie_details(movie.get('movie_id')) for movie in recommended_movies[:3]]
