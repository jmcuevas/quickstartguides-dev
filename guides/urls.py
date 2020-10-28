from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="guide_new"),
    path("show/<int:guide_id>", views.show, name="guide_show"),
    path("all", views.list_all, name="guides_list_all"),
    path("edit/<int:guide_id>", views.edit, name="guide_edit"),
    path("update/<int:guide_id>", views.update, name="guide_update"),
    path("delete/<int:guide_id>", views.delete, name="guide_delete"),
]