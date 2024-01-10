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


def home(request):
    if "user" in request.session:
        cuser = request.session["user"]
        ctx = {"name": cuser}
        return render(request, "home.html", context=ctx)
    else:
        return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if check(email)==False:
            messages.info(request,"email is already in use")
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
    return render(request,'index.html') 