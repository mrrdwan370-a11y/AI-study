from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]
    user = models.ForeignKey(  User, on_delete=models.CASCADE, related_name="tasks" )
    title = models.CharField(  max_length=200  )
    description = models.TextField( blank=True)
    due_date = models.DateTimeField( null=True,  blank=True )
    priority = models.CharField( max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM" )
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default="PENDING" )
    ai_solution = models.TextField( blank=True, null=True )
    created_at = models.DateTimeField( auto_now_add=True  )
    updated_at = models.DateTimeField( auto_now=True )
    class Meta:
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        return self.title