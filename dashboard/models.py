from django.db import models

# Create your models here.

class robotData(models.Model):
    checked_at = models.DateTimeField(auto_now_add=True)
    postime = models.CharField(max_length=20, null = True)
    robotPositionX = models.IntegerField()
    robotPositionY = models.IntegerField()
    
class robotData2(models.Model):
    postime = models.CharField(max_length=20, null = True)
    robotPositionX = models.IntegerField()
    robotPositionY = models.IntegerField()