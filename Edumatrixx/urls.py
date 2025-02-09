"""
URL configuration for Edumatrixx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from students import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("/home", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("", views.index, name="index"),
    path("subject/", views.subject, name="subject"),
    path(r"test_details/<slug:subject>/", views.test_details, name="test_details"),
    path(
        r"test/<slug:subject>/<slug:topic>/<slug:numQuestions>/<slug:time>/<slug:userid>/<slug:testid>",
        views.test,
        name="test",
    ),
    path(r"report/<slug:testid>", views.report, name="report"),
    path("profile/", views.profile, name="profile"),
    path("editname/", views.change_username, name="edit_name"),
    path("request-password-reset/", views.request_change, name="req_pwd_change"),
    path("reset_password/", views.change_password, name="change_pwd"),
]
