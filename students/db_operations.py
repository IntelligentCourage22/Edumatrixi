import sqlite3

try:
    con = sqlite3.connect("./db.sqlite3", check_same_thread=False)
    print("suc")
except:
    pass


db = con.cursor()

db.execute(
    "CREATE TABLE IF NOT EXISTS users(userid INTEGER PRIMARY KEY AUTOINCREMENT,email varchar UNIQUE NOT NULL,name TEXT NOT NULL, password TEXT NOT NULL)"
)


def create_user(name, password, email):
    statement = """INSERT INTO users (name,password,email) VALUES (?,?,?)"""
    datatuple = (name, password, email)
    db.execute(statement, datatuple)
    con.commit()
    print("suc")


def login_user(email, password):
    statement = f"SELECT password FROM users WHERE email='{email}';"
    db.execute(statement)
    confirm = str(db.fetchall())
    con.commit()
    characters_to_remove = "[('',)]"
    new_string = confirm
    for character in characters_to_remove:
        new_string = new_string.replace(character, "")
    if new_string == password:
        return True
    else:
        return False

def check(email):
    statement = f"SELECT email FROM users WHERE email ='{email}'"
    db.execute(statement)
    result= db.fetchall()
    #print(result)
    if not result:
        return True
    else:
        return False


