from django.db import models
from django.utils import timezone

class AnnouncementNotification(models.Model):
    Announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE)
    community_member = models.ForeignKey('CommunityMember', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField()