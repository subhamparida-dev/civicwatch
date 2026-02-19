from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Area(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Issue(models.Model):

    CATEGORY_CHOICES = [
        ('road', 'Road Issues'),
        ('water', 'Water Issues'),
        ('electricity', 'Electricity Issues'),
        ('sanitation', 'Sanitation Issues'),
        ('public_safety', 'Public Safety'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    severity = models.IntegerField(default=1)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    priority_score = models.IntegerField(default=0)

    def calculate_priority(self):
        days_open = 0
        if self.status != 'resolved':
            days_open = (timezone.now() - self.created_at).days
        return (self.severity * 4) + (days_open * 2)

    def save(self, *args, **kwargs):
        self.priority_score = self.calculate_priority()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
