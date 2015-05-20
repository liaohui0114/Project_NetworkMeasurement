'''
Created on Apr 24, 2015

@author: liaohui
'''
# -*- coding: utf-8 -*- 
from networkmeasurement.models import SchoolNode

class TableSchoolNode(object):
    '''
    classdocs
    '''


    def __init__(self, ip, name):
        '''
        Constructor
        '''
        self.ip = ip
        self.name = name
    def InsertNode(self):
        sn = SchoolNode()
        sn.nodeName = self.name
        sn.nodeIp = self.ip
        sn.save()
        