from flask import Flask, render_template, request, url_for, redirect, session, flash
import requests
from KEYS import RECOMMENDATION_HOST

from tmdb import search_movie, get_movie_details
import database as db
import users
import mysql.connector

app = Flask(__name__)
app.secret_key = "gPs26!eE3$R9Dfhj3$R9Df"


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
                return render_template('movies.html',search=True, results=results,
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
            # If the method is GET show the page with only the previously added movies
            return render_template('movies.html', watched_movies=db.get_watched_movies(session['id']))
    else:
        # If the user is not logged on
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
        if users.is_valid(username, pwd):
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

@app.route('/control_panel')
def control_panel():
    """Shows the control panel only to the admin user"""
    if session.get('username').lower() == 'admin':
        return render_template('control_panel.html', users=users.get_all_users())
    else:
        return redirect(url_for('index'))

@app.route('/discover')
def discover():
    """Discover page. If the user has added at least three movies it gives suggestions based on those."""
    if session.get('username'):
        if db.number_of_movies(session.get('id')) >= 3:
            return render_template('discover.html')
        else:
            return render_template('discover_not_enough.html')
    else:
        return redirect(url_for('login'))

@app.route('/api/recommendations')
def api_recommendations():
    """Calls the recommendation microservice"""
    if session.get('id'):
        try:
            response = requests.get(f"http://{RECOMMENDATION_HOST}/recommendation/{session.get('id')}")
            return response.json()
        except requests.exceptions.RequestException:
            return []

@app.route('/api/add_user', methods=['POST'])
def api_add_user():
    if session.get('username').lower() == 'admin':
        username = request.form.get('username')
        password  = request.form.get('password')
        if username and password :
            try:
                users.add_user(username, password)
            except mysql.connector.Error as e:
                if e.errno == 1062:  # MySQL error code for duplicate entry
                    flash(f'User "{username}" already exists', 'warning')
                else:
                    flash("Database error", 'danger')
            return redirect(url_for('control_panel'))
        else:
            return render_template('error.html', error='Method not recognized')
    else:
        return render_template('error.html', error='Not authorized')

@app.route('/api/rm_user', methods=['POST'])
def api_rm_user():
    if session.get('username').lower() == 'admin':
        username = request.form.get('username')
        if username.lower() == 'admin':
            flash("You can't delete the admin account", 'warning')
            return redirect(url_for('control_panel'))
        elif username:
            users.remove_user(username)
            flash(f"Successfully deleted user account {username} ", 'success')
            return redirect(url_for('control_panel'))
        else:
            return render_template('error.html', error='Method not recognized')
    else:
        return render_template('error.html', error='Not authorized')

@app.route('/api/change_password', methods=['POST'])
def api_change_password():
    if session.get('username').lower() == 'admin':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            users.change_password(username, password)
            flash(f"Successfully changed password for user {username} ", 'success')
            print('test')
            return redirect(url_for('control_panel'))
        else:
            return render_template('error.html', error='Method not recognized')
    else:
        return render_template('error.html', error='Not authorized')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
