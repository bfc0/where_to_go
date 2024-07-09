from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_places, name="places"),
    path("places/<int:id>/", views.details, name="details"),
]
