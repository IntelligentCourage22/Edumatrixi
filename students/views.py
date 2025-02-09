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
import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# wrapper function for only logged in users to acces certian pages
def login_required(function):
    def wrapper(request, *args, **kw):
        # if not logged in redirect to login
        if not "user" in request.session:
            return HttpResponseRedirect("/login")
        else:
            # else call the function which redirects to the desired website
            return function(request, *args, **kw)

    return wrapper


@login_required
def home(request):
    # check logged in user for getting name
    if "user" in request.session:
        cuser = request.session["user"]
        name_of_user = info(cuser, "name")
        # send name to html template
        ctx = {"name": name_of_user}
        return render(request, "home.html", context=ctx)
    # else return the original template with login an signup on nav bar
    else:
        return render(request, "home.html")


def signup(request):
    # get details
    if request.method == "POST":
        name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        # if email already exists print appropriate message
        if check(email) == False:
            messages.info(request, "email is already in use")
            return redirect("/signup")
        # create user, login and redirect to main page
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
        # check if credentials are right
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
def change_username(request):
    if request.method == "POST":
        new_name = request.POST["username"]
        password = request.POST["password"]
        email = request.session["user"]
        # check if credentials are right
        status = edit_name(new_name, password, email)
        if status:
            return redirect("/profile")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("/editname")

    else:
        return render(request, "edit_name.html")


@login_required
def request_change(request):
    if "user" in request.session:
        HOST = "smtp.gmail.com"
        PORT = 587
        FROM_EMAIL = "bansh8956@gmail.com"
        TO_EMAIL = request.session["user"]
        PASSWORD = "lrry hlza eojl hvlc"

        message = MIMEMultipart("alternative")
        message["Subject"] = "<add subject here>"
        message["From"] = FROM_EMAIL
        message["To"] = TO_EMAIL
        message["Cc"] = FROM_EMAIL
        message["Bcc"] = FROM_EMAIL
        html = """<html>

<body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f4f4f9;">
    <table
        style="max-width: 600px; margin: 20px auto; background: white; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <tr>
            <td
                style="background-color: #4CAF50; color: white; text-align: center; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                <h1 style="margin: 0;">Reset Your Password</h1>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px; color: #333;">
                <p>Hey!</p>
                <p>We received a request to reset your password. Click the button below to reset it:</p>
                <p style="text-align: center; margin: 20px 0;">
                    <a href="http://localhost:8000/reset_password"
                        style="display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #4CAF50; border-radius: 5px; text-decoration: none;">
                        Reset Password
                    </a>
                </p>
                <p>If you did not request this, you can ignore this email. Your password will not change.</p>
            </td>
        </tr>
        <tr>
            <td
                style="text-align: center; padding: 20px; background: #f4f4f9; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; color: #999; font-size: 12px;">
                <p>&copy; 2025 Edumatrixx. All rights reserved.</p>
            </td>
        </tr>
    </table>
</body>

</html>"""

        html_part = MIMEText(html, "html")
        message.attach(html_part)

        smtp = smtplib.SMTP(HOST, PORT)

        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
        print(f"[*] Logging in: {status_code} {response}")

        smtp.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
        smtp.quit()

        return render(request, "request_passwordchange.html")

    # else return the original template with login an signup on nav bar
    else:
        return render(request, "home.html")


@login_required
def change_password(request):
    if request.method == "POST":
        new_pwd = request.POST["new_pwd"]
        old_pwd = request.POST["old_pwd"]
        email = request.session["user"]
        # check if credentials are right
        status = change_pwd(old_pwd, new_pwd, email)
        if status:
            return redirect("/profile")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("/change_pwd")

    else:
        return render(request, "reset_password.html")


@login_required
def logout(request):
    # delete user from session data
    del request.session["user"]
    return render(request, "logout.html")


# new code
@login_required
def profile(request):
    cuser = request.session["user"]
    name_of_user = info(cuser, "name")
    # send name to html template

    user_id = info(cuser, "userid")
    overall_accuracy = get_accuracy(user_id)

    try:
        math_accuracy = (
            int(total_correct_attempts(user_id, 2))
            / int(get_total_attempts(user_id, 2))
        ) * 100
    except ZeroDivisionError:
        math_accuracy = 0
    try:
        physics_accuracy = (
            int(total_correct_attempts(user_id, 0))
            / int(get_total_attempts(user_id, 0))
        ) * 100
    except ZeroDivisionError:
        physics_accuracy = 0
    try:
        chem_accuracy = (
            int(total_correct_attempts(user_id, 1))
            / int(get_total_attempts(user_id, 1))
        ) * 100
    except ZeroDivisionError:
        chem_accuracy = 0

    tests = get_tests_for_a_user(user_id)
    print(tests)
    print(user_id)
    ctx = {
        "name": name_of_user,
        "math_accuracy": math_accuracy,
        "chem_accuracy": chem_accuracy,
        "physics_accuracy": physics_accuracy,
        "overall_accuracy": overall_accuracy,
        "tests": tests,
    }
    return render(request, "profile.html", context=ctx)


# main page
def index(request):
    if "user" in request.session:
        cuser = request.session["user"]
        print(cuser)
        name_of_user = info(cuser, "name")
        ctx = {"name": name_of_user}
        return render(request, "index.html", context=ctx)
    else:
        return render(request, "index.html")


# selecting subject
@login_required
def subject(request):
    if request.method == "POST":
        subj = request.POST["subject"]
        return redirect("test_details", subj)
    else:
        return render(request, "subject.html")


# rendering test details template
@login_required
def test_details(request, subject):
    # extract topic names based on subject selected in previous page
    list_of_topics = topic_names(subject)
    # get all data regarding test details
    if request.method == "POST":
        topic_name = request.POST["topic"]
        topic = "".join(request.POST["topic"].split())
        print(topic)
        numQuestions = request.POST["numQuestions"]
        time = request.POST["timePerQuestion"]
        # extract user id from database using email
        user_id = info(request.session["user"], "userid")
        # create a test
        create_test(topic_name, subject, user_id)
        # fetch test id
        test_id = get_test_id()
        return redirect("test", subject, topic, numQuestions, time, user_id, test_id)
    else:
        return render(request, "test_details.html", context={"topics": list_of_topics})


@login_required
def test(request, subject, topic, numQuestions, time, userid, testid):
    # handle the case where number of questions entered by user is more than questions in the db
    try:
        qna = get_questions(topic, subject)[: int(numQuestions)]

    except IndexError:
        qna = get_questions(topic, subject)
    # get list of questions
    questions = [ques for ques, ans in qna]
    # list of answers
    answers = [ans for ques, ans in qna]
    # select random questions
    if int(numQuestions) < len(questions):
        questions = random.sample(questions, k=numQuestions)
    # initialise user response list
    user_response = []
    # get user responses
    if request.method == "POST":
        for i in range(1, len(questions) + 1):
            user_response.append(request.POST.get(f"q{i}"))
            # check validity of each answer
        for i in range(len(questions)):
            status = 0
            if answers[i] == user_response[i]:
                status = 1
            if not user_response[i]:
                status = None
                # enter test data for the given test into user response table
            enter_testdata(
                userid,
                testid,
                question_id(questions[i]),
                user_response[i],
                status,
            )
            # confirmation
            print("done")

        return redirect("report", testid)
    else:
        # render template again if invalid
        return render(
            request,
            "test.html",
            context={
                "questions": questions,
                "time": int(time) * 60 * len(questions),
                "numOfQuestions": len(questions),
            },
        )


# report of test
@login_required
def report(request, testid):
    # get test details
    db.execute(f"SELECT * FROM UserResponses where test_id = {testid}")
    res = db.fetchall()
    con.commit()
    # print(res)
    # get correct wrong and unattempted answers
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
    # render the template for result
    generated_report = generate_test_report(testid)

    return render(
        request,
        "report.html",
        context={
            "correct": correct,
            "wrong": wrong,
            "unattempted": unattempted,
            "total": len(res),
            "generated_report": generated_report,
        },
    )
