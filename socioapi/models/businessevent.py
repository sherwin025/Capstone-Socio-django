from django.db import models
from django.utils import timezone

class BusinessEvent(models.Model):
    business = models.ForeignKey("Business", on_delete=models.CASCADE)
    details = models.CharField(max_length=250)
    approved = models.BooleanField()
    date = models.DateField()
    time = models.TimeField()
    title = models.TextField()
    address = models.CharField(max_length=1000)
    image = models.ImageField( upload_to="businesseventimages", height_field=None, width_field=None, max_length=None, null=True)
    timestamp = models.DateTimeField(default=timezone.now)