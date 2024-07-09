from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def placeholder(request):
    print("heello")
    return render(request, "index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("places.urls")),
]
