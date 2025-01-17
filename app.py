from flask import Flask, render_template, request, url_for, redirect, session
from tmdb import search_movie, get_movie_details
import login_check
import mysql_handler as db


app = Flask(__name__)
app.secret_key = "gPs26!eE3$R9Dfhj3$R9Df"

movies_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if session.get('username'):
        if request.method == 'POST':
            # If search button is pressed
            if request.form.get('search'):
                searched_text = request.form['search']
                results = search_movie(searched_text)
                if results:
                    return render_template('movies.html', results=results,
                                           searched_text=searched_text, watched_movies=db.get_watched_movies(session['id']))
            # elif Add button is pressed
            elif request.form.get('id'):
                movie_info = get_movie_details(request.form.get('id'))
                db.add_movie(movie_info)
                db.add_watched_movie(session['id'], movie_info['movie_id'])
                return redirect(url_for('movies'))
            else:
                return render_template('error.html', error='Method not recognized')
        else:
            return render_template('movies.html', watched_movies=db.get_watched_movies(session['id']))
    else:
        return redirect(url_for('login'))

@app.route('/remove_movie', methods=['POST'])
def remove_movie():
    user_id = request.form.get('user_id')
    movie_id = request.form.get('movie_id')
    if user_id and movie_id:
        db.remove_watched_movie(user_id, movie_id)
        return redirect(url_for('movies'))
    else:
        render_template('error', error="Wrong parameters")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Se la richiesta è POST analizziamo i dati del form
        username = request.form['username']
        pwd = request.form['password']
        if login_check.is_valid(username, pwd):
            # Se il login è valido salviamo l'username nel cookie e reindirizziamo alla pagina
            session['username']=username
            session['id']=db.get_user_id(username)
            return redirect(url_for('movies'))
        else:
            # Se le credenziali non sono valide ricarichiamo la pagina con il messaggio di avviso
            return render_template('login.html', errore=True)
    else:
        # Se la richiesta è get presentiamo la pagina di login
        return render_template('login.html')

@app.route('/logout')
def logout():
    """Pulisce il cookie e reindirizza alla homepage"""
    session.pop('username')
    session.pop('id')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
