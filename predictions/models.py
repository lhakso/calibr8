from django.db import models
import uuid

class Prediction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    probability = models.FloatField()  # 0.0 to 1.0
    created_at = models.DateTimeField(auto_now_add=True)
    resolve_by = models.DateTimeField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
    outcome = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.description[:50]} ({int(self.probability * 100)}%)"


class UserProfile(models.Model):
    name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name or "User Profile"
