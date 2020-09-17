from django.db import models
from users import models as user_models

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length = 255)
    body = models.TextField()
    total_votes = models.IntegerField(default=0)
    created_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    body = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers")
    created_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="answers")
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="votes")
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='votes')
    upvote = models.BooleanField()

class Bookmark(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="bookmarks")
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='bookmarks')

