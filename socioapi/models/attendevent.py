from django.db import models

class AttendEvent(models.Model):
    event = models.ForeignKey("CommunityEvent", on_delete=models.CASCADE, related_name="attendingevent")
    member = models.ForeignKey("Member", on_delete=models.CASCADE)