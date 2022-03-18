from django.db import models
from django.utils import timezone

class BusinessAnnouncement(models.Model):
    business = models.ForeignKey("Business", on_delete=models.CASCADE)
    details = models.CharField(max_length=250)
    approved = models.BooleanField()
    image = models.ImageField( upload_to="businessannouncementimages", height_field=None, width_field=None, max_length=None, null=True)
    timestamp = models.DateTimeField(default=timezone.now)