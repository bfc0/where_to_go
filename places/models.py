from enum import unique
from django.db import models
from django.urls import reverse


class Place(models.Model):
    title = models.CharField("Название", max_length=255, unique=True)
    short_description = models.TextField("Короткое описание", blank=True)
    long_description = models.TextField("Полное описание", blank=True)
    longitude = models.DecimalField(
        "Долгота", max_digits=16, decimal_places=14)
    latitude = models.DecimalField("Широта", max_digits=16, decimal_places=14)

    class Meta:
        unique_together = ("longitude", "latitude")

    def __str__(self):  # type:ignore
        return self.title

    def get_api_url(self):
        return reverse("details", args=[self.id])


class Image(models.Model):
    order = models.PositiveIntegerField(blank=True, db_index=True)
    place = models.ForeignKey(
        Place, related_name="imgs", verbose_name="Место", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Изображение {self.order} {self.place}"
