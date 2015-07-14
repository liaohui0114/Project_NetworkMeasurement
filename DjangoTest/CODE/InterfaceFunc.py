#!/usr/bin/env python
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
        

def UDPThread_Iperf(ip,sendMsg):
    print 'UDPThread_Iperf:start iperf'
    filename = 'temp_udp_iperf_' + str(int(time.time()*1000))+'.txt'
    #os.system('iperf -u -c %s -t 5 -i 1 -b 10000M> udpfile.txt'%ip)
    os.system('iperf -u -c %s -t 1 -i 0.5 -b 25M -p 10009> %s'%(ip,filename))
    print 'end iperf'
    msg = ReadIperfUDPFile(filename)
    for key,value in msg.items():
        sendMsg[key] = value #update info like: bandwidth,loss,jitter and so on
    print 'udp iperf,',sendMsg
    os.system('sudo rm -rf %s'%filename)
    
    
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
        delay = '%0.2f'%((sum_delay/5)*1000)
        rtt = '%0.2f'%((sum_rtt/5)*1000)
        jitter = '%0.2f'%((sum_jitter/4)*1000)
        sendTcpMsg[NETWORK_DELAY] = str(delay) + ' (ms)'
        sendTcpMsg[NETWORK_JITTER] = str(jitter) + ' (ms)'
    else:
        sendTcpMsg[NETWORK_AVAIL] = 'NO'
        sendTcpMsg[NETWORK_DELAY] = -1
        sendTcpMsg[NETWORK_JITTER] = -1

def TCP_Iperf(ip,sendTcpMsg):
    filename = 'temp_tcp_iperf_'+str(int(time.time()*1000))+'.txt'
    cmd = 'iperf -c %s  -t 1 -i 0.5 >%s'%(ip,filename)
    os.system(cmd)
    
    fip = open(filename)
    try:
        line = fip.readlines()
        bw = line[-1].strip('\n')
        sendTcpMsg[NETWORK_BANDWITH]= bw
    finally:
        fip.close()
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
    sendTcpMsg={}
    sendTcpMsg[NETWORK_CONGESTION] = 'NO'
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
   
    delete_connection_file = "rm "+ connection_file
    os.system(delete_connection_file)
    return sendMsg
