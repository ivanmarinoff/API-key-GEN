from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid


class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)  # Allow manual setting of `expires_at`
    site_url = models.URLField(unique=True, blank=True, null=True)
    validity_duration = models.PositiveIntegerField(default=86400)  # Default: 24 hours in seconds
    auto_set_expiration = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # If auto_set_expiration is True, calculate based on validity_duration if not manually set
        if self.auto_set_expiration:
            if self.expires_at and not self._state.adding:
                # Calculate validity_duration from expires_at if expires_at is manually set
                time_diff = self.expires_at - timezone.now()
                self.validity_duration = int(time_diff.total_seconds())
            else:
                # Set expires_at based on validity_duration if expires_at isn't set
                self.expires_at = timezone.now() + timedelta(seconds=self.validity_duration)
        else:
            # If auto_set_expiration is False, ensure `expires_at` and `validity_duration` are manually set correctly
            if not self.expires_at:
                raise ValueError("Expiration time must be set if auto_set_expiration is disabled.")
            # Adjust validity_duration based on manually set expires_at
            time_diff = self.expires_at - timezone.now()
            self.validity_duration = int(time_diff.total_seconds())

        super().save(*args, **kwargs)

    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"APIKey({self.key} for {self.site_url or 'No Site'}, expires at {self.expires_at})"

# class CorsSettings(models.Model):
#     name = models.CharField(max_length=64, null=True, blank=True)
#     cors_allowed_origins = models.CharField(max_length=255, default=settings.CORS_ALLOWED_ORIGINS, null=True, blank=True)
#     cors_whitelist = models.CharField(max_length=255, default=settings.CORS_ORIGIN_WHITELIST, null=True, blank=True)
#
#     def __str__(self):
#         return self.name

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
