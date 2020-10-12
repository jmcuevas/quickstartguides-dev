from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="question_new"),
    path("all", views.list_all, name="questions_list_all"),
    path("bookmarked", views.list_bookmarked, name="questions_list_bookmarked"),
    path("show/<int:question_id>", views.show, name="question_show"),
    path("edit/<int:question_id>", views.edit, name="question_edit"),
    path("update/<int:question_id>", views.update, name="question_update"),
    path("delete/<int:question_id>", views.delete, name="question_delete"),
    path("upvote/<int:question_id>", views.upvote, name="question_upvote"),
    path("downvote/<int:question_id>", views.downvote, name="question_downvote"),
    path("bookmark/<int:question_id>", views.bookmark, name="question_bookmark"),
    path("<int:question_id>/answer/new", views.answer_new, name="answer_new"),
    path("answer/edit/<int:answer_id>", views.answer_edit, name="answer_edit"),
    path("answer/update/<int:answer_id>", views.answer_update, name="answer_update"),
    path("answer/delete/<int:answer_id>", views.answer_delete, name="answer_delete"),
]