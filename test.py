from mysql_handler import cur

cur.execute("select genres from movies where title='Skyfall'")
movie_info = cur.fetchone()
print(movie_info)

# https://colorhunt.co/palette/5d8736809d3ca9c46cf4ffc3