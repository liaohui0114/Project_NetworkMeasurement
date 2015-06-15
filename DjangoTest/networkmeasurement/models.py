# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from django.contrib import admin
# Create your models here.

#school node:
class SchoolNode(models.Model):
    nodeName = models.CharField(max_length=50)
    #nodeIp = models.CharField(max_length=16)
    nodeIp = models.IPAddressField() #alse char(15)

  
    def __unicode__(self):
        return self.nodeName

#protocol:TCP,UDP,ICMP,SNMP
class NetProtocol(models.Model):
    protocolName = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.protocolName

#to store active_networkMeasurement informations
class Active(models.Model):
    startNode = models.ForeignKey(SchoolNode,related_name="start_node")
    endNode = models.ForeignKey(SchoolNode,related_name="end_node")
    protocol = models.ForeignKey(NetProtocol)
    createTime = models.DateTimeField()
    bandwidth = models.FloatField(default=0)
    delay = models.FloatField(default=0)
    jitter = models.FloatField(default=0)
    loss = models.FloatField(default=0)
    congestion = models.BooleanField(default=False)
    avail = models.BooleanField(default=False)

class Passive(models.Model):
    startNode = models.ForeignKey(SchoolNode,related_name="passive_start_node")
    endNode = models.ForeignKey(SchoolNode,related_name="passive_end_node")
    createTime = models.DateTimeField()
    bandwidth = models.FloatField(default=0)
    throughput = models.FloatField(default=0)
    loss = models.FloatField(default=0)
    rtt = models.FloatField(default=0)
    cpu = models.FloatField(default=0)
    memory = models.FloatField(default=0)