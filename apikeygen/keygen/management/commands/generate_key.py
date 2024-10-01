from django.core.management.base import BaseCommand
from apikeygen.keygen.models import APIKey


class Command(BaseCommand):
    help = 'Generate a new API key and store it in the database'

    def handle(self, *args, **kwargs):
        # Create a new API key and save it to the database
        new_key = APIKey.objects.create()
        self.stdout.write(f"New API key generated successfully: {new_key.key}")
