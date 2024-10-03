import uuid

from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime


class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    site_url = models.URLField(unique=True, default='127.0.0.1')  # URL of the frontend site
    validity_duration = models.PositiveIntegerField(default=86400)  # Validity in seconds

    def is_valid(self):
        """Check if the API key is still valid."""
        return self.expires_at and self.expires_at > timezone.now()

    def save(self, *args, **kwargs):
        # Set `created_at` to current time if it is not already set
        if not self.created_at:
            self.created_at = timezone.now()

        # Calculate the expiration time based on `created_at` and `validity_duration`
        self.expires_at = self.created_at + timedelta(seconds=self.validity_duration)

        # Call the parent class's save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"APIKey({self.key} for {self.site_url}, expires at {self.expires_at})"

# class APIKey(models.Model):
#     key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()
#
#     def save(self, *args, **kwargs):
#         # Use timezone.now() to ensure expires_at is set correctly
#         if not self.expires_at:
#             self.expires_at = timezone.now() + timedelta(hours=24)
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.key
