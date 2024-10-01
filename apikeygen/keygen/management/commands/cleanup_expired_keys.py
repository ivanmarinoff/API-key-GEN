from django.core.management.base import BaseCommand
from apikeygen.keygen.models import APIKey
from django.utils import timezone


class Command(BaseCommand):
    help = 'Delete all expired API keys'

    def handle(self, *args, **kwargs):
        # Delete keys whose expires_at is less than the current time
        expired_keys = APIKey.objects.filter(expires_at__lt=timezone.now())
        count, _ = expired_keys.delete()  # Delete and get count of deleted keys
        self.stdout.write(f"Deleted {count} expired keys.")
