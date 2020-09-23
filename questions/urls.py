from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="question_new"),
    path("all", views.list_all, name="questions_list_all"),
    path("show/<int:question_id>", views.show, name="question_show"),
    path("edit/<int:question_id>", views.edit, name="question_edit"),
    path("update/<int:question_id>", views.update, name="question_update"),
]