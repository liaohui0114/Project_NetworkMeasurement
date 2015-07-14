 # -*- coding: UTF-8 -*- 
import socket
import sys
import time
import threading
import sys
from JsonAction import  *
import MySQLdb

 
if __name__ == '__main__':
#def passiveClient():
    '''try:
        conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = '123456',port = 3306)
        cur = conn.cursor()
        
        conn.select_db('liaohui')
        
        node = cur.execute('select * from networkmeasurement_schoolnode')
        print 'node',node
        
        node2 = cur.fetchone()
        print node2
        if node2[1] == '上海交通大学':
            print 11111111
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])'''
    allNodes = GetNodes()
    print allNodes    
    
    '''protocol = sys.argv[1]
    st_ip = sys.argv[2]
    dest_ip = sys.argv[3]
    tp = TCPClient(st_ip,SOCKET_TCP_PORT)
    

    if tp.StartConnection():
        msg = {NETWORK_IP:dest_ip,NETWORK_PROTOCOL:protocol}
        tp.SendMsg(SetSocketMsg(msg))
        rsg = tp.RecvMsg()
        print 'Get Info from server:'
        rsgDic = GetSocketMsg(rsg)
        for key,value in rsgDic.items():
            print key,value
            
        tp.Close()
    print 'end'
    '''