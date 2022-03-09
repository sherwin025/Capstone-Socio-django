from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=60)
    details = models.CharField(max_length=200)
    approved = models.BooleanField()
    community = models.ForeignKey("Community", on_delete=models.CASCADE)
    member = models.ForeignKey("Member", on_delete=models.SET_NULL, null=True)
    public = models.BooleanField()
    zipcode = models.IntegerField()
    comments = models.BooleanField()
    image = models.ImageField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)