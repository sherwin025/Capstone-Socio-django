from django.db import models
from django.utils import timezone

class MessageBoard(models.Model):
    content = models.CharField(max_length=200)
    community = models.ForeignKey("Community", on_delete=models.CASCADE)
    member = models.ForeignKey("Member", on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField( upload_to="messageboardimages", height_field=None, width_field=None, max_length=None, null=True)