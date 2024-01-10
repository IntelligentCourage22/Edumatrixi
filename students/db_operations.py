import sqlite3

#connect database
try:
    con = sqlite3.connect("./db.sqlite3", check_same_thread=False)
    print("suc")
except:
    pass

#creating cursor
db = con.cursor()

#create students table
db.execute(
    "CREATE TABLE IF NOT EXISTS users(userid INTEGER PRIMARY KEY AUTOINCREMENT,email varchar UNIQUE NOT NULL,name TEXT NOT NULL, password TEXT NOT NULL)"
)

#making a user
def create_user(name, password, email):
    statement = """INSERT INTO users (name,password,email) VALUES (?,?,?)"""
    datatuple = (name, password, email)
    db.execute(statement, datatuple)
    con.commit()
    print("suc")

#login
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

#check login
def check(email):
    statement = f"SELECT email FROM users WHERE email ='{email}'"
    db.execute(statement)
    result= db.fetchall()
    #print(result)
    if not result:
        return True
    else:
        return False


