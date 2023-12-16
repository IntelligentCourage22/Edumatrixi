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


def home(request):
    return render(request, "home.html")


def signup(request):
    print(f"method: {request.method}")
    if request.method == "POST":
        name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        print(name, email, password)
        create_user(name, password, email)
        return redirect("/")
    else:
        return render(request, "signup.html")
