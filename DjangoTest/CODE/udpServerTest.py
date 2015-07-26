#!/usr/bin/env python
import sys
from SocketModule import *
from GlobleVariable import *


if __name__ == '__main__':
    HOST = sys.argv[1]
    us = UDPServer(HOST,SOCKET_UDP_PORT)
    if us.StartBind():
        while True:
            recvMsg = us.RecvClientMsg()  #waiting for data from different client
            #timeOffsetMsg = GetOffsetTime(recvMsg)  #get offset time(client to server) and send back to client
            #print timeOffsetMsg
            endTime = GetTimeStamp()
            us.SendFeedbackMsg(endTime)
        
    us.Close()
        
