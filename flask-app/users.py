from hashlib import md5
from database import get_db
from KEYS import ADMIN_PASSWORD
import mysql.connector

def is_valid(user, tried_password) -> bool:
    """Restituisce True se l'utente è in elenco e se la password corrisponde"""
    return get_password(user) == hash(tried_password)

def get_password(username):
    con, cur = get_db()
    try:
        cur.execute(f"select password_hash from users where username= %s ;", (username,))
        result = cur.fetchone()
    finally:
        cur.close()
        con.close()

    if result:
        return result[0]
    else:
        return None

def hash(s:str):
    """Restituisce hash md5 di una stringa, convertito in hex"""
    return md5(s.encode()).hexdigest()

def get_all_users():
    con, cur = get_db()
    try:
        cur.execute("Select user_id, username from users;")
        users = cur.fetchall()
        userlist = sorted(users, key=lambda x: x[0])
        return  [ {'user_id':x[0], 'username':x[1]} for x in userlist]
    finally:
        cur.close()
        con.close()

def add_user(username, password):
    """
    Adds a new user to the database
    """
    con, cur = get_db()
    try:
        cur.execute("insert into users (username, password_hash) values (%s, %s);", (username, hash(password)))
        con.commit()
    finally:
        cur.close()
        con.close()

def remove_user(user_id):
    """
    Removes user from database
    """
    con, cur = get_db()
    try:
        cur.execute("delete from watched_movies where user_id=%s;", (user_id,))
        con.commit()
        cur.execute("delete from users where user_id=%s;", (user_id,))
        con.commit()
    finally:
        cur.close()
        con.close()

def change_password(username, password):
    con, cur = get_db()
    try:
        cur.execute("update users set password_hash=%s where username=%s;", (hash(password), username))
        con.commit()
    finally:
        cur.close()
        con.close()

# Initialization: create user account
if ADMIN_PASSWORD:
    try:
        add_user('admin', ADMIN_PASSWORD)
        print("Added admin user to database")
    except mysql.connector.Error as e:
        if e.errno == 1062:  # MySQL error code for duplicate entry
            print(f'Admin user  already exists')
        else:
            print("Database error:\n", e)
