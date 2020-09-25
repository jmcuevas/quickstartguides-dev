from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="question_new"),
    path("all", views.list_all, name="questions_list_all"),
    path("show/<int:question_id>", views.show, name="question_show"),
    path("edit/<int:question_id>", views.edit, name="question_edit"),
    path("update/<int:question_id>", views.update, name="question_update"),
    path("delete/<int:question_id>", views.delete, name="question_delete"),
    path("upvote/<int:question_id>", views.upvote, name="question_upvote"),
    path("downvote/<int:question_id>", views.downvote, name="question_downvote"),
    path("bookmark/<int:question_id>", views.bookmark, name="question_bookmark"),
]