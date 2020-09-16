from django.db import models

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length = 255)
    body = models.TextField()
    total_votes = models.IntegerField(default=0)
    # created_by = 
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    body = models.TextField()
    # created_by = 
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    # user = 
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='votes')
    upvote = models.BooleanField()

class Bookmark(models.Model):
    # user = 
    question = models.ForeignKey('Question' on_delete=models.CASCADE, related_name='bookmarks')

