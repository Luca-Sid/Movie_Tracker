from hashlib import md5
from mysql_handler import cur, con

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

if __name__ == '__main__':
    print(is_valid('luca', '123'))
    print(is_valid('alberto', '123'))