from django.db import models

class CommunityMember(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    community = models.ForeignKey("Community", on_delete=models.CASCADE)
    admin = models.BooleanField()
    approved = models.BooleanField()

    