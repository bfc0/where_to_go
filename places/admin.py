from django.contrib import admin
from .models import Place, Image, Coordinates


class CoordinatesInline(admin.StackedInline):
    model = Coordinates
    can_delete = False
    verbose_name_plural = Coordinates


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin):
    inlines = [CoordinatesInline, ImageInline]
    list_display = ["title", "description_short", "description_long"]
