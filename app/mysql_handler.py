import mysql.connector
from KEYS import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def add_movie(movie_info):
    values = (movie_info.get('movie_id'),
              movie_info.get('title') ,
              movie_info.get('overview'),
              movie_info.get('directors'),
              movie_info.get('release_date'),
              movie_info.get('poster_path'),
              ', '.join(movie_info.get('genres')))
    cur.execute("INSERT IGNORE INTO movies VALUES(%s, %s, %s, %s, %s, %s, %s)", values)
    con.commit()

def add_watched_movie(user_id, movie_id):
    cur.execute("INSERT IGNORE INTO watched_movies (user_id, movie_id) VALUES(%s, %s)", (user_id, movie_id))
    con.commit()

def remove_watched_movie(user_id, movie_id):
    cur.execute(f"DELETE FROM watched_movies WHERE movie_id=%s AND user_id=%s;", (movie_id, user_id))
    try:
        # Try to delete movie record, catches exception if bound via foreign key (added as watched by another account)
        cur.execute(f"DELETE FROM movies WHERE movie_id=%s;", (movie_id,))
    except mysql.connector.errors.IntegrityError as e:
        print(f"Movie record can't be deleted: {e}")
    con.commit()

def get_user_id(username):
    cur.execute(f"select user_id from users where username=%s;", (username,))
    return cur.fetchone()[0]

def get_watched_movies(user_id):
    cur.execute(f"SELECT movies.* "
                f"FROM watched_movies INNER JOIN movies "
                f"ON watched_movies.movie_id = movies.movie_id "
                f"WHERE user_id=%s "
                f"ORDER BY watched_movies.date_added DESC;", (user_id,))
    keys = ("movie_id","title","overview","directors","release_date","poster_path","genres")
    return [dict(zip(keys,record)) for record in cur.fetchall()]

def get_all_users():
    cur.execute(f"Select user_id, username from users;")
    users = cur.fetchall()
    return sorted(users, key=lambda x: x[0])

con = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = con.cursor()
cur.execute(f"USE {DB_NAME};")
