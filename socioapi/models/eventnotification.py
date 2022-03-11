from django.db import models
from django.utils import timezone

class EventNotification(models.Model):
    event = models.ForeignKey('CommunityEvent', on_delete=models.CASCADE)
    community_member = models.ForeignKey('CommunityMember', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField()