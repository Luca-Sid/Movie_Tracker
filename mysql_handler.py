import mysql.connector
from KEYS import DB_HOST, DB_USER, DB_PASSWORD

def initialize_db():
    cur.execute(f'CREATE DATABASE IF NOT EXISTS movie_tracker;')
    cur.execute("USE movie_tracker;")
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "user_id int NOT NULL AUTO_INCREMENT,"
                "username varchar(255) NOT NULL,"
                "password_hash varchar(255) NOT NULL,"
                "PRIMARY KEY (user_id)"
                ");")
    cur.execute("create table IF NOT EXISTS movies("
                "movie_id int NOT NULL,"
                "title varchar(255),"
                "overview text,"
                "director varchar(255),"
                "release_date date,"
                "poster_path varchar(255),"
                "genres varchar(255),"
                "PRIMARY KEY (movie_id)"
                ");")
    cur.execute("CREATE TABLE IF NOT EXISTS watched_movies ("
                "id int NOT NULL AUTO_INCREMENT,"
                "user_id int NOT NULL,"
                "movie_id int NOT NULL,"
                "PRIMARY KEY (id),"
                "FOREIGN KEY (user_id) REFERENCES users(user_id),"
                "FOREIGN KEY (movie_id) REFERENCES movies(movie_id),"
                "CONSTRAINT uc_user_movie UNIQUE (user_id, movie_id)"
                ");")

def add_movie(movie_info):
    values = (movie_info.get('movie_id'),
              movie_info.get('title') ,
              movie_info.get('overview'),
              movie_info.get('directors'),
              movie_info.get('release_date'),
              movie_info.get('poster_path'),
              ', '.join(movie_info.get('genres')))
    cur.execute("INSERT IGNORE INTO movies VALUES(%s, %s, %s, %s, %s, %s, %s)", values)
    connection.commit()

def add_watched_movie(user_id, movie_id):
    cur.execute("INSERT IGNORE INTO watched_movies (user_id, movie_id) VALUES(%s, %s)", (user_id, movie_id))
    connection.commit()

def remove_watched_movie(user_id, movie_id):
    cur.execute(f"DELETE FROM watched_movies WHERE movie_id=%s AND user_id=%s;", (movie_id, user_id))
    try:
        # Try to delete movie record, catches exception if bound via foreign key (added as watched by another account)
        cur.execute(f"DELETE FROM movies WHERE movie_id=%s;", (movie_id,))
    except mysql.connector.errors.IntegrityError as e:
        print(f"Movie record can't be deleted: {e}")
    connection.commit()

def get_user_id(username):
    cur.execute(f"select user_id from users where username=%s;", (username,))
    return cur.fetchone()[0]

def get_watched_movies(user_id):
    cur.execute(f"SELECT movies.* "
                f"FROM watched_movies INNER JOIN movies "
                f"ON watched_movies.movie_id = movies.movie_id "
                f"WHERE user_id=%s;", (user_id,))
    keys = ("movie_id","title","overview","directors","release_date","poster_path","genres")
    return [dict(zip(keys,record)) for record in cur.fetchall()]

connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = connection.cursor()
initialize_db()
