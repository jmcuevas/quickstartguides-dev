from django.db import models
from users import models as user_models
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Guide(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = RichTextUploadingField()
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    division = models.CharField(max_length=100)
    collaborators = models.ManyToManyField(user_models.User, related_name="guides_collab", blank=True, null=True)
    created_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="guides")
    created_at = models.DateTimeField(auto_now_add=True)


