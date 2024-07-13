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


def json_from_url(url: str, tries=MAX_TRIES) -> dict:
    headers = {"Accept": "application/json"}
    for _ in range(tries):
        try:
            response = requests.get(url, headers=headers)
            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()

            if "text/plain" in response.headers.get("Content-Type"):
                content = response.content.decode(response.encoding or 'utf-8')
                return json.loads(content)

        except requests.exceptions.RequestException:
            continue
    raise Exception("Failed to fetch JSON data")


class Command(BaseCommand):
    help = "Imports Place from JSON file"

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        url = options["url"]
        place = None

        try:
            serialized_place = json_from_url(url)

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
                    self.stdout.write(
                        self.style.ERROR(f"Place {place.title} already exists")
                    )
                    return

                place.save()

                for idx, url in enumerate(serialized_place["imgs"], start=1):
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
