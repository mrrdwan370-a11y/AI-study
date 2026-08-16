from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):

    RESOURCE_TYPES = [
        ("VIDEO", "Video"),
        ("ARTICLE", "Article"),
        ("DOCUMENTATION", "Documentation"),
        ("COURSE", "Course"),
        ("BOOK", "Book"),
        ("WEBSITE", "Website"),
        ("OTHER", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resources"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    link = models.URLField()

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        default="OTHER"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    