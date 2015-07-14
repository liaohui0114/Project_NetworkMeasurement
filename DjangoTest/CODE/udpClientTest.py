#!/usr/bin/env python
from SocketModule import *
from GlobleVariable import *
from InterfaceFunc import *
import time
import datetime

if __name__ == '__main__': 
       
    '''ud = UDPClient('202.121.178.195',10002)
    currentTime = GetTimeStamp() #get current time stamp
    if ud.SendMsg(currentTime):
        msg = ud.RecvMsg()  #receive offset time between client and server
        print 'feedback msg:',msg
    ud.Close()'''
    #UDPThread_Delay('202.121.178.195',sendMsg)
    sendMsg = GetUDPNetworkInfo('202.121.178.195')
    print sendMsg
