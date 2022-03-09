from django.db import models
from django.utils import timezone

class Community(models.Model):
    name = models.CharField(max_length=250)
    public = models.BooleanField()
    visible = models.BooleanField()
    about = models.TextField()
    parentportal = models.BooleanField()
    createdby = models.ForeignKey("Member", on_delete=models.SET_NULL, null=True)
    rules = models.TextField()
    tags = models.ManyToManyField("Tag", through="CommunityTag", related_name="tags")
    image = models.ImageField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)