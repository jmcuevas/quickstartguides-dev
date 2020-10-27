from django.db import models
from users import models as user_models
from taggit.managers import TaggableManager

# Create your models here.

class Guide(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    division = models.CharField(max_length=100)
    created_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="guides")
    created_at = models.DateTimeField(auto_now_add=True)


