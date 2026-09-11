import uuid
from django.db import models


class DiscoveryResponse(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        REVIEWED = "reviewed", "Reviewed"
        ARCHIVED = "archived", "Archived"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    company_name = models.CharField(max_length=160)
    contact_person = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(max_length=500, blank=True)
    answers = models.JSONField(default=dict)
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.SUBMITTED, db_index=True)
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"

    @property
    def priority_summary(self):
        return self.answers.get("urgent_priorities", "")

    @property
    def marketing_summary(self):
        return self.answers.get("content_focus", "") or self.answers.get("active_pages", "")

# Create your models here.
