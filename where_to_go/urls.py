from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def placeholder(request):
    return HttpResponse("map placeholder")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", placeholder),
]
