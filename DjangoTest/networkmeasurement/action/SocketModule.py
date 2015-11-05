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


    def __init__(self, ip=SOCKET_TCP_IP,port=SOCKET_TCP_PORT,outtime=NETWORK_TIME_OUT):
        '''
        Constructor
        '''
        self.m_ip = ip
        self.m_port = port
        self.outtime = outtime
        #self.m_socket = socket.socket()
        
        rule = '[\d{1:3}].[\d{1:3}].[\d{1:3}].[\d{1:3}]'
        if not re.match(rule, ip):
            print 'not ip addr:',ip            
            self.m_ip = socket.gethostbyname(ip) #if param is host not ip,use func to get ip addr
            print 'after gethostbyname,ip:',self.m_ip
    
    def StartConnection(self):
        try:
            self.m_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #define socket,using TCP protocol
            print 'tcpclient:StartConnection'
            self.m_socket.settimeout(self.outtime) #set timeout == 5
            self.m_socket.connect((self.m_ip,self.m_port)) #connect server
            print 'connection success'
                        
        except socket.error, errorMsg:
            print 'tcpclient:StartConnection except'
            print sys.exc_info() #print exception infomation
            #(errno,err_msg) = errorMsg
            #print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return False #if connection failed!
        
        return True #finish send msg to server
    
    def SendMsg(self,msg=''):
        try:
            print 'tcpclient:sendMsg'
            self.m_socket.send(msg)
            print 'end send'
        except socket.error, errorMsg:
            print 'tcpclient:SendMsg except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return False #if connection failed!
        return True
            
    #receive msg from server 
    def RecvMsg(self):
        try:
            print 'tcpclient:RecvMsg'
            self.m_socket.settimeout(self.outtime)
            #self.m_socket.settimeout(25) #10s
            msg = self.m_socket.recv(SOCKET_BUFFER_SIZE)  #receive msg from server which packet size is SOCKET_BUFFER_SIZE
            print 'end recvMsg'
            #print 'end recv msg,msg=',msg
        except socket.error,errorMsg:
            print 'tcpclient:RecvMsg except'
            print sys.exc_info() #print exception infomation4
            #(errno,err_msg) = errorMsg
            #print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return None
            #print 'Connection server failed,errorMsg=%s'%(errorMsg)
            return ''
        return msg
    
        '''try:
            print 'start udp RecvMsg'            
            #SETTING TIMEOUT ??? Function.....
            self.m_socket.settimeout(NETWORK_TIME_OUT) #10s
            rcvMsg = self.m_socket.recv(SOCKET_BUFFER_SIZE) # wait for feedback msg from server
            print 'end udp RecvMsg'
            
        except socket.error,errorMsg:
            print sys.exc_info() #print exception infomation'''
    
    #close socket
    def Close(self):
        try:
            print 'tcpclient:close'
            self.m_socket.close()
            print 'end close connection'
        except socket.error,errorMsg:
            print 'tcpclient:Close except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            

#TCP Server
class TCPServer(object):
    #set ip and port to bind
    def __init__(self, ip=SOCKET_TCP_IP,port=SOCKET_TCP_PORT):
        '''
        Constructor
        '''
        self.m_ip = ip
        self.m_port = port
        #self.m_socket = socket.socket()
        
        rule = '[\d{1:3}].[\d{1:3}].[\d{1:3}].[\d{1:3}]'
        if not re.match(rule, ip):
            print 'not ip addr:',ip            
            self.m_ip = socket.gethostbyname(ip) #if param is host not ip,use func to get ip addr
            print 'after gethostbyname,ip:',self.m_ip
    
    #bin ip and port       
    def StartBind(self):
        try:
            print 'tcpserver:StartBind '
            self.m_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #define socket,using TCP protocol            
            self.m_socket.bind((self.m_ip,self.m_port)) #bind ip and port
            self.m_socket.listen(SOCKET_MAX_CLIENT) #set client num that can connect the server at same time
            print 'end StartBind tcp'
                        
        except socket.error, errorMsg:
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'bind failed:%s,errno=%d'%(err_msg,errno)
            return False #if connection failed!
        
        return True #finish send msg to server
    
    #accept connection from client
    def AcceptConnection(self):
        try:
            print 'tcpserver:accept msg from client'
            clientSock,clientAddr = self.m_socket.accept()  #get socket using to send msg to client,and client addr
            print ' end accept msg from client'
                        
        except socket.error, errorMsg:
            print 'tcpserver:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return (None,None) #if fail,return None
        
        return (clientSock,clientAddr) #finish send msg to server
    #close socket
    def Close(self):
        try:
            print 'tcpserver:close'
            self.m_socket.close()
            print 'end tcpserver:close'
        except socket.error,errorMsg:
            print 'tcpserver:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            
            
#UDP Server
class UDPServer(object):
    def __init__(self,ip=SOCKET_UDP_IP,port=SOCKET_UDP_PORT):
        self.m_ip = ip
        self.m_port = port
        rule = '[\d{1:3}].[\d{1:3}].[\d{1:3}].[\d{1:3}]'
        if not re.match(rule, ip):
            print 'not ip addr:',ip            
            self.m_ip = socket.gethostbyname(ip) #if param is host not ip,use func to get ip addr
            print 'after gethostbyname,ip:',self.m_ip
    
    #bind local ip and port using udp protocol
    def StartBind(self):
        try:
            print 'udpserver:StartBind udp server'
            self.m_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  #define udp socket, using socket_dgram
            self.m_socket.bind((self.m_ip,self.m_port)) # bind ip and port 
            print 'udpserver:end StartBind udp server'
        except socket.error,errorMsg:
            print 'udpserver:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'bind udp server failed:%s,errno=%d'%(err_msg,errno)
            return False # bind failed
        return True  #bind success
    
    #recvMsg from client and send feedback msg to client
    def RecvClientMsg(self):
        try:
            print 'udpserver:Received msg from client'            
            rcvMsg, clientAddr = self.m_socket.recvfrom(1024)  #receive data(rcvMsg) and client addr info(ip and port) from client
            self.m_clientAddr = clientAddr  #init for sending feedback msg to client in Func SendFeedbackMsg
            print 'Received from %s:%s.' % clientAddr
            print ' end Received msg from client'                        
        except socket.error, errorMsg:
            print 'udpserver:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            return None #if fail,return None
        
        return rcvMsg  #return msg that receive from client
    
    #send feedback msg to client
    def SendFeedbackMsg(self,msg):
        try:
            print 'udpserver:SendFeedbackMsg msg to client,%s:%s'%self.m_clientAddr
            self.m_socket.sendto(msg, self.m_clientAddr)
            print ' end SendFeedbackMsg msg to client'                        
        except socket.error, errorMsg:
            print 'udpserver:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'SendFeedbackMsg failed:%s,errno=%d'%(err_msg,errno)
            
          
    #close socket
    def Close(self):
        try:
            print 'udpserver:close'
            self.m_socket.close()
            print 'end close udp server'
        except socket.error,errorMsg:
            print 'udpserver:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
            
 #UDP Server
class UDPClient(object):
    #default ip:SOCKET_UDP_IP;default port:SOCKET_UDP_PORT
    def __init__(self,ip=SOCKET_UDP_IP,port=SOCKET_UDP_PORT):
        self.m_ip = ip
        self.m_port = port
        rule = '[\d{1:3}].[\d{1:3}].[\d{1:3}].[\d{1:3}]'
        if not re.match(rule, ip):
            print 'not ip addr:',ip            
            self.m_ip = socket.gethostbyname(ip) #if param is host not ip,use func to get ip addr
            print 'after gethostbyname,ip:',self.m_ip
    
      
    def SendMsg(self,msg=''):
        try:
            print 'udpclient:start SendToServer'
            self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #using udp(socket_dgram) to send msg
            self.m_socket.sendto(msg, (self.m_ip,self.m_port))  #send to server which ip is self.ip,port is self.port
            print 'end SendToServer'
            
        except socket.error,errorMsg:
            print 'udpclient:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'send msg to server failed:%s,errno=%d'%(err_msg,errno)
            return False
        return True
    #receive msg from client,waiting...
    def RecvMsg(self):        
        try:
            print 'udpclient:RecvMsg'            
            #SETTING TIMEOUT ??? Function.....
            self.m_socket.settimeout(NETWORK_TIME_OUT) #10s
            rcvMsg = self.m_socket.recv(SOCKET_BUFFER_SIZE) # wait for feedback msg from server
            print 'end udp RecvMsg'
            
        except socket.error,errorMsg:
            print 'udpclient:except'
            print sys.exc_info() #print exception infomation
            #(err_msg) = errorMsg
            #print 'RecvMsg failed:%s,errno=%d'%(err_msg,errno)
            print 'Connection server failed,errorMsg=%s'%(errorMsg)
            return ''
        return rcvMsg
    
    #close socket
    def Close(self):
        try:
            print 'udpclient:close'
            self.m_socket.close()
            print 'end close udp server'
        except socket.error,errorMsg:
            print 'udpclient:except'
            print sys.exc_info() #print exception infomation
            (errno,err_msg) = errorMsg
            print 'Connection server failed:%s,errno=%d'%(err_msg,errno)
        
        
               