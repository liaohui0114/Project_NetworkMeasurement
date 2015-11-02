#!/usr/bin/env python
import sys
from SocketModule import *
from GlobleVariable import *
import threading

def MyThread(udpsocket):
    print 'MyThread UDP'
    #print type(clientAddr),len(clientAddr)
    endTime = GetTimeStamp()
    us.SendFeedbackMsg(endTime)
    print 'End MyThread UDP'
    
if __name__ == '__main__':
    HOST = sys.argv[1]
    us = UDPServer(HOST,SOCKET_UDP_PORT)
    if us.StartBind():
        while True:
            recvMsg = us.RecvClientMsg()  #waiting for data from different client
            #timeOffsetMsg = GetOffsetTime(recvMsg)  #get offset time(client to server) and send back to client
            #print timeOffsetMsg
            
            t = threading.Thread(target=MyThread,args=(us,))
            t.start()
        
    us.Close()
        
