import socket
import time
import threading
import os
import fcntl 
import struct
import threading
from SocketModule import *
from GlobleVariable import *
import threading
from InterfaceFunc import *
from Passive import *
#from restart import *

mylock = threading.RLock()
NUM_CON = 0
TMP_UDP = {}

def get_ip_address(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, # SIOCGIFADDR 
                    struct.pack('256s', ifname[:15]) )[20:24])

def IperfTCPServer():
    os.system('iperf -s')

def DelayTCPServer(HOST):
    print HOST
    print str(HOST)
    os.system('python Tcp_measure_server.py %s'%HOST)

def IperfUDPServer():
    os.system('iperf -s -u -p 10009')

def DelayUDPServer(HOST):
    os.system('python udpServerTest.py %s'%HOST)
    
def getTrace():
    cmd = 'captcp socketstatistic -o output'
    os.system(cmd)
    
def getTcp():
    cmd = 'sudo tcpdump -w trace2.txt'
    os.system(cmd)
    
def startPassive():
    '''os.system('sudo rm -r output')
    os.system('mkdir output')
    t1 = threading.Thread(target = getTrace)  
    t1.start()'''

    os.system("sudo rm -r trace2.txt")
    t2 = threading.Thread(target = getTcp)
    t2.start()

def stopPassive():
    '''fid = open('pid.txt') #captcp will create a new process, we need to get the pid
                              #of it and "kill -2 pid" to complete it
    pid = (int)(fid.read())
    fid.close()
    print pid
    os.system('sudo kill -2 %d'%pid)
    time.sleep(5)#wait for generating data'''
    os.system('sudo killall -2 tcpdump')                
    time.sleep(5)#wait for generating data
    
def restartIperf():
    os.system('sudo killall -9 iperf')
    time.sleep(5)

    

    iperfTCP = threading.Thread(target = IperfTCPServer)
    #iperfTCP.setDaemon(True)
    iperfTCP.start()
    
    #daemon threading for udp
    iperfUDP = threading.Thread(target = IperfUDPServer)
    #iperfUDP.setDaemon(True)
    iperfUDP.start()

    time.sleep(5)
    print 3

      
#define our own thread to deal with 
def MyThread(clientSocket,clientAddr,HOST):
    print 'MyThread to deal with connection from %s:%s'%(clientAddr)
    msg =  clientSocket.recv(SOCKET_BUFFER_SIZE)
    
    detailMsg = GetSocketMsg(msg)  #formmat msg to dict we have defined in GlobleVariable
    print 'detailMsg:',detailMsg
    
    sendMsg = {} #msg which feedback to client include delay,bandwidth and so on
    
    if detailMsg[PROTOCOL_PROTOCOL] == 'TCP':
        print "TCP operation--iperf"
        sendMsg = GetTCPNetworkInfo(detailMsg[PROTOCOL_IP])
        
    elif detailMsg['protocol'] == 'UDP':
        print 'UDP operation--iperf'
        global NUM_CON
        global TMP_UDP
        print 'NUM_CON=',NUM_CON
        if NUM_CON == 0:
            mylock.acquire()
            sendMsg = GetUDPNetworkInfo(detailMsg[PROTOCOL_IP])#interface you need to override
            TMP_UDP = sendMsg
            mylock.release()
        else:
            print 'TMP_UDP:',TMP_UDP
            sendMsg = TMP_UDP
            
        
    elif detailMsg['protocol'] == 'ICMP':
        print 'ICMP operation--ping'
        sendMsg = GetICMPNetworkInfo(detailMsg[PROTOCOL_IP])
        
    elif detailMsg['protocol'] == 'PASSIVE':
        print 'PASSIVE operation'
        sendMsg = {}
        
        stopPassive()      
        sendMsg = passive(HOST,detailMsg[PROTOCOL_IP])        
        startPassive()
        
    else:
        pass
       
    if detailMsg['protocol'] == 'PASSIVE':
        clientSocket.send(SetPassiveMsg(sendMsg))
    else:
        clientSocket.send(SetSocketMsg(sendMsg))  #send feedback msg to client
        #if there is no bandwith,which mean iperf doesn't work,restart iperf
        if sendMsg.has_key(NETWORK_BANDWITH) == False or sendMsg[NETWORK_BANDWITH] == '':
            restartIperf()
    clientSocket.close() #close socket
    print 'End MyThread to deal with connection'



#if __name__ == '__main__':
def server():
        
    HOST = get_ip_address('eth0')
    print type(HOST)
    #tpServer = TCPServer(SOCKET_TCP_IP,SOCKET_TCP_PORT)
    tpServer = TCPServer(HOST,SOCKET_TCP_PORT)
    #daemon threading for tcp
    iperfTCP = threading.Thread(target = IperfTCPServer)
    #iperfTCP.setDaemon(True)
    iperfTCP.start()
    delayTCP = threading.Thread(target = DelayTCPServer,args = (HOST,))
    #delayTCP.setDaemon(True)
    delayTCP.start()
    #daemon threading for udp
    iperfUDP = threading.Thread(target = IperfUDPServer)
    #iperfUDP.setDaemon(True)
    iperfUDP.start()
    delayUDP = threading.Thread(target = DelayUDPServer, args = (HOST,))
    #delayUDP.setDaemon(True)
    delayUDP.start()
    
    '''os.system('sudo rm -r output')
    os.system('mkdir output')
    t1 = threading.Thread(target = getTrace)  
    t1.start()

    os.system("sudo rm -r trace2.txt")
    t2 = threading.Thread(target = getTcp)
    t2.start()'''
    startPassive()
    
    '''while True:
        sleep(10)
        restart()
        print 5
        sleep(20)
        print 6'''
        
    
    if tpServer.StartBind():
        #always working at background to deal with connection from client
        while True:
            clientSocket,clientAddr = tpServer.AcceptConnection()
            if clientAddr==None and clientAddr==None:
                continue #if we get none info
            #create new thread to deal with every connection from different Client            
            t = threading.Thread(target=MyThread,args=(clientSocket,clientAddr,HOST))
            t.start()
        tpServer.Close()

    
