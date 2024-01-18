import sqlite3

# connect database
try:
    con = sqlite3.connect("./db.sqlite3", check_same_thread=False)
    print("suc")
except:
    pass

# creating cursor
db = con.cursor()

# create students table
db.execute(
    "CREATE TABLE IF NOT EXISTS users(userid INTEGER PRIMARY KEY AUTOINCREMENT,email varchar UNIQUE NOT NULL,name TEXT NOT NULL, password TEXT NOT NULL)"
)


# making a user
def create_user(name, password, email):
    statement = """INSERT INTO users (name,password,email) VALUES (?,?,?)"""
    datatuple = (name, password, email)
    db.execute(statement, datatuple)
    con.commit()
    print("suc")


# login
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


# check login
def check(email):
    statement = f"SELECT email FROM users WHERE email ='{email}'"
    db.execute(statement)
    result = db.fetchall()
    # print(result)
    if not result:
        return True
    else:
        return False


def info(email, param):
    statement = f"SELECT {param} FROM users WHERE email ='{email}'"
    db.execute(statement)
    result = str(db.fetchall())
    characters_to_remove = "[('',)]"
    new_string = result
    for character in characters_to_remove:
        new_string = new_string.replace(character, "")
    return new_string


"""
-- Users Table
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password_hash VARCHAR(255)
);

-- Subjects Table
CREATE TABLE Subjects (
    subject_id INT PRIMARY KEY,
    subject_name VARCHAR(255)
);

-- Topics Table
CREATE TABLE Topics (
    topic_id INT PRIMARY KEY,
    topic_name VARCHAR(255),
    subject_id INT,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

-- Questions Table
CREATE TABLE Questions (
    question_id INT PRIMARY KEY,
    question_text TEXT,
    topic_id INT,
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);

-- Tests Table
CREATE TABLE Tests (
    test_id INT PRIMARY KEY,
    user_id INT,
    subject_id INT,
    topic_id INT,
    test_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);

-- TestQuestions Table
CREATE TABLE TestQuestions (
    test_question_id INT PRIMARY KEY,
    test_id INT,
    question_id INT, 
    FOREIGN KEY (test_id) REFERENCES Tests(test_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

-- UserResponses Table
CREATE TABLE UserResponses (
    response_id INT PRIMARY KEY,
    user_id INT,
    test_id INT,
    question_id INT,
    selected_option VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (test_id) REFERENCES Tests(test_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

-- Mistakes Table
CREATE TABLE Mistakes (
    mistake_id INT PRIMARY KEY,
    user_id INT,
    question_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);


"""
