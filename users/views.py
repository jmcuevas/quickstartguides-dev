from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import User
from questions.models import Question, Answer

# Only emails in ALLOWED_DOMAIN can create accounts
ALLOWED_DOMAIN = ["@hdcco.com"]

def index(request):
    if (request.user.is_authenticated):
        return HttpResponseRedirect(reverse('guides_list_all'))
    else:
        return render(request, "users/login.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('guides_list_all'))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "users/login.html")

def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        domain = email[email.index('@') : ]
        username = email[ : email.index('@')]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        
        # Only emails with allowed domain can register
        if not (domain in ALLOWED_DOMAIN):
            print("---Account not created. Only Allowed domains can create account")
            return render(request, "users/register.html", {
                "message": "Account not created. Only Allowed domains can create account"
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.last_name = last_name
            user.first_name = first_name
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('guides_list_all'))
    else:
        return render(request, "users/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    questions = Question.objects.filter(created_by=profile_user)
    answers = Answer.objects.filter(created_by=profile_user)
    answered_questions = []

    for answer in answers:
        answered_questions.append(answer.question)

    print(f"---Answers: {answers}")
    print(f"---Answered questions: {answered_questions}")

    return render(request, "users/profile.html", {
        "profile_user": profile_user,
        "questions": questions,
        "answered_questions": answered_questions})
