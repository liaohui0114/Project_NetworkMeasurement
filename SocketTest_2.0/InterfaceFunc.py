#!/usr/bin/env python
from GlobleVariable import *
import os
from SocketModule import *
#####UDP Thread######

def UDPThread_Iperf(ip,sendMsg):
    print 'UDPThread_Iperf:start iperf'
    os.system('iperf -u -c 192.168.1.152 -t 5 -i 1 > udpfile.txt')
    print 'end iperf'
    msg = ReadIperfUDPFile()
    for key,value in msg.items():
        sendMsg[key] = value #update info like: bandwidth,loss,jitter and so on
    print 'udp iperf,',sendMsg
    
    
def UDPThread_Delay(ip,sendMsg):
    print 'UDPThread_Iperf:start get delay info'
    #get delay info
    ud = UDPClient(SOCKET_UDP_IP,SOCKET_UDP_PORT)
    currentTime = GetTimeStamp() #get current time stamp
    msg = ''
    if ud.SendMsg(currentTime):
        msg = ud.RecvMsg()  #receive offset time between client and server
        print 'delay msg:',msg
    ud.Close()
    #end get delayinfo 
    sendMsg[NETWORK_DELAY] = msg #update delay info
    print 'udp delay,',sendMsg

#######################

#override TCP
#input:ip addr;output:dict of TCP network condition
def GetTCPNetworkInfo(ip):
    print ''
    return {}

#override TCP
#input:ip addr;output:dict of UDP network condition
def GetUDPNetworkInfo(ip):
    
    #sendMsg = {NETWORK_BANDWITH:'12Mps',NETWORK_DELAY:timeInfo,NETWORK_JITTER:'0.9ms',NETWORK_LOSS:'0.9%',NETWORK_CONGESTION:'yes',NETWORK_AVAIL:'yes'}
    '''
    print 'start iperf'
    os.system('iperf -u -c 192.168.1.152 -t 5 -i 1 > udpfile.txt')
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
    t1 = threading.Thread(target=UDPThread_Iperf,args=(ip,sendMsg))
    t2 = threading.Thread(target=UDPThread_Delay,args=(ip,sendMsg))
    t1.start()
    t2.start()
    t1.join()
    t2.join()  #block until thread t1 and t2 end
    
    return sendMsg
    

#override TCP
#input:ip addr;output:dict of ICMP network condition
def GetICMPNetworkInfo(ip):
    return {}