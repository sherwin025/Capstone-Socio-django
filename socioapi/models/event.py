from django.db import models
from django.utils import timezone

class CommunityEvent(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    address = models.CharField(max_length=250)
    approved = models.BooleanField()
    community = models.ForeignKey("Community", on_delete=models.CASCADE, related_name='events')
    member = models.ForeignKey("Member", on_delete=models.SET_NULL, null=True)
    public = models.BooleanField()
    details = models.CharField(max_length=250)
    isactivity = models.BooleanField()
    zipcode = models.IntegerField()
    image = models.ImageField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    attendees = models.ManyToManyField("Member", through="AttendEvent", related_name="attending")
    
    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value
        
    @property
    def attending_count(self):
        return self.__attending_count
    
    @attending_count.setter
    def attending_count(self, value):
        self.__attending_count = value