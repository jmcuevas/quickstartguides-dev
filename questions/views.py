from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django import forms
from .models import Question

# ----- Forms -----

class NewQuestionForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea(attrs= {'class':'form-control', 'placeholder':'Write a question...'}))


# ----- Views -----

def index(request):
    return render(request, "questions/index.html")

def new(request):

    # Submit new Question Form
    if request.method == "POST":
        form = NewQuestionForm(request.POST)
        
        # Valida form data
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            total_votes = 0
            created_by = request.user

            # Create and save question
            new_question = Question(
                title=title, 
                body=body, 
                total_votes=total_votes, 
                created_by=created_by)
            
            new_question.save()
            print("Sucess: Question saved")

            return(HttpResponseRedirect(reverse("index")))

        # Invalid form data
        else:
            print("Error: Post not Created")
            return HttpResponseRedirect(reverse("new"))

    # Get request to questions/new
    else:
        return render(request, 'questions/new.html', {"new_question_form": NewQuestionForm()})

def list_all(request):
    questions = Question.objects.all().order_by("-created_at")
    return render(request, "questions/list.html", 
    {"questions": questions })
