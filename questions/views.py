from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django import forms
from .models import Question, Answer, Vote, Bookmark

# ----- Forms -----

class NewQuestionForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea(attrs= {'class':'form-control', 'placeholder':'Write a question...'}))

class NewAnswerForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs= {'class':'form-control', 'placeholder':'Write your answer...'}))

# ----- Views Questions -----

def index(request):
    return render(request, "questions/index.html")

def new(request):

    # Submit new Question Form
    if request.method == "POST":
        form = NewQuestionForm(request.POST)
        
        # Valid form data
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

    # Check if question is bookmarked by user
    for question in questions:
        try:
            bookmark = Bookmark.objects.get(question=question, user=request.user) 
            question.bookmarked_by_user = True
        except:
            question.bookmarked_by_user = False

    return render(request, "questions/list.html", 
    {"questions": questions })

def show(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = Answer.objects.filter(question=question)

    try:
        bookmark = Bookmark.objects.get(question=question, user=request.user)
        if bookmark:
            bookmarked = True
    except:
        bookmarked = False

    return render(request, "questions/show.html", {
        "question":question, 
        "answers":answers,
        "bookmarked":bookmarked,
        "answer_form": NewAnswerForm() })

def edit(request, question_id):

    # Check if question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        print("---Question does not exist---")
        return HttpResponseRedirect(reverse("questions_list_all"))

    if request.user.is_authenticated and request.user == question.created_by:
        form_data = {"title": question.title, "body": question.body}
    
        return render(request, "questions/edit.html", {"question":question, "form":NewQuestionForm(initial=form_data)})

    else:
        print("---User is not logged in or didn't created question---")
        return HttpResponseRedirect(reverse("questions_list_all"))

def update(request, question_id):

    # Check if Question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        print("---Question does not exists---")
        return HttpResponseRedirect(reverse("questions_list_all"))

    # User should have created Question to update
    if not (request.user == question.created_by):
        print("---User didn't created question")
        return HttpResponseRedirect(reverse("questions_list_all"))

    # User submited edit form
    if request.method == "POST":
        form = NewQuestionForm(request.POST)

        # Validate form data
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            new_body = form.cleaned_data["body"]

            question.title = new_title
            question.body = new_body
            question.save()

            print("---Question saved---")

            return HttpResponseRedirect(reverse("question_show", kwargs={'question_id': question.pk}))

        else:
            print("---Question data is not valid---")
            return HttpResponseRedirect(reverse("questions_list_all"))

    # Request method is other than POST
    else:
        print("---Method is not post---")
        return HttpResponseRedirect(reverse("questions_list_all"))

def delete(request, question_id):

    # Check if question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        print("---Question does not exists---")
        return HttpResponseRedirect(reverse("questions_list_all"))

    # User should have created Question to update
    if not (request.user == question.created_by):
        print("---User didn't created question")
        return HttpResponseRedirect(reverse("questions_list_all"))

    # User clicked on Delete button (Post request)
    if request.method == "POST":
        print("---Question deleted---")
        question.delete()
    else:
        print("---views.delete: not POST method---")

    return HttpResponseRedirect(reverse('questions_list_all'))

def upvote(request, question_id):

    # Check if question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        print("---Question does not exists---")
        return HttpResponseRedirect(reverse("questions_list_all"))

    # User should be logged in
    if request.user.is_authenticated:

        # User can only upvote a question once
        try:
            vote = Vote.objects.get(user=request.user, question=question)
        except Vote.DoesNotExist:
            print("Vote does not exist")
            vote = None

        # Create new upvote
        if vote is None:
            upvote = Vote(user=request.user, question=question, upvote=True)
            upvote.save()
            print("---Question Upvoted---")

        # Question is already voted
        else:
            if vote.upvote:
                print("---User can only upvote question once---")
                # User can oly upvote the question once
                # Redirect
            else: 
                vote.delete()
                print("---Downvote deleted---")

        update_total_votes(question)
        
    return HttpResponseRedirect(reverse("questions_list_all"))

def downvote(request, question_id):

    # Check if question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        print("---Question does not exists---")
        return HttpResponseRedirect(reverse("questions_list_all"))

    # User should be logged in
    if request.user.is_authenticated:

        # User can only upvote a question once
        try:
            vote = Vote.objects.get(user=request.user, question=question)
        except Vote.DoesNotExist:
            print("Vote does not exist")
            vote = None

        # Create new upvote
        if vote is None:
            downvote = Vote(user=request.user, question=question, upvote=False)
            downvote.save()
            print("---Question Downvoted---")

        # Question is already voted
        else:
            if vote.upvote:
                vote.delete()
                print("---Upvote deleted---")
            else: 
                print("---User can only downvote question once---")
                # User can oly upvote the question once
                # Redirect

        update_total_votes(question)
        
    return HttpResponseRedirect(reverse("questions_list_all"))

def bookmark(request, question_id):

    # Check if question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        print("---Question does not exists---")
        return HttpResponseRedirect(reverse("questions_list_all"))

    # User should be logged in
    if request.user.is_authenticated:

        # Check if question is already bookmarked
        try:
            bookmark = Bookmark.objects.get(user=request.user, question=question)
        except Bookmark.DoesNotExist:
            bookmark = None
    
        # Create bookmark
        if bookmark is None:
            bookmark = Bookmark(user=request.user, question=question)
            bookmark.save()
            print("---Bookmark has been created---")

        # Delete bookmark
        else:
            bookmark.delete()
            print("---Bookmark has been deleted---")

    
    return HttpResponseRedirect(reverse('questions_list_all'))
            
# ----- Answers Questions -----

def answer_new(request, question_id):
    print("---Create new Answer---")

    # Check if Question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        print("---Question does not exists---")
        return HttpResponseRedirect(reverse("question_show", kwargs={"question_id":question_id}))

    if request.method == "POST":
        form = NewAnswerForm(request.POST)

        # Valid form data
        if form.is_valid():
            body = form.cleaned_data["body"]
            question = question
            created_by = request.user
            
            new_answer = Answer(
                body=body, 
                question=question, 
                created_by=created_by)

            new_answer.save()
            print("---Succes: Answer Saved---")

    return HttpResponseRedirect(reverse("question_show", kwargs={"question_id":question_id}))


# ----- Helpers -----

def update_total_votes(question):
    upvotes = Vote.objects.filter(question=question, upvote = True).count()
    downvotes = Vote.objects.filter(question=question, upvote = False).count()
    question.total_votes = upvotes - downvotes 
    question.save()
    print(f"---Total votes: {upvotes} - {downvotes} = {question.total_votes}---")