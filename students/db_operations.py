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


# get other info of users using email
def info(email, param):
    statement = f"SELECT {param} FROM users WHERE email ='{email}'"
    db.execute(statement)
    result = str(db.fetchall())
    characters_to_remove = "[('',)]"
    new_string = result
    for character in characters_to_remove:
        new_string = new_string.replace(character, "")
    return new_string


# Subjects Table
db.execute(
    """CREATE TABLE IF NOT EXISTS Subjects (
    subject_id INT PRIMARY KEY,
    subject_name VARCHAR(255)
);"""
)

# Topics Table
db.execute(
    """CREATE TABLE IF NOT EXISTS Topics (
    topic_id INT PRIMARY KEY,
    topic_name VARCHAR(255),
    subject_id INT,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);"""
)


# Questions Table
db.execute(
    """CREATE TABLE IF NOT EXISTS Questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT,
    answer TEXT,
    topic_id INT,
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);"""
)
# Tests Table
db.execute(
    """CREATE TABLE IF NOT EXISTS Tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    subject_id INT,
    topic_id INT,
    test_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);"""
)

# TestQuestions Table
db.execute(
    """CREATE TABLE IF NOT EXISTS TestQuestions (
    test_question TEXT,
    test_id INT,
    question_id INT, 
    FOREIGN KEY (test_id) REFERENCES Tests(test_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);"""
)

# UserResponses Table
db.execute(
    """CREATE TABLE IF NOT EXISTS UserResponses (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    test_id INT,
    question_id INT,
    selected_option VARCHAR(255),
    status BIT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (test_id) REFERENCES Tests(test_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);"""
)

# Mistakes Table
db.execute(
    """CREATE TABLE IF NOT EXISTS Mistakes (
    mistake_id INT PRIMARY KEY,
    user_id INT,
    question_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);"""
)


# clean string
def clean(word):
    characters_to_remove = "[('',)]"
    new_string = word
    for character in characters_to_remove:
        new_string = new_string.replace(character, "")
    return new_string


# get topic names
def topic_names(subject):
    db.execute(
        f"SELECT subject_id from Subjects WHERE subject_name = '{subject.title().strip()}'"
    )
    subject_id = int(clean(str(db.fetchall())))
    db.execute(f"SELECT topic_name FROM Topics WHERE subject_id = {subject_id}")
    res = db.fetchall()
    names = []
    for i in res:
        names.append(i[0])
    return names


# get topic id
def topic_id(topic):
    statement = f"SELECT topic_id from Topics WHERE topic_name = '{topic}'"
    db.execute(statement)
    topicid = int(clean(str(db.fetchall())))
    return topicid


# get subject id
def subject_id(subject):
    db.execute(
        f"SELECT subject_id from Subjects WHERE subject_name = '{subject.strip().capitalize()}'"
    )
    subject_id = int(clean(str(db.fetchall())))
    return subject_id


# get question id
def question_id(question):
    db.execute(f"SELECT question_id from Questions WHERE question_text = '{question}'")
    questionid = int(clean(str(db.fetchall())))
    return questionid


# get latest test id
def get_test_id():
    statement = f"SELECT test_id FROM Tests ORDER BY test_id DESC LIMIT 1;"
    db.execute(statement)
    res = int(clean(str(db.fetchall())))
    return res


# get questions and answers from a topic , return a list of tuples
def get_questions(topic, subject):
    list_of_topics = topic_names(subject)
    ques = []
    ans = []
    for i in list_of_topics:
        if "".join(i.split()) == topic:
            db.execute(
                f"SELECT question_text from Questions where topic_id={topic_id(i)}"
            )
            res = db.fetchall()
            con.commit()
            for j in res:
                ques.append(clean(str(j)))
            db.execute(f"SELECT answer from Questions where topic_id={topic_id(i)}")
            res2 = db.fetchall()
            for k in res2:
                ans.append(clean(str(k)))
            con.commit()

    return list(zip(ques, ans))


# create a new test
def create_test(topic, subject, user_id):
    statement = (
        "INSERT INTO Tests (user_id,subject_id,topic_id,test_name) VALUES (?,?,?,?)"
    )
    topicid = topic_id(topic)
    subjectid = subject_id(subject)
    data_tuple = (user_id, subjectid, topicid, topic)
    db.execute(statement, data_tuple)


# enter test data into responses table to generate result
def enter_testdata(user_id, test_id, question_id, selected_option, status):
    statement = "INSERT INTO UserResponses (user_id,test_id,question_id,selected_option,status) VALUES (?,?,?,?,?)"
    data_tuple = (user_id, test_id, question_id, selected_option, status)
    db.execute(statement, data_tuple)
    con.commit()
