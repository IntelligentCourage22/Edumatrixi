"""
echo "# Edumatrixi" >> README.md
  git init
  git add README.md
  git commit -m "first commit"
  git branch -M main
  git remote add origin https://github.com/IntelligentCourage22/Edumatrixi.git
  git push -u origin main
"""


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
        print(cuser)
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


def subject(request):
    if request.method == "POST":
        subj = request.POST["subject"]
        return redirect("test_details", subj)
    else:
        return render(request, "subject.html")


def test_details(request, subject):
    list_of_topics = topic_names(subject)
    if request.method == "POST":
        topic = "".join(request.POST["topic"].split())
        print(topic)
        numQuestions = request.POST["numQuestions"]
        time = request.POST["timePerQuestion"]
        return redirect("test", subject, topic, numQuestions, time)
    else:
        return render(request, "test_details.html", context={"topics": list_of_topics})


def test(request, subject, topic, numQuestions, time):
    try:
        questions = get_questions(topic, subject)[: int(numQuestions)]
        print(questions)
    except IndexError:
        questions = get_questions(topic, subject)
        print(questions)
    user_response = []
    if request.method == "POST":
        for i in range(1, len(questions) + 1):
            user_response.append((f"answer{i}", request.POST.get(f"q{i}")))
        print(user_response)
        return redirect("/")
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
