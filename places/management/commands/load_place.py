import json
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile

from django.core.management.base import BaseCommand
from django.db import transaction
from places.models import Place, Image
from ._utils import fetch_image_content, fetch_json


class Command(BaseCommand):
    help = "Imports Place from JSON url"

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        url = options["url"]
        place = None

        try:
            serialized_place = fetch_json(url)

            with transaction.atomic():

                place, created = Place.objects.get_or_create(
                    title=serialized_place["title"],
                    defaults={
                        "short_description": serialized_place["description_short"],
                        "long_description": serialized_place["description_long"],
                        "longitude": serialized_place["coordinates"]["lng"],
                        "latitude": serialized_place["coordinates"]["lat"],
                    },
                )

                if not created:
                    self.stderr.write(
                        self.style.ERROR(f"Place {place.title} already exists")
                    )
                    return

                image_order = 1
                for url in serialized_place["imgs"]:
                    image_content = fetch_image_content(url)
                    if image_content is None:
                        self.stderr.write(
                            f"Failed to fetch an image for {place}")
                        continue

                    filename = urlparse(url).path.split("/")[-1]
                    image = Image(place=place, order=image_order)
                    image.image.save(filename, ContentFile(image_content))
                    image.save()
                    image_order += 1

        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"Error occurred: {e} for {place}"))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Place {place.title} imported successfully")
            )
