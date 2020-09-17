from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "users/layout.html")

def login(request):
    return render(request, "users/login.html")

def register(request):
    return render(request, "users/register.html")

def logout(request):
    # Pending
    pass
