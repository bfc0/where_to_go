from django.contrib import admin
from django.urls import path
from django.shortcuts import render


def placeholder(request):
    return render(request, "index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", placeholder, name="places"),
]
