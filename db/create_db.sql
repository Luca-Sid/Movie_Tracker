CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS movies (
    movie_id INT NOT NULL,
    title VARCHAR(255),
    overview TEXT,
    director VARCHAR(255),
    release_date DATE,
    poster_path VARCHAR(255),
    genres VARCHAR(255),
    PRIMARY KEY (movie_id)
);

CREATE TABLE IF NOT EXISTS watched_movies (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    CONSTRAINT uc_user_movie UNIQUE (user_id, movie_id)
);
