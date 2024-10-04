import uuid

from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime


class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    site_url = models.URLField(unique=True, blank=True, null=True)  # Made optional with blank=True and null=True
    validity_duration = models.PositiveIntegerField(default=86400)  # Validity in seconds (default: 24 hours)
    auto_set_expiration = models.BooleanField(default=True)  # Control flag for automatic expiration setting

    def save(self, *args, **kwargs):
        # Only set `expires_at` automatically if `auto_set_expiration` is True and not manually set
        if self.auto_set_expiration:
            if not self.expires_at or self._state.adding:
                self.expires_at = timezone.now() + timedelta(seconds=self.validity_duration)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"APIKey({self.key} for {self.site_url or 'No Site'}, expires at {self.expires_at})"

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
