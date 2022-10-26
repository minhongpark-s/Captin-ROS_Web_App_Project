from django.db import models

# Create your models here.

class robotData(models.Model):
    checked_at = models.DateTimeField(auto_now_add=True)
    robotPositionX = models.IntegerField()
    robotPositionY = models.IntegerField()