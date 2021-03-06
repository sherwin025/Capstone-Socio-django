from django.db import models
from django.utils import timezone

class AnnouncementComment(models.Model):
    details = models.CharField(max_length=200)
    announcement = models.ForeignKey("Announcement", on_delete=models.CASCADE, related_name='thecomments')
    member = models.ForeignKey("Member", on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField( upload_to="announcementcommentimages", height_field=None, width_field=None, max_length=None, null=True)