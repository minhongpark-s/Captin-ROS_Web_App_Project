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
    
class requestData(models.Model):
    requestPosition = models.IntegerField()
    requestMethod = models.IntegerField()
    requestTime = models.CharField(max_length=20, null = True)
    
class requestDelData(models.Model):
    requestPosition = models.IntegerField()
    requestMethod = models.IntegerField()
    requestTime = models.CharField(max_length=20, null = True)
    referenceStatus = models.CharField(max_length=20, null = True)
    MSTime = models.CharField(max_length=20, null = True)
    loadingReadyTime = models.CharField(max_length=20, null = True)
    loadedTime = models.CharField(max_length=20, null = True)
    MTUTime = models.CharField(max_length=20, null = True)
    URTime = models.CharField(max_length=20, null = True)
    UMTime = models.CharField(max_length=20, null = True)
    DRTime = models.CharField(max_length=20, null = True)
    FTime = models.CharField(max_length=20, null = True)