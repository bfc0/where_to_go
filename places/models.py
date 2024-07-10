from enum import unique
from django.db import models
from django.urls import reverse


class Place(models.Model):
    title = models.CharField(max_length=255, unique=True)
    onmap_title = models.CharField(max_length=50)
    description_short = models.TextField()
    description_long = models.TextField()

    def __str__(self):
        return str(self.title)

    def get_api_url(self):
        return reverse("details", args=[self.id])


class Coordinates(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    lng = models.DecimalField(max_digits=16, decimal_places=14)
    lat = models.DecimalField(max_digits=16, decimal_places=14)

    class Meta:
        unique_together = ("lng", "lat")


class Image(models.Model):
    order = models.PositiveIntegerField()
    place = models.ForeignKey(Place, related_name="imgs", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image {self.order} for {self.place}"
