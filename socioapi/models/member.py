from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zipcode = models.IntegerField()
    parent = models.BooleanField()
    details = models.CharField(max_length=250)
    image = models.ImageField( upload_to="memberimages", height_field=None, width_field=None, max_length=None, null=True)
    