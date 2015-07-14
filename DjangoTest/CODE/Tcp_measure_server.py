#!/usr/bin/env python
import sys
from TCPSocket import *
from GlobleVariable import *
import threading
import time

def MyThread(clientSocket,clientAddr):
    print 'MyThread to deal with connection from %s:%s'%(clientAddr)
    #print type(clientAddr),len(clientAddr)
    count = 5
    while count>0:
        count = count - 1
        msg = clientSocket.recv(17)
        recv_time = time.time()
        clientSocket.send(str("%f"%recv_time))
        print 'send time: %s'%msg
        print 'recived time: %f'%recv_time
    clientSocket.close()
    print 'End MyThread to deal with connection from %s:%s'%(clientAddr)


if __name__ == '__main__':
    HOST = sys.argv[1]
    tcp_measure_server = TCPServer(HOST,DELAY_TCP_PORT)
    if tcp_measure_server.StartBind():
        while True:
            clientSocket,clientAddr = tcp_measure_server.AcceptConnection()
            if clientSocket == None and clientAddr == None:
                continue

            t = threading.Thread(target=MyThread,args=(clientSocket,clientAddr))
            t.start()
        tcp_measure_server.CloseServer()
