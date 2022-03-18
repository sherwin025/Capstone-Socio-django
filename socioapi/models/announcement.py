from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=60)
    details = models.CharField(max_length=200)
    approved = models.BooleanField()
    community = models.ForeignKey("Community", on_delete=models.CASCADE, related_name="announcements")
    member = models.ForeignKey("Member", on_delete=models.SET_NULL, null=True)
    public = models.BooleanField()
    zipcode = models.IntegerField()
    comments = models.BooleanField()
    image = models.ImageField( upload_to="announcementimages", height_field=None, width_field=None, max_length=None, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    @property
    def comment_count(self):
        return self.__comment_count
    
    @comment_count.setter
    def comment_count(self, value):
        self.__comment_count = value