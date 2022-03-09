from django.db import models
from django.utils import timezone

class BusinessAnnouncement(models.Model):
    business = models.ForeignKey("Business", on_delete=models.CASCADE)
    details = models.CharField(max_length=250)
    approved = models.BooleanField()
    image = models.ImageField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)