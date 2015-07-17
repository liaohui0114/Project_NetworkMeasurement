 # -*- coding: UTF-8 -*- 
import socket
import sys
import time
import threading
import sys
from GlobleVariable import *
from SocketModule import *
import MySQLdb
from datetime import *



def Measure(st_ip,ed_ips):
    tp = TCPClient(st_ip,SOCKET_TCP_PORT)
    if tp.StartConnection():
        msg = {NETWORK_IP:ed_ips,NETWORK_PROTOCOL:'PASSIVE'}
        tp.SendMsg(SetSocketMsg(msg))
        rsg = tp.RecvMsg()
        print 'Get Info from server:'
        rsgDic = GetPassiveMsg(rsg)
        print rsgDic
        st_ip = "'"+st_ip + "'"
        for key,value in rsgDic.items():
            print key,value
            try:
                conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'root',port = 3306,charset='utf8')
                cur = conn.cursor()
        
                conn.select_db('network')
            
                
                cmd = "select * from networkmeasurement_schoolnode where nodeIp = %s"%st_ip
                print cmd
                cur.execute(cmd)
                node = cur.fetchone()
                print node
                st_id = node[0]
            
                ed_ip = "'"+key + "'"
                cmd = "select * from networkmeasurement_schoolnode where nodeIp = %s"%ed_ip
                print cmd
                cur.execute(cmd)
                node = cur.fetchone()
                print node
                ed_id = node[0]
            
            
                cur.execute('select * from networkmeasurement_passive')
                value = (st_id,ed_id,datetime.now(),value[NETWORK_BANDWITH],value[NETWORK_DELAY],value[NETWORK_THROUGHPUT],value[NETWORK_LOSS],value[NETWORK_CPU],value[NETWORK_MEM])
                print value
                
                cur.execute('insert into networkmeasurement_passive(startNode_id,endNode_id,createTime,\
                bandwidth,rtt,throughput,loss,cpu,memory) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
                print 3
                conn.commit()
                cur.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
            
        
            
        tp.Close()
 
#if __name__ == '__main__':
def passiveClient():
    try:
        #names of nodes
        DEST_NAME = []
        #ip of nodes
        DEST_IP = {}
        conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'root',port = 3306,charset='utf8')
        cur = conn.cursor()
        
        conn.select_db('network')
        cur.execute('select * from networkmeasurement_schoolnode')
        
        nodes = cur.fetchall()
        for node in nodes:
            DEST_NAME.append(node[1])
            DEST_IP[node[1]] = node[2]
            
        #print DEST_NAME
        #print DEST_IP
            

        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
    #DEST_NAME = ['上海交通大学','复旦大学','上海大学','实验室']
    #DEST_IP = {'上海交通大学':'202.121.178.195','复旦大学':'219.228.12.60','上海大学':'202.120.199.169','实验室':'192.168.1.177'}
    #print DEST_NAME[2]
    #st_node = DEST_NAME[0]
    #ed_node = DEST_NAME[2]
    #st_ip = DEST_IP[st_node]
    #ed_ip = DEST_IP[ed_node]
    #Measure(st_ip,ed_ip)
    
    threads = []
    for st_node in DEST_NAME:
        tmp_node = list(DEST_NAME)
        tmp_node.remove(st_node)
        ed_ips = []
        for ed_node in tmp_node:
            if st_node != ed_node:
                st_ip = DEST_IP[st_node]
                #ed_ip = DEST_IP[ed_node]
                ed_ips.append(DEST_IP[ed_node])
                
        t = threading.Thread(target = Measure,args = (st_ip,ed_ips))
                #t = threading.Thread(target = MyThread,args = (protocol.upper(),st_IP,ed_IP,overallDic,start,end))
        threads.append(t)
                
    for t in threads:
        t.start()
    for t in threads:
        t.join()