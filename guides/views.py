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
            'description',
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

            
            return(HttpResponseRedirect(reverse("guide_show", kwargs={'guide_id':new_guide.pk})))
            

        # Invalid form data
        else:
            print("Error: guide not Created")
            return HttpResponseRedirect(reverse("guide_new"))

    # Get request to guides/new
    else:
        if request.user.is_authenticated:
            return render(request, 'guides/new.html', {"new_guide_form": NewGuideForm()})
        else:
            return(HttpResponseRedirect(reverse("login")))

def show(request, guide_id):
    guide = get_object_or_404(Guide, pk=guide_id)

    return render(request, "guides/show.html", {
        "guide":guide })

def list_all(request):
    # Check if guides list exists
    try:
        guides = Guide.objects.all().order_by("title")
    except Guide.DoesNotExist:
        print("---Guides list does not exist---")
        return HttpResponse("Error please try again")

    title = "All Guides"

    return render(request, "guides/list.html", 
    {"guides": guides,
    "title":title })

def edit(request, guide_id):

    # Check if guide exists
    try:
        guide = Guide.objects.get(pk=guide_id)
    except Guide.DoesNotExist:
        print("---Guide does not exist---")
        return HttpResponseRedirect(reverse("guides_list_all"))

    if request.user.is_authenticated and request.user == guide.created_by:
        tags_names = []
        for tag in guide.tags.all():
            tags_names.append(tag.name)

        form_data = {"title": guide.title, "description": guide.description, "content": guide.content, "tags":tags_names}
    
        return render(request, "guides/edit.html", {"guide":guide, "form":NewGuideForm(initial=form_data), "form_data":form_data})

    else:
        print("---User is not logged in or didn't created guide---")
        return HttpResponseRedirect(reverse("guides_list_all"))

def update(request, guide_id):

    # Check if Guide exists
    try:
        guide = Guide.objects.get(pk=guide_id)
    except Guide.DoesNotExist:
        print("---Guide does not exists---")
        return HttpResponseRedirect(reverse("guides_list_all"))

    # User should have created Guide to update
    if not (request.user == guide.created_by):
        print("---User didn't created guide")
        return HttpResponseRedirect(reverse("guides_list_all"))

    # User submited edit form
    if request.method == "POST":
        form = NewGuideForm(request.POST, instance=guide)

        # Validate form data & Save
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse("guide_show", kwargs={'guide_id': guide.pk}))

        else:
            print("---Guide data is not valid---")
            return HttpResponseRedirect(reverse("guides_list_all"))

    # Request method is other than POST
    else:
        print("---Method is not post---")
        return HttpResponseRedirect(reverse("guides_list_all"))

def delete(request, guide_id):
    # Check if guide exists
    try:
        guide = Guide.objects.get(pk=guide_id)
    except Guide.DoesNotExist:
        print("---Guide does not exists---")
        return HttpResponseRedirect(reverse("guides_list_all"))

    # User should have created Guide to update
    if not (request.user == guide.created_by):
        print("---User didn't created guide")
        return HttpResponseRedirect(reverse("guides_list_all"))

    # User clicked on Delete button (Post request)
    if request.method == "POST":
        print("---Guide deleted---")
        guide.delete()
    else:
        print("---Guides views.delete: not POST method---")

    return HttpResponseRedirect(reverse('guides_list_all'))

def search(request):
    if request.method == "GET":
        search_term = request.GET['search_term']
        guides = Guide.objects.filter(title__icontains=search_term).order_by("-created_at")
        title = "Search results for: '" + search_term + "'"

        return render(request, "guides/list.html", 
            {"guides": guides,
            "title":title })
    else:
        return HttpResponseRedirect(reverse("guides_list_all"))