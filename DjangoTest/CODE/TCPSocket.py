import GlobleVariable
from GlobleVariable import *
import re
import socket
import sys
import threading

#TCP Client
class TCPClient(object):
    '''
    classdocs
    '''


    def __init__(self, ip=SOCKET_SERVER_IP,port=SOCKET_SERVER_PORT):
        '''
        Constructor
        '''
        self.m_ip = ip
        self.m_port = port
        #self.m_socket = socket.socket()
        
        rule = '[/d{1:3}].[/d{1:3}].[/d{1:3}].[/d{1:3}]'
        if not re.match(rule, ip):
            print 'not ip addr:',ip            
            self.m_ip = socket.gethostbyname(ip) #if param is host not ip,use func to get ip addr
            print 'after gethostbyname,ip:',self.m_ip
    
    def StartConnection(self):
        try:
            self.m_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #define socket,using TCP protocol
            print 'start connection to server'
            self.m_socket.connect((self.m_ip,self.m_port)) #connect server
            print 'connection success'
                        
        except socket.error, errorMsg:
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return False #if connection failed!
        
        return True #finish send msg to server
    
    def SendMsg(self):
        try:
            msg = SetSocketMsg(self.m_ip,self.m_port)
        
            print 'send data to server,data:',msg
            self.m_socket.send(msg)
            print 'end send'
        except socket.error, errorMsg:
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return False #if connection failed!
        return True
            
    #receive msg from server 
    def RecvMsg(self):
        try:
            print 'start recv msg'
            msg = self.m_socket.recv(SOCKET_BUFFER_SIZE)  #receive msg from server which packet size is SOCKET_BUFFER_SIZE
            print 'end recv msg'
        except socket.error,errorMsg:
            print sys.exc_info() #print exception infomation4
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return None
        print 'recv msg is:',msg
        return msg
    
    #close socket
    def CloseConnection(self):
        try:
            print 'start close connection'
            self.m_socket.close()
            print 'end close connection'
        except socket.error,errorMsg:
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            

#TCP Server
class TCPServer(object):
    #set ip and port to bind
    def __init__(self, ip=SOCKET_SERVER_IP,port=SOCKET_SERVER_PORT):
        '''
        Constructor
        '''
        self.m_ip = ip
        self.m_port = port
        #self.m_socket = socket.socket()
        
        rule = '[/d{1:3}].[/d{1:3}].[/d{1:3}].[/d{1:3}]'
        if not re.match(rule, ip):
            print 'not ip addr:',ip            
            self.m_ip = socket.gethostbyname(ip) #if param is host not ip,use func to get ip addr
            print 'after gethostbyname,ip:',self.m_ip
    
    #bin ip and port       
    def StartBind(self):
        try:
            self.m_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #define socket,using TCP protocol
            print 'start bind server'
            self.m_socket.bind((self.m_ip,self.m_port)) #bind ip and port
            self.m_socket.listen(SOCKET_MAX_CLIENT) #set client num that can connect the server at same time
            print 'bind success'
                        
        except socket.error, errorMsg:
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'bind failed:%s,errno=%d'%(err_msg,errno)
            return False #if connection failed!
        
        return True #finish send msg to server
    
    #accept connection from client
    def AcceptConnection(self):
        try:
            print 'accept msg from client'
            clientSock,clientAddr = self.m_socket.accept()  #get socket using to send msg to client,and client addr
            print ' end accept msg from client'
                        
        except socket.error, errorMsg:
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return (None,None) #if fail,return None
        
        return (clientSock,clientAddr) #finish send msg to server
    #close socket
    def CloseServer(self):
        try:
            print 'start close connection'
            self.m_socket.close()
            print 'end close connection'
        except socket.error,errorMsg:
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
        
        
