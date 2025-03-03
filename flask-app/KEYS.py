import os

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# DB information
DB_HOST = os.getenv('DB_HOST', default='localhost')
DB_PORT = os.getenv('DB_PORT', default='3306')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME', default='movie_tracker') # Name of the database inside mysql
