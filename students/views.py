"""
echo "# Edumatrixi" >> README.md
  git init
  git add README.md
  git commit -m "first commit"
  git branch -M main
  git remote add origin https://github.com/IntelligentCourage22/Edumatrixi.git
  git push -u origin main
"""

import random
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from .db_operations import *
from django.http import Http404
from .models import *
from .db_operations import *
from django.contrib import messages


def login_required(function):
    def wrapper(request, *args, **kw):
        if not "user" in request.session:
            return HttpResponseRedirect("/login")
        else:
            return function(request, *args, **kw)

    return wrapper


@login_required
def home(request):
    if "user" in request.session:
        cuser = request.session["user"]
        name_of_user = info(cuser, "name")
        ctx = {"name": name_of_user}
        return render(request, "home.html", context=ctx)
    else:
        return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if check(email) == False:
            messages.info(request, "email is already in use")
            return redirect("/signup")
        else:
            print(name, email, password)
            create_user(name, password, email)
            return redirect("/")

    else:
        return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = login_user(email=email, password=password)
        if confirm == True:
            request.session["user"] = email
            return redirect("/")

        else:
            messages.info(request, "Invalid credentials")
            return redirect("/login")

    else:
        return render(request, "login.html")


@login_required
def logout(request):
    del request.session["user"]
    return render(request, "logout.html")


def index(request):
    if "user" in request.session:
        cuser = request.session["user"]
        print(cuser)
        name_of_user = info(cuser, "name")
        ctx = {"name": name_of_user}
        return render(request, "index.html", context=ctx)
    else:
        return render(request, "index.html")


@login_required
def subject(request):
    if request.method == "POST":
        subj = request.POST["subject"]
        return redirect("test_details", subj)
    else:
        return render(request, "subject.html")


@login_required
def test_details(request, subject):
    list_of_topics = topic_names(subject)
    if request.method == "POST":
        topic_name = request.POST["topic"]
        topic = "".join(request.POST["topic"].split())
        print(topic)
        numQuestions = request.POST["numQuestions"]
        time = request.POST["timePerQuestion"]
        user_id = info(request.session["user"], "userid")
        create_test(topic_name, subject, user_id)
        test_id = get_test_id()
        return redirect("test", subject, topic, numQuestions, time, user_id, test_id)
    else:
        return render(request, "test_details.html", context={"topics": list_of_topics})


@login_required
def test(request, subject, topic, numQuestions, time, userid, testid):
    try:
        qna = get_questions(topic, subject)[: int(numQuestions)]

    except IndexError:
        qna = get_questions(topic, subject)
    questions = [ques for ques, ans in qna]
    answers = [ans for ques, ans in qna]
    if int(numQuestions) < len(questions):
        questions = random.sample(questions, k=numQuestions)

    user_response = []
    if request.method == "POST":
        for i in range(1, len(questions) + 1):
            user_response.append(request.POST.get(f"q{i}"))
        for i in range(len(questions)):
            status = 0
            if answers[i] == user_response[i]:
                status = 1
            if not user_response[i]:
                status = None
            enter_testdata(
                userid,
                testid,
                question_id(questions[i]),
                user_response[i],
                status,
            )
            print("done")

        return redirect("report", testid)
    else:
        return render(
            request,
            "test.html",
            context={
                "questions": questions,
                "time": int(time) * 60 * len(questions),
                "numOfQuestions": len(questions),
            },
        )


@login_required
def report(request, testid):
    db.execute(f"SELECT * FROM UserResponses where test_id = {testid}")
    res = db.fetchall()
    con.commit()
    print(res)
    correct = 0
    wrong = 0
    unattempted = 0
    for i in range(len(res)):
        if res[i][-1] == 0:
            wrong += 1
        elif res[i][-1] == 1:
            correct += 1
        elif res[i][-1] == None:
            unattempted += 1

    return render(
        request,
        "report.html",
        context={
            "correct": correct,
            "wrong": wrong,
            "unattempted": unattempted,
            "total": len(res),
        },
    )
