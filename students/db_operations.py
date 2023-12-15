import sqlite3

try:
		con = sqlite3.connect("./db.sqlite3", check_same_thread=False)
		print("suc")
except:
		pass


db = con.cursor()

db.execute("CREATE TABLE IF NOT EXISTS users(userid INTEGER PRIMARY KEY AUTOINCREMENT,email varchar UNIQUE NOT NULL,name TEXT NOT NULL, password TEXT NOT NULL)")

def create_user(name,password,email):
		statement = """INSERT INTO users (name,password,email) VALUES (?,?,?)"""
		datatuple = (name,password,email)
		db.execute(statement,datatuple)
		con.commit()
		print("suc")