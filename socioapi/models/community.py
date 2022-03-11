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
    
    
    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value
        
    @property
    def member_count(self):
        return self.__member_count
    
    @member_count.setter
    def member_count(self, value):
        self.__member_count = value
        
    @property
    def event_count(self):
        return self.__event_count
    
    @event_count.setter
    def event_count(self, value):
        self.__event_count = value
        
    @property
    def announcement_count(self):
        return self.__announcement_count
    
    @announcement_count.setter
    def announcement_count(self, value):
        self.__announcement_count = value