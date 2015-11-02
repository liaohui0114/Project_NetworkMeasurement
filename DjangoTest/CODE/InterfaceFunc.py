#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from GlobleVariable import *
import string
import numpy
import socket
import time
import threading
import sys
import os
from SocketModule import *
from multiprocessing import Process
from subprocess import *
#import MySQLdb
#####UDP Thread######
'''
SCHOOLIP = {'10.255.249.42':'上海交通大学',
            '10.255.249.14':'上海交通大学',
            '10.255.249.10':'上海交通大学',
            '10.255.249.26':'上海交通大学',
            '10.255.249.38':'上海交通大学',
            '10.255.249.6':'上海交通大学',
            '10.255.249.34':'上海交通大学',
            '10.255.249.22':'上海交通大学',
            '10.255.249.2':'上海交通大学',
            '10.255.249.18':'上海交通大学',
            '10.255.249.25':'复旦医学院',
            '10.255.249.214':'复旦医学院',
            '10.255.249.213':'交大医学院',
            '10.255.249.54':'交大医学院',
            '10.255.249.30':'华东理工大学',
            '10.255.249.122':'华东理工大学',
            '10.255.249.121':'紫竹高科园区',
            '10.255.249.9':'紫竹高科园区',
            '10.255.249.113':'紫竹高科园区',
            '10.255.249.125':'紫竹高科园区',
            '10.255.249.133':'紫竹高科园区',
            '10.255.249.130':'紫竹高科园区',
            '10.255.249.118':'紫竹高科园区',
            '10.255.249.2':'科大',
            '10.255.249.138':'科大',
            #'10.255.249.1':'张江高科园区',
            '10.255.249.161':'张江高科园区',
            '10.255.249.173':'张江高科园区',
            '10.255.249.169':'张江高科园区',
            '10.255.249.49':'张江高科园区',
            '10.255.249.172':'第二工业大学',
            '10.255.249.225':'第二工业大学',
            '10.255.250.186':'第二工业大学',
            '10.255.249.17':'上海师范大学',
            '10.255.249.146':'上海师范大学',
            '10.255.249.98':'华东师范大学',
            '10.255.249.93':'华东师范大学',
            '10.255.249.73':'华东师范大学',
            '10.255.249.101':'华东师范大学',
            '10.255.249.110':'华东师范大学',
            '10.255.249.1':'华东师范大学',
            '10.255.249.21':'东华大学',
            '10.255.249.97':'东华大学',
            '10.255.249.94':'上海大学',
            '10.255.249.141':'上海大学',
            '10.255.249.142':'上海财经大学',
            '10.255.249.82':'上海财经大学',
            '10.255.249.81':'复旦大学',
            '10.255.249.74':'复旦大学',
            '10.255.249.85':'复旦大学',
            '10.255.249.90':'复旦大学',
            '10.255.249.77':'复旦大学',
            '10.255.249.46':'复旦大学',
            '10.255.249.78':'同济大学',
            '10.255.249.218':'同济大学',
            
            '10.255.249.13':'上外',
            '10.255.249.114':'上外',
            '10.255.249.185':'上外',
            '10.255.249.189':'上外',
            '10.255.250.181':'上外',
            '10.255.249.153':'奉贤大学园区',
            '10.255.249.229':'奉贤大学园区',
            '10.255.249.150':'临港大学园区',
            '10.255.249.149':'临港大学园区',
            '10.255.249.158':'南汇大学园区',
            '10.255.249.157':'南汇大学园区',
            '10.255.249.117':'南汇大学园区',
            '10.255.249.165':'南汇大学园区',
            '10.255.249.162':'南汇大学园区',
            '10.255.249.137':'国际医学园区',
            '10.255.249.221':'国际医学园区',
            '10.255.249.174':'国际医学园区',
            
            '10.255.249.53':'市教委远教',
            '10.255.249.50':'市教委远教',
            '10.255.249.69':'市教委远教',
            '10.255.249.57':'市教委远教',
            '10.255.249.45':'市教委远教',
            '10.255.249.61':'市教委远教',
            '10.255.249.5':'市教委远教',
            '10.255.249.65':'市教委远教',
            '10.255.250.185':'市教委远教',
            
            '10.255.250.182':'松江大学园区',
            '10.255.249.194':'松江大学园区',
            '10.255.249.193':'松江教育',
            '10.255.249.126':'松江教育',
            '10.255.249.134':'金山教育',
            '10.255.249.230':'金山教育',
            '10.255.249.129':'奉贤教育',
            '10.255.249.154':'奉贤教育',
            '10.255.249.166':'浦东教育',
            '10.255.249.222':'浦东教育',
            '10.255.249.41':'闵行教育',
            '10.255.249.190':'闵行教育',
            '10.255.249.70':'崇明教育',
            '10.255.249.226':'崇明教育',
            '10.255.249.37':'徐汇教育',
            '10.255.249.210':'徐汇教育',
            '10.255.249.209':'黄浦教育',
            '10.255.249.66':'黄浦教育',
            '10.255.249.186':'青浦教育',
            '10.255.249.197':'青浦教育',
            '10.255.249.33':'静安教育',
            '10.255.249.206':'静安教育',
            '10.255.249.205':'虹口教育',
            '10.255.249.62':'虹口教育',
            '10.255.249.58':'杨浦教育',
            '10.255.249.217':'杨浦教育',
            '10.255.249.145':'长宁教育',
            '10.255.249.106':'长宁教育',
            '10.255.249.102':'普陀教育',
            '10.255.249.177':'普陀教育',
            '10.255.249.178':'闸北教育',
            '10.255.249.86':'闸北教育',
            '10.255.249.89':'宝山教育',
            '10.255.249.202':'宝山教育',
            '10.255.249.201':'嘉定教育',
            '10.255.249.109':'嘉定教育',
            '10.255.249.198':'嘉定教育',         
            }
'''
SCHOOLIP = {'10.255.250.1':'张江高科',
            '10.255.251.1':'张江高科',
            '10.2.1.254':'张江高科',
            '10.255.249.49':'张江高科',
            '10.255.249.161':'张江高科',
            '10.255.249.169':'张江高科',
            '10.255.249.1':'张江高科',
            '10.255.1.9':'张江高科',
            '10.255.1.177':'张江高科',
            '10.255.1.5':'张江高科',
            '10.255.1.17 ':'张江高科',
            '10.255.1.13':'张江高科',
            '192.168.249.5':'张江高科',
            '192.168.249.9':'张江高科',
            '192.168.249.13':'张江高科',
            
            '10.255.250.3':'浦东教育',
            '10.255.251.3':'浦东教育',
            '10.2.3.254':'浦东教育',
            '10.255.249.166':'浦东教育',
            '10.255.249.222':'浦东教育',
            '10.136.1.1':'浦东教育',
            
            '10.255.250.4':'南汇园区',
            '10.255.251.4':'南汇园区',
            '10.2.4.254':'南汇园区',
            '10.255.249.162':'南汇园区',
            '10.255.249.117':'南汇园区',
            '10.255.249.157':'南汇园区',
            '10.255.249.165':'南汇园区',
            '10.255.4.1':'南汇园区',
            '10.255.4.5':'南汇园区',
            
            '10.255.250.7':'奉贤教育',
            '10.255.251.7':'奉贤教育',
            '10.2.7.254':'奉贤教育',
            '10.255.249.129':'奉贤教育',
            '10.255.249.154':'奉贤教育',
            '10.152.1.1':'奉贤教育',
            
            '10.255.250.8':'金山教育',
            '10.255.251.8':'金山教育',
            '10.2.8.254':'金山教育',
            '10.255.249.134':'金山教育',
            '10.255.249.230':'金山教育',
            '192.168.3.1':'金山教育',
            
            '10.255.250.9':'紫竹园区',
            '10.255.251.9':'紫竹园区',
            '10.2.9.254':'紫竹园区',
            '10.255.249.9':'紫竹园区',
            '10.255.249.118':'紫竹园区',
            '10.255.249.130':'紫竹园区',
            '10.255.9.17':'紫竹园区',
            '10.255.249.125':'紫竹园区',
            '10.255.249.133':'紫竹园区',
            '10.255.249.113':'紫竹园区',
            '10.255.249.121':'紫竹园区',
            '10.255.9.5':'紫竹园区',
            '10.255.9.9':'紫竹园区',
            '10.255.9.21':'紫竹园区',
            '10.251.255.1':'紫竹园区',
            '10.255.9.14':'紫竹园区',
            '10.254.4.1':'紫竹园区',
            '219.228.31.1':'紫竹园区',
            '192.168.249.45':'紫竹园区',
            '192.168.249.49':'紫竹园区',
            
            '10.255.250.10':'松江教育',
            '10.255.251.10':'松江教育',
            '10.2.10.254':'松江教育',
            '10.255.249.193':'松江教育',
            '10.255.249.126':'松江教育',
            '10.160.3.1':'松江教育',
            '192.168.249.53':'松江教育',
            '10.255.10.1':'松江教育',
            
            '10.255.250.12':'闵行教育',
            '10.255.251.12':'闵行教育',
            '10.2.12.254':'闵行教育',
            '10.255.249.41':'闵行教育',
            '10.255.249.190':'闵行教育',
            '192.168.195.137':'闵行教育',
            '192.168.249.157':'闵行教育',
            '192.168.249.161':'闵行教育',
            
            '10.255.38.1':'交通大学',
            '10.255.38.253':'交通大学',
            '10.255.13.5':'交通大学',
            '10.255.250.13':'交通大学',
            '10.255.251.13':'交通大学',
            '10.2.13.254':'交通大学',
            '10.255.249.10':'交通大学',
            '10.255.249.6':'交通大学',
            '10.255.249.42':'交通大学',
            '202.112.27.69':'交通大学',
            '10.255.249.14':'交通大学',
            '10.255.249.253':'交通大学',
            '10.255.249.26':'交通大学',
            '10.255.249.38':'交通大学',
            '10.255.249.22':'交通大学',
            '10.255.249.29':'交通大学',
            '10.255.249.18':'交通大学',
            '10.255.249.34':'交通大学',
            '10.255.248.241':'交通大学',
            '10.255.248.245':'交通大学',
            '192.168.249.177':'交通大学',
            '10.255.64.1':'交通大学',
            '10.255.13.1':'交通大学',
            '202.112.28.1':'交通大学',
            '202.112.27.230':'交通大学',
            '10.255.249.241':'交通大学',
            '10.255.13.9':'交通大学',
            '10.255.249.245':'交通大学',
            '10.255.248.1':'交通大学',
            '10.255.248.5':'交通大学',
            
            '10.255.250.15':'长宁教育',
            '10.255.251.15':'长宁教育',
            '10.2.15.254':'长宁教育',
            '10.255.249.106':'长宁教育',
            '10.255.249.145':'长宁教育',
            '10.80.1.3':'长宁教育',
            
            '10.255.16.1':'华师大',
            '10.255.250.16':'华师大',
            '10.255.251.16':'华师大',
            '10.2.16.254':'华师大',
            '10.255.249.254':'华师大',
            '10.255.249.73':'华师大',
            '10.255.249.93':'华师大',
            '10.255.249.101':'华师大',
            '10.255.249.110':'华师大',
            '10.255.249.105':'华师大',
            '10.255.249.98':'华师大',
            '10.255.16.5':'华师大',
            
            '10.255.250.17':'普陀教育',
            '10.255.251.17':'普陀教育',
            '10.2.17.254':'普陀教育',
            '10.255.249.177':'普陀教育',
            '10.255.249.102':'普陀教育',
            '10.88.255.253':'普陀教育',
            '192.168.249.109':'普陀教育',
            '192.168.249.113':'普陀教育',
            '192.168.249.117':'普陀教育',
            '10.255.17.5':'普陀教育',
            '192.168.254.233':'普陀教育',
            '192.168.4.29':'普陀教育',
            
            '10.255.250.18':'闸北教育',
            '10.255.251.18':'闸北教育',
            '10.2.18.254':'闸北教育',
            '10.255.249.86':'闸北教育',
            '10.255.249.178':'闸北教育',
            '192.168.3.21':'闸北教育',
            
            '10.255.250.19':'复旦大学',
            '10.255.251.19':'复旦大学',
            '10.2.19.254':'复旦大学',
            '10.255.249.46':'复旦大学',
            '10.255.249.74':'复旦大学',
            '10.255.249.77':'复旦大学',
            '10.255.249.90':'复旦大学',
            '10.255.249.85':'复旦大学',
            '10.255.249.81':'复旦大学',
            '10.255.19.1':'复旦大学',
            '10.255.19.33':'复旦大学',
            '10.255.249.233':'复旦大学',
            '10.255.19.5':'复旦大学',
            '10.255.19.21':'复旦大学',
            '10.255.19.17':'复旦大学',
            '192.168.249.97':'复旦大学',
            '192.168.249.89':'复旦大学',
            '192.168.249.85':'复旦大学',
            
            '10.255.250.21':'杨浦教育',
            '10.255.251.21':'杨浦教育',
            '10.2.21.254':'杨浦教育',
            '10.255.249.58':'杨浦教育',
            '10.255.249.217':'杨浦教育',
            '192.168.3.29':'杨浦教育',
            
            '10.255.250.22':'远程教育',
            '10.255.251.22':'远程教育',
            '10.2.22.254':'远程教育',
            '192.168.99.2':'远程教育',
            '10.255.249.5':'远程教育',
            '10.255.249.45':'远程教育',
            '10.255.249.53':'远程教育',
            '10.255.249.65':'远程教育',
            '10.255.249.61':'远程教育',
            '10.255.249.57':'远程教育',
            '10.255.249.237':'远程教育',
            '10.255.38.249':'远程教育',
            '10.255.22.1':'远程教育',
            '10.255.22.5':'远程教育',
            '192.168.249.77':'远程教育',
            '192.168.249.81':'远程教育',
            '10.249.0.254':'远程教育',
            '10.255.250.185':'远程教育',
            '10.255.249.50':'远程教育',
            
            '10.255.250.23':'崇明教育',
            '10.255.251.23':'崇明教育',
            '10.2.23.254':'崇明教育',
            '10.255.249.226':'崇明教育',
            '192.168.200.18':'崇明教育',
            
            '10.255.250.25':'青浦教育',
            '10.255.251.25':'青浦教育',
            '10.2.25.254':'青浦教育',
            '10.255.249.197':'青浦教育',
            '10.144.254.58':'青浦教育',
            '10.255.249.186':'青浦教育',
            '192.168.254.229':'青浦教育',
            '10.255.25.1':'青浦教育',
            
            '10.255.250.26':'嘉定教育',
            '10.255.251.26':'嘉定教育',
            '10.2.26.254':'嘉定教育',
            '10.255.249.201':'嘉定教育',
            '10.255.249.109':'嘉定教育',
            '10.255.249.198':'嘉定教育',
            '10.254.254.41':'嘉定教育',
            '10.255.26.1':'嘉定教育',
            '192.168.249.57':'嘉定教育',
            '10.112.1.1':'嘉定教育',
            '192.168.249.209':'嘉定教育',
            
            '10.255.250.27':'宝山教育',
            '10.255.251.27':'宝山教育',
            '10.2.27.254':'宝山教育',
            '192.168.99.1':'宝山教育',
            '10.255.249.89':'宝山教育',
            '10.255.249.202':'宝山教育',
            '192.168.13.1':'宝山教育',
            '10.254.254.45':'宝山教育',
            '192.168.249.65':'宝山教育',
            '10.255.27.5':'宝山教育',
            '10.255.27.1':'宝山教育',
            '192.168.249.69':'宝山教育',
            
            '10.255.250.31':'静安教育',
            '10.255.251.31':'静安教育',
            '10.2.31.254':'静安教育',
            '10.255.249.206':'静安教育',
            '10.255.249.33':'静安教育',
            '192.168.178.73':'静安教育',
            '192.168.249.129':'静安教育',
            '192.168.254.213':'静安教育',
            '10.255.31.1':'静安教育',
            '192.168.254.201':'静安教育',
            '10.255.31.5':'静安教育',
            
            '10.255.250.32':'虹口教育',
            '10.255.251.32':'虹口教育',
            '10.2.32.254':'虹口教育',
            '10.255.249.62':'虹口教育',
            '10.255.249.205':'虹口教育',
            '10.254.254.57':'虹口教育',
            '10.62.1.1':'虹口教育',
            '192.168.254.225':'虹口教育',
            
            '10.255.250.33':'徐汇教育',
            '10.255.251.33':'徐汇教育',
            '10.2.33.254':'徐汇教育',
            '10.255.249.210':'徐汇教育',
            '10.255.249.37':'徐汇教育',
            '10.255.254.37':'徐汇教育',
            '192.168.1.49':'徐汇教育',
            '10.255.33.1':'徐汇教育',
            '10.255.33.5':'徐汇教育',
            '192.168.249.149':'徐汇教育',
            
            '10.255.250.34':'黄浦教育',
            '10.255.251.34':'黄浦教育',
            '10.2.34.254':'黄浦教育',
            '10.255.249.66':'黄浦教育',
            '10.255.249.209':'黄浦教育',
            '192.168.113.17':'黄浦教育',
            '192.168.249.141':'黄浦教育',
            
            '10.255.250.44':'松江上外',
            '10.255.251.44':'松江上外',
            '10.2.44.254':'松江上外',
            '10.255.249.13':'松江上外',
            '10.255.249.189':'松江上外',
            '10.255.249.114':'松江上外',
            '10.255.250.181':'松江上外',
            '10.255.44.17':'松江上外',
            '10.255.249.185':'松江上外',
            
            
            '10.255.249.137':'国际医学',
            '10.255.249.157':'国际医学',
            '10.255.2.1':'国际医学',
            '10.255.250.2':'国际医学',
            '10.255.251.2':'国际医学',
            
            '10.255.249.149':'临港园区',
            '10.255.5.9':'临港园区',
            '10.255.5.5':'临港园区',
            '10.255.5.17':'临港园区',
            '10.255.249.158':'临港园区',
            '10.255.5.1':'临港园区',
            '10.255.250.5':'临港园区',
            '10.255.251.5':'临港园区',
            '10.2.5.254':'临港园区',
        
            '10.255.249.229':'奉贤园区',
            '10.255.6.129':'奉贤园区',
            '10.255.6.1':'奉贤园区',
            '10.255.6.9':'奉贤园区',
            '192.168.249.33':'奉贤园区',
            '10.255.249.153':'奉贤园区',
            '10.255.249.150':'奉贤园区',
            '10.255.6.5':'奉贤园区',
            '10.255.250.6':'奉贤园区',
            '10.255.251.6':'奉贤园区',
            
            '192.168.0.1':'松江园区',
            '10.255.11.25':'松江园区',
            '10.255.11.1':'松江园区',
            '10.255.11.21':'松江园区',
            '10.255.11.13':'松江园区',
            '10.255.11.9':'松江园区',
            '10.255.11.5':'松江园区',
            '10.255.11.33':'松江园区',
            '10.255.11.37':'松江园区',
            '10.255.11.45':'松江园区',
            '10.255.11.29':'松江园区',
            '10.255.11.41':'松江园区',
            '10.255.11.49':'松江园区',
            '10.255.249.114':'松江园区',
            '10.255.249.194':'松江园区',
            '10.255.250.182':'松江园区',
            '10.255.250.11':'松江园区',
            '10.255.251.11':'松江园区',
            
            '10.255.249.146':'上师大',
            '10.255.249.17':'上师大',
            '10.255.14.17':'上师大',
            '10.255.14.21':'上师大',
            '192.168.10.81':'上师大',
            '10.255.249.249':'上师大',
            '10.255.14.1':'上师大',
            '10.255.14.5':'上师大',
            '10.255.14.9':'上师大',
            '10.255.14.13':'上师大',
            '10.255.14.25':'上师大',
            '192.168.249.153':'上师大',
            '10.255.250.14':'上师大',
            '10.2.14.254':'上师大',
            
            '10.255.249.218':'同济大学',
            '10.255.20.1':'同济大学',
            '10.255.20.9':'同济大学',
            '10.255.20.25':'同济大学',
            '10.255.20.5':'同济大学',
            '10.255.20.21':'同济大学',
            '10.255.20.17':'同济大学',
            '10.255.20.13':'同济大学',
            '192.168.249.121':'同济大学',
            '10.255.0.2':'同济大学',
            '10.255.20.101':'同济大学',
            '10.255.20.129':'同济大学',
            '10.255.249.78':'同济大学',
            '10.255.250.20':'同济大学',
            '10.255.251.20':'同济大学',
            
            '10.255.249.170':'二工大',
            '10.255.250.186':'二工大',
            '10.255.24.1':'二工大',
            '10.255.24.9':'二工大',
            '10.255.24.13':'二工大',
            '192.168.249.137':'二工大',
            '192.168.249.133':'二工大',
            '10.255.24.101':'二工大',
            '10.255.24.5':'二工大',
            '10.255.249.225':'二工大',
            '10.255.250.24':'二工大',
            '10.255.251.24':'二工大',
            
            '10.255.249.141':'上海大学',
            '10.255.249.94':'上海大学',
            '192.168.254.1':'上海大学',
            '10.255.28.1':'上海大学',
            '10.255.28.5':'上海大学',
            '10.254.254.5':'上海大学',
            '10.255.28.9':'上海大学',
            '10.255.28.81':'上海大学',
            '192.168.249.165':'上海大学',
            '192.168.249.169':'上海大学',
            '10.255.250.28':'上海大学',
            ' 10.2.28.254':'上海大学',
            
            '110.255.249.82':'财经大学',
            '10.255.249.142':'财经大学',
            '10.255.200.1':'财经大学',
            '192.168.254.241':'财经大学',
            '10.255.29.5':'财经大学',
            '10.255.29.1':'财经大学',
            '10.255.250.29':'财经大学',
            
            '10.255.249.97':'东华大学',
            '10.255.30.1':'东华大学',
            '10.255.30.5':'东华大学',
            '10.255.30.9':'东华大学',
            '10.255.30.13':'东华大学',
            '10.255.30.17':'东华大学',
            '10.255.30.21':'东华大学',
            '10.255.30.101':'东华大学',
            '10.255.249.21':'东华大学',
            '10.255.250.30':'东华大学',
            '10.255.251.30':'东华大学',
            '10.2.30.254':'东华大学',
            
            
            '10.255.35.81':'复旦医学院',
            '10.255.35.5':'复旦医学院',
            '10.255.249.214':'复旦医学院',
            '10.255.249.25':'复旦医学院',
            '10.255.35.129':'复旦医学院',
            '10.255.35.1':'复旦医学院',
            '10.255.250.35':'复旦医学院',
            
            '10.255.249.54':'交大医学院',
            '10.255.249.213':'交大医学院',
            '10.255.36.1':'交大医学院',
            '192.168.5.1':'交大医学院',
            '10.255.36.9':'交大医学院',
            '192.168.249.125':'交大医学院',
            '10.255.36.41':'交大医学院',
            '202.120.201.217':'交大医学院',
            '202.120.201.177':'交大医学院',
            '10.255.36.17':'交大医学院',
            '10.255.36.5':'交大医学院',
            '10.255.36.33':'交大医学院',
            '58.195.83.177':'交大医学院',
            '10.255.96.1':'交大医学院',
            '10.255.250.36':'交大医学院',
            '10.2.36.254':'交大医学院',
            
            '10.255.249.30':'华东理工',
            '10.255.37.1':'华东理工',
            '10.255.37.5':'华东理工',
            '10.255.37.17':'华东理工',
            '10.255.37.9':'华东理工',
            '58.195.87.161':'华东理工',
            '10.255.37.13':'华东理工',
            '192.168.249.181':'华东理工',
            '192.168.249.185':'华东理工',
            '192.168.249.189':'华东理工',
            '192.168.249.193':'华东理工',
            '10.255.37.21':'华东理工',
            '192.168.249.197':'华东理工',
            '10.255.249.122':'华东理工',
            '10.255.250.37':'华东理工',
            '10.255.251.37':'华东理工',
            
            '10.255.249.238':'有孚节点',
            '10.255.249.234':'有孚节点',
            '10.255.248.9':'有孚节点',
            '192.168.89.254':'有孚节点',
            '10.255.40.2':'有孚节点',
            '10.255.40.9':'有孚节点',
            '10.0.1.65':'有孚节点',
            '202.121.2.249':'有孚节点',
            '192.168.254.245':'有孚节点',
            '10.0.0.254':'有孚节点',
            '192.168.254.234':'有孚节点',
            '192.168.254.253':'有孚节点',
            '192.168.254.237':'有孚节点',
            '10.255.250.40':'有孚节点',
            '10.2.40.254':'有孚节点',
            
            '10.255.248.2':'专网互通',
            '10.255.249.242':'专网互通',
            '10.255.248.6':'专网互通',
            '10.255.250.41':'专网互通',
            
            '10.255.249.246':'中运指挥中心',
            '192.168.254.249':'中运指挥中心',
            '10.254.254.1':'中运指挥中心',
            '10.255.250.42':'中运指挥中心',
            
            
            '10.255.249.50':'上海科大',
            '10.255.249.61':'上海科大',
            '10.255.249.2':'上海科大',
            '10.255.249.5':'上海科大',
            '10.255.45.1':'上海科大',
            '10.255.249.138':'上海科大',
            '10.255.250.45':'上海科大',

            }     

def UDPThread_Iperf(ip,sendMsg):
    print 'UDPThread_Iperf:start iperf'
    filename = 'temp_udp_iperf_' + str(int(time.time()*1000))+'.txt'
    #os.system('iperf -u -c %s -t 5 -i 1 -b 10000M> udpfile.txt'%ip)
    os.system('iperf -u -c %s -t 1 -i 0.5 -b 50M -p 10009> %s'%(ip,filename))  #40M is close to thresh_hold
    print 'end iperf'
    msg = ReadIperfUDPFile(filename)
    
    for key,value in msg.items():
        sendMsg[key] = value #update info like: bandwidth,loss,jitter and so on
    #print 'udp iperf,',sendMsg
    
    os.system('sudo rm -rf %s'%filename)
    
'''   
def UDPThread_Delay(ip,sendMsg):
    print 'UDPThread_Iperf:start get delay info'
    #get delay info
    ud = UDPClient(ip,SOCKET_UDP_PORT)
    currentTime = GetTimeStamp() #get current time stamp
    msg = ''
    if ud.SendMsg(currentTime):
        msg = ud.RecvMsg()  #receive offset time between client and server
        print 'delay msg:',msg
    ud.Close()
    #end get delayinfo 
    sendMsg[NETWORK_DELAY] = msg #update delay info
    print 'udp delay,',sendMsg
'''
##altered to send 5 packets
def UDPThread_Delay(ip,sendMsg):
    print 'UDPThread_Delay:start get delay info'
    #get delay info
    packetCount = 2  #发送3个包来测量平均时延
    counter = packetCount
    sumTime = 0.0
    isTimeOut = False
    while counter > 0:
        if isTimeOut:
            break  #i如果存在超时出现，则退出
        ud = UDPClient(ip,SOCKET_UDP_PORT)
        startTimeMsg = GetTimeStamp() #get current time stamp
        endTimeMsg = ''
        if ud.SendMsg(startTimeMsg):
            endTimeMsg = ud.RecvMsg()  #receive offset time between client and server
            #print 'udp delay msg:',msg
            if ''==endTimeMsg:
                isTimeOut = True  #timeout accur
            else:
                sumTime = sumTime + float(GetOffsetTime(startTimeMsg, endTimeMsg)) #正常接收
        ud.Close()   
        counter = counter-1
        
    #end get delayinfo 
    if isTimeOut and packetCount == counter:
        sendMsg[NETWORK_DELAY] = '' #update delay info
    else:
        #avgTime = '%.2f'%(sumTime/(packetCount-counter))
        avgTime = '%.2f'%abs(sumTime/(packetCount-counter)) #make sure it's positive
        sendMsg[NETWORK_DELAY] = str(avgTime)+' (ms)' #get avg delay time
    #print 'udp delay,',sendMsg
#######################

#override TCP
#input:ip addr;output:dict of TCP network condition

def TCP_Delay(ip,sendTcpMsg):
    tcp_measure_client = TCPClient(ip,DELAY_TCP_PORT)
    if tcp_measure_client.StartConnection():
        sendTcpMsg[NETWORK_AVAIL] = 'YES'
        sum_delay = 0.0
        sum_rtt = 0.0
        sum_jitter = 0.0
        last_delay = 0.0
        count = 5
        while count > 0:
            count = count - 1
            send_time = time.time()
            tcp_measure_client.m_socket.send(str("%f"%send_time))
            recv_time = float(tcp_measure_client.m_socket.recv(17))
            feedback_time = time.time()
            sum_delay = sum_delay + (recv_time-send_time)
            sum_rtt = sum_rtt + (feedback_time-send_time)
            sum_jitter = sum_jitter + abs((recv_time-send_time) -last_delay)
            last_delay = (recv_time-send_time)
            last_delay = (recv_time-send_time)
        #delay = '%0.2f'%((sum_delay/5)*1000)
        delay = '%0.2f'%abs((sum_delay/5)*1000) #make sure it's positive
        rtt = '%0.2f'%((sum_rtt/5)*1000)
        jitter = '%0.2f'%((sum_jitter/4)*1000)
        sendTcpMsg[NETWORK_DELAY] = str(delay) + ' (ms)'
        sendTcpMsg[NETWORK_JITTER] = str(jitter) + ' (ms)'
    else:
        sendTcpMsg[NETWORK_AVAIL] = 'NO'
        sendTcpMsg[NETWORK_DELAY] = -1
        sendTcpMsg[NETWORK_JITTER] = -1

def TCP_Iperf(ip,sendTcpMsg):
    print 'TCPThread_Iperf:start iperf'
    filename = 'temp_tcp_iperf_'+str(int(time.time()*1000))+'.txt'
    cmd = 'iperf -c %s  -t 1 -i 0.5 >%s'%(ip,filename)
    os.system(cmd)
    print 'end iperf'
    fip = open(filename)
    try:
        line = fip.readlines()
        bw = line[-1].strip('\n')
        sendTcpMsg[NETWORK_AVAIL] = 'YES'
    except:
        bw = ''
    finally:
        sendTcpMsg[NETWORK_BANDWITH]= bw
        fip.close()
    print 'tcp iperf,',sendTcpMsg
    os.system('sudo rm -rf %s'%filename)
            
    

def TCP_Loss(ip,sendTcpMsg):
    '''filename = 'temp_trace_'+str(int(time.time()*1000))+'.txt'
    #os.system("sudo rm -r trace2.txt")
    #cmd = 'sudo tcpdump -w trace2.txt'
    cmd = 'sudo tcpdump -w %s'%filename
    p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    time.sleep(10)
    os.system('sudo killall -2 tcpdump')
    p.terminate()
    time.sleep(2)
    
    capname = 'temp_cap_'+str(int(time.time()*1000))+'.txt'
    cmd = "captcp statistic --format '%%(rexmt-da\
ta-bytes)d / %%(transport-layer-byte)d' --filter '*:*-*:*' \
%s >%s"%(filename,capname)
    os.system(cmd)
    fcap = open(capname)
    retran = 0.0
    tran = 0.0
    try:
        lines = fcap.readlines()
        for line in lines:
            mid = line.find('/')
            ed = line.find('\n')
            retran = retran + (float)(string.atoi(line[0:mid-1]))
            tran = tran + (float)(string.atoi(line[mid+2:ed]))
        
        if(tran == 0):
            loss = 0.0
        else:
            loss = 100*retran / tran
        sendTcpMsg[NETWORK_LOSS] = str('%0.2f'%loss) + ' %' 
    finally:
        fcap.close()  
    os.system("sudo rm -rf %s"%filename)
    os.system("sudo rm -rf %s"%capname)'''
    sendTcpMsg[NETWORK_LOSS] = 0

    
def GetTCPNetworkInfo(ip):
    sendTcpMsg={'loss': 0, 'jitter': -1, 'delay': -1, 'bandwidth': '', 'congestion': 'NO', 'availability': 'NO'}
    t1 = threading.Thread(target=TCP_Iperf,args=(ip,sendTcpMsg))
    t2 = threading.Thread(target=TCP_Delay,args=(ip,sendTcpMsg))
    t3 = threading.Thread(target=TCP_Loss,args=(ip,sendTcpMsg))
    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()
    return sendTcpMsg

#override UDP
#input:ip addr;output:dict of UDP network condition
def GetUDPNetworkInfo(ip):
    
    #sendMsg = {NETWORK_BANDWITH:'12Mps',NETWORK_DELAY:timeInfo,NETWORK_JITTER:'0.9ms',NETWORK_LOSS:'0.9%',NETWORK_CONGESTION:'yes',NETWORK_AVAIL:'yes'}
    '''
    print 'start iperf'
    os.system('iperf -u -c 127.0.0.1 -t 5 -i 1 > udpfile.txt')
    print 'end iperf'
    sendMsg = ReadIperfUDPFile()
    
    print 'start get delay info'
    #get delay info
    ud = UDPClient(SOCKET_UDP_IP,SOCKET_UDP_PORT)
    currentTime = GetTimeStamp() #get current time stamp
    if ud.SendMsg(currentTime):
        msg = ud.RecvMsg()  #receive offset time between client and server
        print 'feedback msg:',msg
        sendMsg[NETWORK_DELAY] = msg
    ud.Close()
    #end get delayinfo 
    print 'GetNetworkUDP',sendMsg
    return sendMsg
    '''
    sendMsg = {}
    
    t1 = threading.Thread(target=UDPThread_Delay,args=(ip,sendMsg))
    t2 = threading.Thread(target=UDPThread_Iperf,args=(ip,sendMsg))
    t1.start()
    t1.join()  #block until thread t1 and t2 end
    t2.start()
    t2.join()
    return sendMsg
    

#override ICMP
#input:ip addr;output:dict of ICMP network condition
def GetICMPNetworkInfo(ip):
    ISOTIMEFORMAT='%Y-%m-%d_%X'
    time_char = time.strftime(ISOTIMEFORMAT, time.gmtime(time.time()))
    IP = ip
    num_to_send_string = "10"
    c_rate_raw = "0.3";
    s_bandwidth_raw = "10"
    command = "./ICMP/ICMP_Positive " + IP + " " + num_to_send_string + " " + c_rate_raw + " " + s_bandwidth_raw + " " + time_char
    os.system(command)

    connection_file = "./" + time_char + "_result.txt"
    f=open(connection_file)
    array=[]
    for line in f:
        array.append(string.atof(line))
        
    bandwidth_to_send = str("%0.2f"%array[4]) + ' Mbits/sec'
    if IP == '127.0.0.1':
        bandwidth_to_send = 'localhost'
    delay_to_send = str("%0.2f"%array[0]) + ' (ms)'
    jitter_to_send = str("%0.2f"%array[1])+ ' (ms)'
    loss_to_send = str("%0.2f"%array[2])
    if(array[5] == 1):
        congestion_to_send = 'YES'
    elif(array[5] == 0):
        congestion_to_send = 'NO'
    if(array[3] == 1):
        available_to_send = 'YES'
    elif(array[3] == 0):
        available_to_send = 'NO'
    
    
    sendMsg = {NETWORK_BANDWITH:bandwidth_to_send,NETWORK_DELAY:delay_to_send,NETWORK_JITTER:jitter_to_send,NETWORK_LOSS:loss_to_send,NETWORK_CONGESTION:congestion_to_send,NETWORK_AVAIL:available_to_send}
   
    delete_connection_file = "rm -rf"+ connection_file
    os.system(delete_connection_file)
    return sendMsg
'''
#change for graphize   
def GetTracerouteNetworkInfo(ip):
    print 'GetTracerouteNetworkInfo'
    filename = 'traceroute_'+str(int(time.time()*1000))+'.txt'
    cmd = 'sudo traceroute -n -I %s >%s'%(ip,filename) #using traceroute to trace path
    os.system(cmd)
    
    traceInfo = []
    fip = open(filename)
    try:
        lines = fip.readlines() #get all lines
        for line in lines:
            tmp = line.split()
            traceInfo.append(tmp[1])  # get route ip from traceroute result
    finally:
        fip.close()
        os.system('sudo rm -rf %s'%filename)
    os.system('sudo rm -rf %s'%filename)  #delete file
    sendMsg = {}
    for item in traceInfo:
        #to check if those ips were in SCHOOLIP
        if SCHOOLIP.has_key(item):
            sendMsg[item] = SCHOOLIP[item]
    #print sendMsg
    return sendMsg
'''
def GetTracerouteNetworkInfo(ip):
    print 'GetTracerouteNetworkInfo'
    filename = 'traceroute_'+str(int(time.time()*1000))+'.txt'
    cmd = 'sudo traceroute -n -I %s >%s'%(ip,filename) #using traceroute to trace path
    os.system(cmd)
    
    traceInfo = []
    fip = open(filename)
    try:
        fip.readline() #to jump first line
        lines = fip.readlines() #get all lines
        for line in lines:
            tmp = line.split()
            #ignore * * *
            if '*' != tmp[1][0]:
                traceInfo.append(tmp[1])  # get route ip from traceroute result
    finally:
        fip.close()
    #print 'traceInfo:',traceInfo
    
    #formate msg to string
    sendMsg = {} #{ip:name,ip2:name2..}
    counter = 0
    for item in traceInfo:
        counter = counter+1;
        #to check if those ips were in SCHOOLIP
        key = '0'
        if counter < 10:
            key = "0"+str(counter)+" "+str(item) #like: 01 192.168.1.1
        else:
            key = str(counter)+" "+str(item) 
        if SCHOOLIP.has_key(item):
            sendMsg[key] = SCHOOLIP[item]
        else:
            sendMsg[key] = ''
    #print sendMsg
    os.system('rm -rf %s'%filename) #delete record file
    return sendMsg