from django.urls import path
from . import views

urlpatterns = [
    path("", views.placeholder, name="places"),
    path("places/<int:id>/", views.details, name="details"),
]
