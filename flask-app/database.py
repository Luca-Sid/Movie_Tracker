import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

from KEYS import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def add_movie(movie_info):
    con, cur = get_db()
    values = (movie_info.get('movie_id'),
              movie_info.get('title') ,
              movie_info.get('overview'),
              movie_info.get('directors'),
              movie_info.get('release_date'),
              movie_info.get('poster_path'),
              ', '.join(movie_info.get('genres')))
    try:
        cur.execute("INSERT IGNORE INTO movies VALUES(%s, %s, %s, %s, %s, %s, %s)", values)
        con.commit()
    finally:
        cur.close()
        con.close()

def add_watched_movie(user_id, movie_id):
    con, cur = get_db()
    try:
        cur.execute("INSERT IGNORE INTO watched_movies (user_id, movie_id) VALUES(%s, %s)", (user_id, movie_id))
        con.commit()
    finally:
        cur.close()
        con.close()

def remove_watched_movie(user_id, movie_id):
    con, cur = get_db()
    try:
        cur.execute(f"DELETE FROM watched_movies WHERE movie_id=%s AND user_id=%s;", (movie_id, user_id))
        try:
            # Try to delete movie record, catches exception if bound via foreign key (added as watched by another account)
            cur.execute(f"DELETE FROM movies WHERE movie_id=%s;", (movie_id,))
        except mysql.connector.errors.IntegrityError as e:
            print(f"Movie record can't be deleted: {e}")
        con.commit()
    finally:
        cur.close()
        con.close()

def get_user_id(username):
    con, cur = get_db()
    try:
        cur.execute(f"select user_id from users where username=%s;", (username,))
        return cur.fetchone()[0]
    finally:
        cur.close()
        con.close()

def get_watched_movies(user_id):
    con, cur = get_db()
    try:
        cur.execute(f"SELECT movies.* "
                    f"FROM watched_movies INNER JOIN movies "
                    f"ON watched_movies.movie_id = movies.movie_id "
                    f"WHERE user_id=%s "
                    f"ORDER BY watched_movies.date_added DESC;", (user_id,))
        keys = ("movie_id","title","overview","directors","release_date","poster_path","genres")
        return [dict(zip(keys,record)) for record in cur.fetchall()]
    finally:
        cur.close()
        con.close()

def number_of_movies(user_id):
    """
    Returns the number of movies watched by a specified user
    """
    con, cur = get_db()
    cur.execute("select count(id) from watched_movies where user_id=%s;", (user_id,))
    result = cur.fetchone()[0]
    cur.close()
    con.close()
    return result


# INITIALIZATION
pool = MySQLConnectionPool(pool_name='mypool',
                           pool_size=10,
                           host=DB_HOST,
                           port=DB_PORT,
                           user=DB_USER,
                           password=DB_PASSWORD,
                           database=DB_NAME
                           )

def get_db():
    con = pool.get_connection()
    cur = con.cursor()
    return con, cur