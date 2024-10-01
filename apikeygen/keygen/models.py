from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid


class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Use timezone.now() to ensure expires_at is set correctly
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key
