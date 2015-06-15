# -*- conding:utf-8 -*-
from django.contrib import admin

from models import SchoolNode,Active,NetProtocol
# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ('nodeName','nodeIp')
    
admin.site.register(SchoolNode,NodeAdmin) #register SchoolNode

class ActiveAdmin(admin.ModelAdmin):
    list_display = ('id','startNode','endNode','createTime','protocol','bandwidth','delay','jitter','loss','congestion','avail')

admin.site.register(Active,ActiveAdmin)

class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('protocolName',)
    
admin.site.register(NetProtocol,ProtocolAdmin)