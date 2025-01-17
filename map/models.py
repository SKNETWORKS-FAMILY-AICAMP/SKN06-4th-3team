# account/models.py
from django.db import models

class pharmacy(models.Model):
    address = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    lat = models.FloatField()
    lng = models.FloatField()

