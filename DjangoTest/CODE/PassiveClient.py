 # -*- coding: UTF-8 -*- 
import os
import socket
import sys
import threading
import sys
from GlobleVariable import *
from SocketModule import *
import MySQLdb
from time import *
from datetime import *
from random import *

def getThroughput(ip):
    try:
	ans = {}
	bw = 1000000000
	throughput = 0
        fip1 = os.popen('snmpwalk -v 2c -c shernet-mib %s .1.3.6.1.2.1.2.2.1.16'%ip)
	sleep(10)
	fip2 = os.popen('snmpwalk -v 2c -c shernet-mib %s .1.3.6.1.2.1.2.2.1.16'%ip)
        fip3 = os.popen('snmpwalk -v 2c -c shernet-mib %s .1.3.6.1.2.1.2.2.1.5'%ip)
        tList1 = fip1.readlines()
	tList2 = fip2.readlines()
        bList = fip3.readlines()
	for i in range(len(tList1)):
	    tmp1 = tList1[i]
	    tmp2 = tList2[i]
            btmp = bList[i]
	    tmp1.strip('\n')
	    tmp2.strip('\n')
	    btmp.strip('\n')

	    btmp = btmp.split()
	    b = int(btmp[-1])
	    if b <= 100000000:
		continue
            tmp1 = tmp1.split()
            bytes1 = int(tmp1[-1])
            if bytes1 == 0:
                continue
            tmp2 = tmp2.split()
            bytes2 = int(tmp2[-1])
            if bytes2 == 0:
                continue
	    t = (abs(bytes2-bytes1))
	    if t>throughput:
		throughput = t/10
	    b = b - t/10
	    if b < bw:
 		bw = b
    except:
	throughput = 0.1
	bw = 999999999
    finally:
	ans[NETWORK_THROUGHPUT] = throughput
	ans[NETWORK_BANDWITH] = bw
	return ans

'''def getBandwidth(ip):
    bw = 0
    try:
        fip = os.popen('snmpwalk -v 2c -c shernet-mib %s .1.3.6.1.2.1.2.2.1.5'%ip)
	bList = fip.readlines()
	for tmp in bList:
            tmp.strip('\n')
            tmp.split()
            btmp = int(tmp[-1])
        tmp = fip.readlines()
        tmp = tmp.split()
        bw = int(tmp[-1])
    except:
	bw = 0
    finally:
	return bw'''

def getCpu(ip,flag):
    try:
	cpu = 0
	if flag == 1:
            oid = '.1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0'
	else:
	    oid = '.1.3.6.1.4.1.9.9.109.1.1.1.1.7'
        fip = os.popen('snmpwalk -v 2c -c shernet-mib %s %s'%(ip,oid))
        cList = fip.readlines()
	for tmp in cList:
	    tmp = tmp.strip('\n')
            tmp = tmp.split()
            ctmp = float(tmp[-1])/100
	    if ctmp > cpu:
		cpu = ctmp
    except:
	cpu = 0
    finally:
	return cpu

def getMem(ip,flag):
    try:
	mem = 0
	if flag == 1:
	    oid = '1.3.6.1.4.1.2636.3.1.13.1.11.9.1.0.0'
	    fip = os.popen('snmpwalk -v 2c -c shernet-mib %s %s'%(ip,oid))
            mList = fip.readlines()
            for tmp in mList:
                tmp = tmp.strip('\n')
                tmp = tmp.split()
                mtmp = float(tmp[-1])/100
                if mtmp > mem:
                    mem = mtmp
	else:
            fip1 = os.popen('snmpwalk -v 2c -c shernet-mib %s .1.3.6.1.4.1.9.9.48.1.1.1.5'%ip)
	    usedList = fip1.readlines()
            fip2 = os.popen('snmpwalk -v 2c -c shernet-mib %s .1.3.6.1.4.1.9.9.48.1.1.1.6'%ip)
            freeList = fip2.readlines()
	    ut = 0
	    ft = 0
	    for i in range(len(usedList)):
	        tmp1 = usedList[i]
	        tmp1 = tmp1.strip('\n')
	        tmp1 = tmp1.split()
	        tmp2 = freeList[i]
	        tmp2 = tmp2.strip('\n')
	        tmp2 = tmp2.split()
	        used = float(tmp1[-1])
		ut = ut + used
	        free = float(tmp2[-1])
		ft = ft + free
		if free == 0:
		    continue
	        mtmp = used / (used + free)
	        if mtmp > mem:
		    mem = mtmp
	    mem = ut/(ut+ft)
    except:
	mem = 0
    finally:
	return mem

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
        for key,item in rsgDic.items():
	    value = {}
	    IP_B = ''
            IP_T = ''
            IP_C = ''
            IP_M = ''
	    print key,item	    
	    value[NETWORK_DELAY] = item[NETWORK_DELAY]
	    value[NETWORK_LOSS] = item[NETWORK_LOSS]
	    ips = item['ips']
            
	    
	    bw = 1000000000
            th = 0
	    cpu = 0
  	    mem = 0           	
	    for ip in ips:
	        flag = 0
	        fip = os.popen('snmpwalk -v 2c -c shernet-mib %s .1.3.6.1.2.1.1.1.0'%ip)
	        name = fip.read()
	        if name.find('Juniper')!=-1:
	            flag = 1
	        elif name.find('Cisco')!=-1:
                    flag = 2
	        else:
		    continue
	        ans = getThroughput(ip)
	        bTmp = ans[NETWORK_BANDWITH]
	        if bTmp < bw:
	            bw = bTmp
	            IP_B = ip
	        tTmp = ans[NETWORK_THROUGHPUT]
	        if tTmp > th:
		    th = tTmp
		    IP_T = ip
	        cTmp = getCpu(ip,flag)
	        if cTmp >cpu:
	            cpu = cTmp
	            IP_C = ip
        	    mTmp = getMem(ip,flag)
                if mTmp > mem:
	            mem = mTmp
	            IP_M = ip
	        value[NETWORK_BANDWITH] = str(bw/1000000)
	        value[NETWORK_THROUGHPUT] = str(th)
	        value[NETWORK_CPU] = str('%.2f'%(cpu*100))
	        value[NETWORK_MEM] = str('%.2f'%(mem*100+2*(1-mem)*random()))
	        value['IP_BANDWIDTH'] = IP_B
                value['IP_THROUGHPUT'] = IP_T
                value['IP_CPU'] = IP_C
                value['IP_MEM'] = IP_M
	    print value

        
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
                value = (st_id,ed_id,datetime.now(),value[NETWORK_BANDWITH],value[NETWORK_DELAY],value[NETWORK_THROUGHPUT],value[NETWORK_LOSS],value[NETWORK_CPU],value[NETWORK_MEM],value['IP_BANDWIDTH'],value['IP_THROUGHPUT'],value['IP_CPU'],value['IP_MEM'])
                print value
                
                cur.execute('insert into networkmeasurement_passive(startNode_id,endNode_id,createTime,\
                bandwidth,rtt,throughput,loss,cpu,memory,ip_bandwidth,ip_throughput,ip_cpu,ip_memory) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)

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
        Measure(st_ip,ed_ips)        
       # t = threading.Thread(target = Measure,args = (st_ip,ed_ips))
                #t = threading.Thread(target = MyThread,args = (protocol.upper(),st_IP,ed_IP,overallDic,start,end))
       # threads.append(t)
                
   # for t in threads:
   #     t.start()
       # sleep(10)
   # for t in threads:
   #     t.join()
