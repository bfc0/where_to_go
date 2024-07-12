from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Place, Image
PREVIEW_WIDTH = PREVIEW_HEIGHT = 200


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ["preview"]
    fields = ["image", "preview"]

    def preview(self, obj):
        url = reverse('admin:places_image_change', args=[obj.id])
        return format_html(
            "<a href='{}'><img src='{}' style='max-width: {}px; max-height: {}px; object-fit: cover;' /></a>",
            url,
            obj.image.url,
            PREVIEW_WIDTH,
            PREVIEW_HEIGHT
        )


@admin.register(Place)
class PlacesAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    fields = ["title", "longitude", "latitude", "short_description",
              "long_description"]
    list_display = ["title", "longitude", "latitude", "short_description",
                    "long_description"]
    list_filter = ["title"]
    search_fields = ["title"]

    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    fields = ["image",  "place", "order", "preview"]
    list_display = ["preview", "place"]
    readonly_fields = ["preview"]
    autocomplete_fields = ["place"]
    search_fields = ["place__title"]

    def preview(self, obj):
        url = reverse('admin:places_image_change', args=[obj.id])
        return format_html(

            "<a href='{}'><img src='{}' style='max-width: {}px; max-height: {}px; object-fit: cover;' /></a>",
            url,
            obj.image.url,
            PREVIEW_WIDTH,
            PREVIEW_HEIGHT
        )
