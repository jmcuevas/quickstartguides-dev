from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.urls import reverse

from django import forms
from .models import Guide

# ----- Forms -----

class NewGuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = [
            'title',
            'content',
            'tags',
        ]

    # Render Form elements with "form-control" class
    def __init__(self, *args, **kwargs):
        super(NewGuideForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

def index(request):
    return render(request, "guides/index.html")

def new(request):

    # Submit new guide Form
    if request.method == "POST":
        form = NewGuideForm(request.POST)
        
        # Valid form data
        if form.is_valid():
            new_guide = form.save(commit=False)
            new_guide.created_by = request.user
            new_guide.slug = slugify(new_guide.title)
        

            # Save guide
            new_guide.save()
            form.save_m2m() #Save Many-2-Many field in forms (tags)

            print("---Sucess: guide saved")

            # Pending redirect to guide_show
            # return(HttpResponseRedirect(reverse("guide_show", kwargs={'guide_id':new_guide.pk})))
            return HttpResponse("Form Saved")

        # Invalid form data
        else:
            print("Error: guide not Created")
            return HttpResponseRedirect(reverse("guide_new"))

    # Get request to guides/new
    else:
        if request.user.is_authenticated:
            return render(request, 'guides/new.html')
        else:
            return(HttpResponseRedirect(reverse("login")))

def show(request, guide_id):
    guide = get_object_or_404(Guide, pk=guide_id)

    return render(request, "guides/show.html", {
        "guide":guide })

def list_all(request):
    guides = get_list_or_404(Guide)
    # guides = Question.objects.all().order_by("-created_at")
    title = "All Guides"

    return render(request, "guides/list.html", 
    {"guides": guides,
    "title":title })