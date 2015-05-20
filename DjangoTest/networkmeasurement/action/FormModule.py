#/usr/bin/env PYTHON
# -*- coding:utf-8 -*-

from django import forms
from django.forms import ModelForm
from networkmeasurement.models import SchoolNode
# 
# class UDPForm(forms.Form):
#  
#     print 'UDPForm Init!'
#     print 'UDPForm'
#     snAll = SchoolNode.objects.all()
#     nodeMsg = [ (sn.nodeIp,sn.nodeName) for sn in SchoolNode.objects.all() ]
#     print tuple(nodeMsg)
#     nodeChoice = tuple(nodeMsg)
#     print nodeChoice
#     startNode = forms.ChoiceField(widget=forms.Select,choices=nodeChoice)
#     endNode = forms.ChoiceField(widget=forms.Select,choices=nodeChoice)
#    it will be called only once,unless we put them in func __init()__

  
class UDPForm(forms.Form):
    def __init__(self):
        super(UDPForm,self).__init__()  #it's important,or we will get error no attribute fields  
        print 'UDPForm Init!'
        print 'UDPForm'
        snAll = SchoolNode.objects.all()
        nodeMsg = [ (sn.nodeIp,sn.nodeName) for sn in SchoolNode.objects.all() ]
        print tuple(nodeMsg)
        nodeChoice = tuple(nodeMsg)
        print nodeChoice
        startNode = forms.ChoiceField(widget=forms.Select,choices=nodeChoice)
        endNode = forms.ChoiceField(widget=forms.Select,choices=nodeChoice)
        self.fields['startNode'] = startNode # add line:super(UDPForm,self).__init__()
        self.fields['endNode'] = endNode    
    
  
# class UDPForm(ModelForm):
#     print 'UUDPFomr'
#     
#     class Meta:
#         model = SchoolNode
#         fields = ['nodeIp','nodeName']
