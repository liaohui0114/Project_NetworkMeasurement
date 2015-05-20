from django.contrib import admin

from models import SchoolNode
# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ('nodeName','nodeIp')
    
admin.site.register(SchoolNode,NodeAdmin) #register SchoolNode