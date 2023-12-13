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

def home(request):
    pass

def signup(request):
    pass