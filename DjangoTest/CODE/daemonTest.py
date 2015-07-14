# -*- coding:utf-8 -*- 
import MySQLdb
from GlobleVariable import *
from string import *
from PassiveClient import  *
import os
import threading
from datetime import *
import time




if __name__ == '__main__':
    st_name = '123'
    cmd = "select * from networkmeasurement_schoolnode where nodeName = '%s'"%st_name
    print cmd
    print 'UDP'
    a = {}
    b = a.has_key('123')
    if a.has_key('123') == False :
        print 1






'''def get_ip_address(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, # SIOCGIFADDR 
                    struct.pack('256s', ifname[:15]) )[20:24])

import socket 
import fcntl 
import struct    


import threading
from time import ctime,sleep


def music(func):
    for i in range(2):
        print "I was listening to %s. %s" %(func,ctime())
        sleep(1)

def move(func):
    for i in range(2):
        print "I was at the %s! %s" %(func,ctime())
        sleep(5)

threads = []
t1 = threading.Thread(target=music,args=(u'爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=move,args=(u'阿凡达',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

    print "all over %s" %ctime()



    

    
def DelayTCPServer(HOST):
    print HOST
    print str(HOST)
    #os.system('python Tcp_measure_server.py %s'%HOST)

if __name__ == '__main__':
    HOST = get_ip_address('eth0')
    print HOST
    delayTCP = threading.Thread(target = DelayTCPServer,args = (u'%s'%HOST,))
    delayTCP.start()
    delayTCP.join()
    
    
import socket
    localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
    print "local ip:%s "%localIP
    
    ipList = socket.gethostbyname_ex(socket.gethostname())
    print(ipList)
    
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    print myaddr
    
    print get_ip_address('eth0')
    createTime =datetime.now()
    print createTime
    print createTime.timetuple()
    print time.mktime(createTime.timetuple())
    
    
    try:
        conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = '123456',port = 3306,charset='utf8')
        cur = conn.cursor()

        conn.select_db('liaohui')

        st_id = 6
        ed_id = 4
        cmd = "select * from networkmeasurement_passive where startNode_id = %d and endNode_id = %d order by id desc"%(st_id,ed_id)
        cur.execute(cmd)
        node = cur.fetchone()
        print node
        
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    os.system('sudo rm -r output')
    os.system('mkdir output')
    t = threading.Thread(target=MyThread)
    t.start()
    #p = Process(target = getTrace)
    #p.start()
    time.sleep(5)
    fid = open('pid.txt') #captcp will create a new process, we need to get the pid
                              #of it and "kill -2 pid" to complete it
    pid = (int)(fid.read())
    fid.close()
    print pid
    os.system('kill -2 %d'%pid)
    time.sleep(5)#wait for generating data
    
    
    
    
    
    
    st_ip = '192.168.1.177'
    ed_ips = ['202.121.178.195','219.228.12.60','202.120.199.169']
    Measure(st_ip,ed_ips)
    
    
    
    sendMsg = {'192.168.1.177': {'loss': 0.0, 'memory percent': 84.15478309981184, 'delay': -1, 'bandwidth': 0, 'throughput': 0, 'cpu percent': 17.412935323383085}, '192.168.1.2': {'loss': 0.0, 'memory percent': 83.85973932908159, 'delay': -1, 'bandwidth': 0, 'throughput': 0, 'cpu percent': 7.0}, '127.0.0.1': {'loss': 0.0, 'memory percent': 83.92249306419404, 'delay': 4.875, 'bandwidth': 0, 'throughput': 0, 'cpu percent': 8.542713567839195}}
    msg = SetPassiveMsg(sendMsg)
    print msg
    rvmsg = GetPassiveMsg(msg)
    print rvmsg
    socketMsg={}
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
        
    print socketMsg
    
    index  = [NETWORK_BANDWITH,NETWORK_DELAY,NETWORK_LOSS,NETWORK_THROUGHPUT,NETWORK_CPU,NETWORK_MEM]
        socketMsg[tmp[0]] = tmp[1]
        if tmp[1] == "":
            print "[key:%s],value is ''"%tmp[0]
            print 'End GetSocketMsg,msg is:',socketMsg
    return socketMsg'''
