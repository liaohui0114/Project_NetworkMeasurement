from django.db import models
from django.db import connection
from django.contrib import admin
# Create your models here.

class SchoolNode(models.Model):
    nodeName = models.CharField(max_length=50)
    #nodeIp = models.CharField(max_length=16)
    nodeIp = models.IPAddressField() #alse char(15)

  
    def __unicode__(self):
        return self.nodeName