from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField( max_length=100 )
    description = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True )
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.action