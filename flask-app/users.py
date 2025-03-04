from hashlib import md5
from database import cur, con
from KEYS import ADMIN_PASSWORD
import mysql.connector

def is_valid(user, tried_password) -> bool:
    """Restituisce True se l'utente è in elenco e se la password corrisponde"""
    return get_password(user) == hash(tried_password)

def get_password(username):
    cur.execute(f"select password_hash from users where username= %s ;", (username,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None

def hash(s:str):
    """Restituisce hash md5 di una stringa, convertito in hex"""
    return md5(s.encode()).hexdigest()

def get_all_users():
    cur.execute("Select user_id, username from users;")
    users = cur.fetchall()
    userlist = sorted(users, key=lambda x: x[0])
    return  [ {'user_id':x[0], 'username':x[1]} for x in userlist]

def add_user(username, password):
    """
    Adds a new user to the database
    """
    cur.execute("insert into users (username, password_hash) values (%s, %s);", (username, hash(password)))
    con.commit()

def remove_user(username):
    """
    Removes user from database
    """
    cur.execute("delete from users where username=%s;", (username,))
    con.commit()

def change_password(username, password):
    cur.execute("update users set password_hash=%s where username=%s;", (hash(password), username))
    con.commit()

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
