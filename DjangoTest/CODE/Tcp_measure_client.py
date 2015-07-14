import os
import numpy
import socket
import time
import threading
import sys
import string
from GlobleVariable import *
from TCPSocket import *

if __name__ == '__main__':
    '''tcp_measure_client = TCPClient('192.168.1.152',10003)
    if tcp_measure_client.StartConnection():
        sum_delay = 0.0
        sum_rtt = 0.0
        sum_jitter = 0.0
        last_delay = 0.0
        count = 5
        while count > 0:
            count = count - 1
            send_time = time.time()
            tcp_measure_client.m_socket.send(str("%f"%send_time))
            #print 'send time: %f'%send_time
            recv_time = float(tcp_measure_client.m_socket.recv(17))
            feedback_time = time.time()
            #print 'recived time: %f'%recv_time
            #print 'delay: %f'%(recv_time-send_time)
            #print 'RTT: %f'%(feedback_time-send_time)
            sum_delay = sum_delay + (recv_time-send_time)
            sum_rtt = sum_rtt + (feedback_time-send_time)
            sum_jitter = sum_jitter + abs((recv_time-send_time) -last_delay)
            last_delay = (recv_time-send_time)
            last_delay = (recv_time-send_time)
        delay = int((sum_delay/5)*1000000)
        rtt = int((sum_rtt/5)*1000000)
        jitter = int((sum_jitter/4)*1000000)
        #print 'ave_delay: %0.9f'%delay
        #print 'ave_rtt: %0.9f'%rtt
        #print 'jitter: %0.9f'%jitter
        sendTcpMsg={}
        os.system('iperf -c 127.0.0.1  -t 2 -i 0.5 >/home/wenhao/ip.txt')
        os.system("captcp statistic --format '%(rexmt-da\
ta-bytes)d / %(transport-layer-byte)d' --filter '*:48548-*:*,*:*-*:48548' \
trace.pcap >/home/wenhao/cap.txt")
        fip = open('/home/wenhao/ip.txt')
        try:
            line = fip.readlines()
            print line
            bw = line[-1].strip('\n')
        finally:
            fip.close()
            
        fcap = open('/home/wenhao/cap.txt')
        try:
            line = fcap.readlines()
            mid1 = line[0].find('/')
            ed1 = line[0].find('\n')
            retran1 = string.atoi(line[0][0:mid1-1])
            tran1 = string.atoi(line[0][mid1+2:ed1])

            mid2 = line[1].find('/')
            ed2 = line[1].find('\n')
            retran2 = string.atoi(line[1][0:mid2-1])
            tran2 = string.atoi(line[1][mid2+2:ed2])

            loss = (float)(retran1+retran2)/(float)(tran1+tran2)
            loss = float('%0.4f'%loss)
        finally:
            fcap.close()

        sendTcpMsg[NETWORK_BANDWITH]= bw
        sendTcpMsg[NETWORK_DELAY] = delay
        sendTcpMsg[NETWORK_JITTER] = jitter
        sendTcpMsg[NETWORK_LOSS] = loss
        sendTcpMsg[NETWORK_CONGESTION] = 'yes'
        sendTcpMsg[NETWORK_AVAIL] = 'yes'
        print sendTcpMsg
        
        tcp_measure_client.CloseConnection()'''
        
