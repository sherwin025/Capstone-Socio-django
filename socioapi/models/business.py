from tkinter import Menu
from django.db import models

class Business(models.Model):
    name = models.TextField()
    address = models.TextField()
    email = models.TextField()
    phone = models.PositiveBigIntegerField()
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    menu = models.ImageField(blank=True)
    zipcode = models.IntegerField()
    image = models.ImageField(blank=True)
    