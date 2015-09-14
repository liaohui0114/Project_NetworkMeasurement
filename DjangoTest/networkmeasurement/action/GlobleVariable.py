#!/usr/bin/env python
from string import *
import time

FILE_SIGNAL = 0
PROTOCOL_UDP = 'UDP'
PROTOCOL_TCP = 'TCP'
PROTOCOL_ICMP = 'ICMP'
PROTOCOL_PROTOCOL = 'protocol'
PROTOCOL_IP = 'ip'

#HOST = '192.168.1.177'
DEST = '192.168.1.152'
HOST_NAME = 'HOST'
#DEST_NAME = ['sjtu','fudan','shangda']
#DEST_IP = {'sjtu':'202.121.178.195','fudan':'219.228.12.60','shangda':'202.120.199.169'}

#HOST = '127.0.0.1'
#DEST = '127.0.0.1'

NODE_SJTU = '202.121.178.195'
NODE_FUDAN = '219.228.12.60'
NODE_SHANGDA = '202.120.199.169'
NODE_TONGJI = '127.0.0.1'

SOCKET_SERVER_IP = '127.0.0.1'
SOCKET_SERVER_PORT = 10001

#DEFAULT IP AND PORT OF TCP
SOCKET_TCP_IP = '127.0.0.1'
#SOCKET_TCP_PORT = 9999
SOCKET_TCP_PORT = 10000
DELAY_TCP_PORT = 10003

#DEFAULT IP AND PORT OF UDP
SOCKET_UDP_IP = '127.0.0.1'
#SOCKET_UDP_PORT = 11111
SOCKET_UDP_PORT = 10002
SOCKET_UDP_IPERF_PORT = 10009

SOCKET_BUFFER_SIZE = 1024  #packet size of socket(send/receive) 
SOCKET_TIME_OUT = 8

SOCKET_MAX_CLIENT = 10     #max connection num from client

#define attribute
NETWORK_BANDWITH = 'bandwidth'   
NETWORK_DELAY = 'delay'          
NETWORK_JITTER = 'jitter'        
NETWORK_LOSS = 'loss'            
NETWORK_CONGESTION = 'congestion'
NETWORK_AVAIL = 'availability'
NETWORK_THROUGHPUT = 'throughput'
NETWORK_CPU = 'cpu percent'
NETWORK_MEM = 'memory percent'    

NETWORK_IP = 'ip'
NETWORK_PROTOCOL = 'protocol'

FILE_PATH_UDP = 'udpfile.txt'

#define TIMEOUT
NETWORK_TIME_OUT = 10 #10S

#define period for passive throughput
THROUGHPUT_TIME = 10


def SetPassiveMsg(dicMsg):
    msg = ''
    print dicMsg
    for k,v in dicMsg.items():
        if msg == '':
            msg += '%s:%s,%s,%s,%s,%s,%s'%(k,v[NETWORK_BANDWITH],v[NETWORK_DELAY],v[NETWORK_LOSS],v[NETWORK_THROUGHPUT],v[NETWORK_CPU],v[NETWORK_MEM]) #format dict to string which is 'key:value,key:value,key:value...'
        else:
            msg += ';%s:%s,%s,%s,%s,%s,%s'%(k,v[NETWORK_BANDWITH],v[NETWORK_DELAY],v[NETWORK_LOSS],v[NETWORK_THROUGHPUT],v[NETWORK_CPU],v[NETWORK_MEM]) #format dict to string which is 'key:value,key:value,key:value...'
    print 'End SetSocketMsg,msg is:',msg
    return msg
    
def GetPassiveMsg(msg):
    socketMsg={}
    print 'msg:',msg
    tmpList = msg.split(';')
    for i in tmpList:
        tmp = i.split(':')
        listPassive = tmp[1]
        print listPassive
        listPassive = listPassive.split(',')
        print listPassive
        index  = [NETWORK_BANDWITH,NETWORK_DELAY,NETWORK_LOSS,NETWORK_THROUGHPUT,NETWORK_CPU,NETWORK_MEM]
        result = {}
        for j in range(6):
            result[index[j]] = listPassive[j]
        print result
        socketMsg[tmp[0]] = result
        
    return socketMsg
    


#func,deal with string
def SetSocketMsg(dicMsg):
    print 'SetSocketMsg,msg:',dicMsg
    msg = ''
    if dicMsg.has_key(NETWORK_PROTOCOL) and dicMsg[NETWORK_PROTOCOL] == 'PASSIVE':
        listIP = dicMsg[NETWORK_IP]
        msg = 'ip:'
        for ip in listIP:
            msg+='%s,'%ip
        msg+='protocol:PASSIVE'
    
    else: 
        for k,v in dicMsg.items():
            #print k,v
            if msg == '':
                msg += '%s:%s'%(k,v) #format dict to string which is 'key:value,key:value,key:value...'
            else:
                msg += ',%s:%s'%(k,v)
        
    print 'End SetSocketMsg,msg is:',msg
    return msg


#transform str to dic 
def GetSocketMsg(msg):
    print 'GetSocketMsg'
    socketMsg = {}
    proList = msg.split(':')
    if proList[-1] == 'PASSIVE':
        socketMsg = {}
        #tmpList = sdmsg.split(',')
        tmpList = msg.split(':')
        list_ip = tmpList[1].split(',')
        print list_ip[0:-1]
        socketMsg[list_ip[-1]] = tmpList[-1]
        list_ip = list_ip[0:-1]
        socketMsg[tmpList[0]] = list_ip
        print socketMsg
    else:
        tmpList = msg.split(',')
        for i in tmpList:
            tmp = i.split(':')
            socketMsg[tmp[0]] = tmp[1]
            if tmp[1] == "":
                print "[key:%s],value is ''"%tmp[0]
                print 'End GetSocketMsg,msg is:',socketMsg
    return socketMsg

#get time stamp which is type(float) ,we only keep 9 bin after .,return type(str)
def GetTimeStamp():
    return '%.9f'%time.time()

#get offset time:between timstampstr and currenttime
def GetOffsetTime(timeStampStr):
    currentTime = time.time()
    print '%.9f'%currentTime
    offsetTime = currentTime - float(timeStampStr)
    print '%.9f'%offsetTime
    if offsetTime > 1:
        return '%.3f (s)'%offsetTime
    else:
        return '%.3f (ms)'%(offsetTime*1000)
    


#to get network condition in udpfile.txt;return dict
#def ReadIperfUDPFile(filePath = FILE_PATH_UDP):
def ReadIperfUDPFile(filename):
    print 'StartReadIperfUDPFile'

    #f = open(FILE_PATH_UDP)       #open file  
    f = open(filename)       #open file
    lineStr = f.readline()

    lastLineStr = ''  # get string of last line in file

    bIsConnect = False #to judge if we can connect with node

    while lineStr:

        if not -1 == lineStr.find('Server Report'):#if we find str Server Report

            bIsConnect = True

        #print 'lastLineStr',lastLineStr

        lineStr = f.readline()

        if bIsConnect:

            lastLineStr = lineStr  #get the line including detail infos which is next the line contains 'Server Report'

            break 

    f.close()  #close open

    print lastLineStr

    

    #Init DEFAULT

    networkDict = {NETWORK_BANDWITH:'',NETWORK_JITTER:'',NETWORK_LOSS:'',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}

    #to get network info in lastLineStr

    if not bIsConnect:  #connect failed

        print 'fail connection'  #if str contains 'datagrams' which means failing connecting to server

        networkDict[NETWORK_AVAIL] = 'NO'  #not available to connect

        networkDict[NETWORK_CONGESTION] = ''

    else:

        tmpStr= lastLineStr.split(' sec') #using 'sec' to split lastLineStr
        print "tmpStr:",tmpStr
        tmpList = tmpStr[1].split()  #split by ' '  to get data that we truely need

        ##testtest

        #for index,value in enumerate(tmpList):

            #print '[index:%d][value:%s]'%(index,value)

        ###

        

        bandwidth = tmpList[2]+' '+tmpList[3]  #get bandwidth
        jitter =  tmpList[4] + ' ' +tmpList[5]  #get jitter
        loss = tmpList[-1][1:-1]   #delete ( and ) to get loss
        networkDict[NETWORK_BANDWITH] = bandwidth

        networkDict[NETWORK_JITTER] = jitter

        networkDict[NETWORK_LOSS] = loss[0:-1]+' '+loss[-1]

    #print networkDict    
    #print networkDict
    print 'End StartReadIperfUDPFile'

    return networkDict

    
    
    
