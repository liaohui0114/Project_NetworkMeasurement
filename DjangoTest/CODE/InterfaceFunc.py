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
        

def UDPThread_Iperf(ip,sendMsg):
    print 'UDPThread_Iperf:start iperf'
    filename = 'temp_udp_iperf_' + str(int(time.time()*1000))+'.txt'
    #os.system('iperf -u -c %s -t 5 -i 1 -b 10000M> udpfile.txt'%ip)
    os.system('iperf -u -c %s -t 1 -i 0.5 -b 35M -p 10009> %s'%(ip,filename))  #40M is close to thresh_hold
    print 'end iperf'
    msg = ReadIperfUDPFile(filename)
    for key,value in msg.items():
        sendMsg[key] = value #update info like: bandwidth,loss,jitter and so on
    print 'udp iperf,',sendMsg
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
    packetCount = 3  #发送3个包来测量平均时延
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