from django.db import models

class CommunityTag(models.Model):
    community = models.ForeignKey("Community", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    