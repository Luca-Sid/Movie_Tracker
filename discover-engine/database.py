import mysql.connector
from KEYS import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def get_watched_movies(user_id):
    cur.execute(f"SELECT movies.* "
                f"FROM watched_movies INNER JOIN movies "
                f"ON watched_movies.movie_id = movies.movie_id "
                f"WHERE user_id=%s "
                f"ORDER BY watched_movies.date_added DESC;", (user_id,))
    keys = ("movie_id","title","overview","directors","release_date","poster_path","genres")
    result = [dict(zip(keys,record)) for record in cur.fetchall()]
    con.commit()
    return result


# INITIALIZATION
con = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = con.cursor()
cur.execute(f"USE {DB_NAME};")
