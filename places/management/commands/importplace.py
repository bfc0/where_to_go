import json
import requests
from urllib.parse import urlparse
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.db import transaction
from places.models import Place, Image
MAX_TRIES = 3


def image_contents_from_url(url: str, tries=MAX_TRIES) -> bytes:
    for _ in range(tries):
        try:
            response = requests.get(url)
            if "image" in response.headers.get("Content-Type", ""):
                return response.content
        except requests.exceptions.RequestException:
            continue
    raise Exception("Failed to fetch data for image")


class Command(BaseCommand):
    help = "Imports Place from JSON file"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        filename = options["filename"]

        with open(filename, "r") as file:
            place_as_dict = json.load(file)

        try:
            with transaction.atomic():

                place, created = Place.objects.get_or_create(
                    title=place_as_dict["title"],
                    defaults={
                        "short_description": place_as_dict["description_short"],
                        "long_description": place_as_dict["description_long"],
                        "longitude": place_as_dict["coordinates"]["lng"],
                        "latitude": place_as_dict["coordinates"]["lat"],
                    },
                )

                if not created:
                    self.stdout.write(
                        self.style.ERROR(f"Place {place.title} already exists")
                    )
                    return

                place.save()

                for idx, url in enumerate(place_as_dict["imgs"], start=1):
                    img_content = image_contents_from_url(url)
                    filename = urlparse(url).path.split("/")[-1]

                    with NamedTemporaryFile(delete=True) as temp_file:
                        temp_file.write(img_content)
                        temp_file.flush()
                        image = Image(place=place, order=idx)
                        image.image.save(filename, temp_file)
                        image.save()

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error occurred: {e} for {place}"))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Place {place.title} imported successfully")
            )
