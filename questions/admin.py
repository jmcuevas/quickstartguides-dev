from django.contrib import admin
from .models import Answer, Bookmark, Question, Vote

admin.site.register(Answer)
admin.site.register(Bookmark)
admin.site.register(Question)
admin.site.register(Vote)