from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Place, Image, Coordinates


class CoordinatesInline(admin.StackedInline):
    model = Coordinates
    can_delete = False
    verbose_name_plural = Coordinates


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ["preview"]
    fields = ["image", "preview", "order"]

    def preview(self, obj):
        return format_html(
            '<img src="{}" style="width: 200px; height: 200px; object-fit: cover;" />',
            obj.image.url,
        )


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin):
    inlines = [CoordinatesInline, ImageInline]
    list_display = ["title", "description_short", "description_long"]
