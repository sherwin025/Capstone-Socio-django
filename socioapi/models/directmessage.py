from django.db import models
from django.utils import timezone

class DirectMessage(models.Model):
    sender = models.ForeignKey('Member', on_delete=models.CASCADE)
    recipient = models.ForeignKey('Member', on_delete=models.CASCADE, related_name="recipient")
    content = models.CharField(max_length=1500)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=150)
    image = models.ImageField(blank=True)