import os
import string
from GlobleVariable import *
from subprocess import *
from multiprocessing import Process
import time
import threading
#import MySQLdb
from SocketModule import *


def getTrace():
    '''global pid
    pid = os.getpid()
    print 'child_pid:',pid
    global flag
    flag = 1
    print 'flag_trace = ',flag'''
    cmd = 'captcp socketstatistic -o output'
    os.system(cmd)
    



def readRTT(path):
    frtt = open(path)
    rtt_ave = 0.0
    count_rtt = 0
    try:
        lines = frtt.readlines()
        for line in lines:
            mid = line.find(' ')
            end = line.find('\n')
            #print line[mid+1:end]
            rtt_ave = rtt_ave + (float)(line[mid+1:end])
            count_rtt = count_rtt + 1
        rtt_ave = rtt_ave /count_rtt
    finally:
        frtt.close()
    return rtt_ave


def getRTT(st_ip,ed_ip):    
    '''cmd = 'find output -name %s:*%s:* >path.txt'%(st_ip,ed_ip)
    os.system(cmd)
    rtt = 0.0
    count = 0
    fpath = open('path.txt')
    try:
        lines = fpath.readlines()
        for line in lines:
            path = line.strip()+'/rtt/rtt.data'
            if(os.path.isfile(path)): 
                rtt = rtt + readRTT(path)
                count = count + 1
        if(count != 0):
            print rtt
            print count
            rtt = rtt / count
        else:
            rtt = -1
    finally:
        fpath.close()
    print 'rtt from %s to %s:'%(st_ip,ed_ip),rtt
    return rtt'''

    tcp_measure_client = TCPClient(ed_ip,DELAY_TCP_PORT)
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
            recv_time = float(tcp_measure_client.m_socket.recv(17))
            feedback_time = time.time()
            #sum_delay = sum_delay + (recv_time-send_time)
            sum_rtt = sum_rtt + (feedback_time-send_time)
            #sum_jitter = sum_jitter + abs((recv_time-send_time) -last_delay)
            #last_delay = (recv_time-send_time)
            #last_delay = (recv_time-send_time)
        #delay = '%0.2f'%((sum_delay/5)*1000)
        rtt = '%0.2f'%((sum_rtt/5)*1000)
        #jitter = '%0.2f'%((sum_jitter/4)*1000)
        #sendTcpMsg[NETWORK_DELAY] = str(delay) + ' (ms)'
        #sendTcpMsg[NETWORK_JITTER] = str(jitter) + ' (ms)'
    else:
        rtt = -1
    print 'rtt from %s to %s:'%(st_ip,ed_ip),rtt
    return rtt

def getLOSS(st_ip,ed_ip):
    part1 = "'%(rexmt-data-bytes)d / %(transport-layer-byte)d'"
    part2 = '%s:*-%s:*'%(st_ip,ed_ip)
    part3 = "'"+part2+"'"
    filename = 'loss_'+st_ip+'_'+ed_ip+'.txt'
    cmd = "captcp statistic --format %s --filter %s trace2.txt >./%s"%(part1,part3,filename)
    os.system(cmd)
    floss = open(filename)
    tran = 0.0;
    retran = 0.0;
    try:
        lines = floss.readlines()
        for line in lines:
            mid = line.find('/')
            ed = line.find('\n')
            retran = retran + (float)(string.atoi(line[0:mid-1]))
            tran = tran + (float)(string.atoi(line[mid+2:ed]))
        if(tran == 0.0):
            loss = 0
        else:
            loss = retran / tran
        loss = float('%0.4f'%loss)
        print 'data loss from %s to %s:'%(st_ip,ed_ip),loss
    finally:
        floss.close()
        
    os.system('sudo rm -rf %s'%filename)
    return loss


def getTHROUGHPUT(st_ip,ed_ip):
    
    part1 = "'%(network-layer-byte)d'"
    part2 = '%s:*-%s:*'%(st_ip,ed_ip)
    part3 = "'"+part2+"'"
    filename = 'throughput_'+st_ip+'_'+ed_ip+'.txt'
    cmd = "captcp statistic --format %s --filter %s trace2.txt >./%s"%(part1,part3,filename)
    os.system(cmd)
    
        
    #os.system("captcp statistic --format '%(network-layer-byte)d' \
#--filter '*:*-*:*,*:*-*:*' trace2.txt >./throughput.txt")
    throughput = 0;
    fthr = open(filename)
    try:
        lines = fthr.readlines()
        for line in lines:
            if(string.atoi(line)):
                throughput = throughput + string.atoi(line)
                
        #bandwidth = ((float)(throughput))/10
        print 'throughput from %s to %s:'%(st_ip,ed_ip),throughput,'byte'
        print 'bandwidth from %s to %s:'%(st_ip,ed_ip),((float)(throughput))/THROUGHPUT_TIME,'byte'
    finally:
        fthr.close()
    os.system('sudo rm -rf %s'%filename)
    return throughput
    
    
def getCPU():
    #get the cpu state
    fcpu = open('/proc/stat')
    try:
        lines = fcpu.readlines()
        line= lines[1].split()
    finally:
        fcpu.close()
    total1 =0.0
    idle1 = 0.0
    for slide in line[1:7]:
        total1 = total1 + (float)(slide)
        if(slide == line[4]):
            idle1 = idle1 + (float)(slide)

    time.sleep(2)
    fcpu = open('/proc/stat')
    try:
        lines = fcpu.readlines()
        line= lines[1].split()
    finally:
        fcpu.close()
    total2 =0.0
    idle2 = 0.0
    for slide in line[1:7]:
        total2 = total2 + (float)(slide)
        if(slide == line[4]):
            idle2 = idle2 + (float)(slide)
    total = total2 - total1
    idle = idle2 - idle1
    cpu_per = 100*(total - idle)/total
    print "cpu percentage: %0.2f %%"%cpu_per
    return cpu_per

def getMEM():
    #get the memory state
    fmem = open('/proc/meminfo')
    try:
        lines = fmem.readlines()
        line1 = lines[0].split()
        line2 = lines[1].split()
    finally:
        fmem.close()
    total = (float)(line1[1])
    idle = (float)(line2[1])
    mem_per = 100*(1-idle/total)
    print "mem percetage: %0.2f %%"%mem_per
    return mem_per

    
    
    
#if __name__ == '__main__':
def passive(HOST,ipList):   
    #while(True):
    #ipList = ['127.0.0.1', '192.168.1.2', '192.168.1.177']
    sendMsg = {}
    '''os.system('sudo rm -r output')
    os.system('mkdir output')
    p = Process(target = getTrace)
    p.start()
    time.sleep(5)
    fid = open('pid.txt') #captcp will create a new process, we need to get the pid
                              #of it and "kill -2 pid" to complete it
    pid = (int)(fid.read())
    fid.close()
    print pid
    os.system('kill -2 %d'%pid)
    p.terminate()
    time.sleep(5)#wait for generating data'''
    for ip in ipList:
        tmp = {}
        rtt = getRTT(HOST,ip)
        loss = getLOSS(HOST,ip)
        throughput = getTHROUGHPUT(HOST,ip)
        bandwidth = throughput/10
        cpu_per = getCPU()
        mem_per = getMEM()
        tmp[NETWORK_LOSS] = loss
        tmp[NETWORK_THROUGHPUT] = throughput
        tmp[NETWORK_BANDWITH] = bandwidth
        tmp[NETWORK_DELAY] = rtt
        tmp[NETWORK_CPU] = '%0.2f'%cpu_per
        tmp[NETWORK_MEM] = '%0.2f'%mem_per
        sendMsg[ip] = tmp
        
    return sendMsg
    #for node in DEST_NAME:
    #rtt[node] = getRTT(HOST,DEST_IP[node])
        
    #using tcpdump to collect trace
    '''os.system("sudo rm -r trace2.txt")
    cmd = 'sudo tcpdump -w trace2.txt'
    p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    time.sleep(THROUGHPUT_TIME)
    os.system('sudo killall -2 tcpdump')
    p.terminate()
    time.sleep(2)
    #using captcp to analyse trace
    loss = getLOSS(HOST,ip)
    throughput = getTHROUGHPUT(HOST,ip)
    bandwidth = throughput/10
    sendMsg[NETWORK_LOSS] = loss
    sendMsg[NETWORK_THROUGHPUT] = throughput
    sendMsg[NETWORK_BANDWITH] = bandwidth

    cpu_per = getCPU()
    mem_per = getMEM()
    sendMsg[NETWORK_CPU] = cpu_per
    sendMsg[NETWORK_MEM] = mem_per
    #passive()
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    #for node in DEST_NAME :
    try:
        conn = MySQLdb.connect(host = 'localhost',user = 'root', passwd = 'root',port = 3306)
        cur = conn.cursor()
        cur.execute('create database if not exists %s'%HOST_NAME)
        conn.select_db(HOST_NAME)
        cur.execute('create table if not exists test(time varchar(30),st_node varchar(30)\
        ,ed_node varchar(30),st_IP varchar(20),ed_IP varchar(20),rtt varchar(20),\
        loss varchar(20),throughput varchar(20),bandwidth varchar(20),cpu_per varchar(20),mem_per varchar(20))')
        cur.execute('create table if not exists test(time varchar(30),st_IP varchar(20),ed_IP varchar(20),rtt varchar(20),\
        loss varchar(20),throughput varchar(20),bandwidth varchar(20),cpu_per varchar(20),mem_per varchar(20))')
        value = [time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) ),HOST,ip,str('%0.2f'%rtt),str(loss), str(throughput),str(bandwidth),str('%0.2f'%cpu_per),str('%0.2f'%mem_per)]
        value = ['1433229021443','sjtu','sd','127.0.0.1','127.0.0.1','75.12','0.0', '464','46.4','6.03','5.66']
        cur.execute('insert into test values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
        conn.commit()
        cur.close()
        conn.close()
        print value
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s"%(e.args[0],e.args[1])'''
        		
    #return sendMsg		
        #time.sleep(10)
    
    
    
    
    
    
    

        
    
    
