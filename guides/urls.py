from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="guide_new"),
    path("show/<int:guide_id>", views.show, name="guide_show"),
]