import os
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Imports every JSON file in a specified directory as Place"

    def add_arguments(self, parser):
        parser.add_argument(
            "directory", type=str, help="Directory containing JSON files"
        )

    def handle(self, *args, **options):
        directory = options["directory"]

        if not os.path.isdir(directory):
            self.stdout.write(self.style.ERROR(
                f"{directory} is not a valid directory"))
            return

        json_files = [f for f in os.listdir(directory) if f.endswith(".json")]

        if not json_files:
            self.stdout.write(
                self.style.WARNING(
                    f"No JSON files found in directory: {directory}")
            )
            return

        self.stdout.write("Starting import, this might take a while..")

        for json_file in json_files:
            place_filepath = os.path.join(directory, json_file)
            try:
                call_command("importplace", place_filepath)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to import {place_filepath}: {e}")
                )
