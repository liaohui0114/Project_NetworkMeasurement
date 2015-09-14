# -*- coding:utf-8 -*- 
#!/usr/bin/env python
from django.http import HttpResponse
from django.shortcuts import render_to_response
import json,os,sys,datetime,time,string
from  GlobleVariable import *
from Client import *
from datetime import *
import threading
import time
import MySQLdb
from networkmeasurement.models import SchoolNode,Active,Passive,NetProtocol
from time import sleep


#DEFAULT SETTING
DEFAULT_UDP_COND = {NETWORK_BANDWITH:'100(Mbs)',NETWORK_DELAY:'0(ms)',NETWORK_JITTER:'0.1(ms)',NETWORK_LOSS:'0(%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}
DEFAULT_OVERALL_COND = {NETWORK_BANDWITH:'',NETWORK_DELAY:'',NETWORK_JITTER:'',NETWORK_LOSS:'',NETWORK_CONGESTION:'',NETWORK_AVAIL:''}
TAG_UNREACHABLE = '*' #当网络不可达时，在网页显示
TAG_CONGESTION = '20 %'  #当丢包率超过TAG_CONGESTION是，表示网络用赛
TAG_ISCONGESTION = 15.0
#判断是否拥塞
def isCongestion(percentStr):
    tmpArray = percentStr.split('%')
    print 'tmpArray:',tmpArray
    if float(tmpArray[0]) >= TAG_ISCONGESTION:
        return 'YES'
    else:
        return 'NO'
#function:获取图标信息，即获取各个节点的最近十条记录
def GetSingleChart(protocol,st_ip):
    print 'GetSingleChart'
    chartData = [] #return msg
    createTime = {}
    #to judge if the protocol was exist
    #print protocol
    #protocol = '"'+protocol+'"'
    #print protocol
    #A = NetProtocol.objects.filter(protocolName = protocol)
    #print 111111111111,A
    if NetProtocol.objects.filter(protocolName=protocol).exists() and SchoolNode.objects.filter(nodeIp=st_ip).exists():
        pro = NetProtocol.objects.get(protocolName=protocol)  #to get protocol_id
        nodeInfo = SchoolNode.objects.all().exclude(nodeIp=st_ip)  #to get all nodes info exclude start_node
        st_node = SchoolNode.objects.get(nodeIp=st_ip) #to get startNode
        
        if nodeInfo.exists():#to get all nodes info in DB
            for i in nodeInfo:
                tmpDic = {}
                tmpDic['name']=i.nodeName
                #print i.nodeName
                cond = Active.objects.order_by('-id').filter(protocol=pro,startNode=st_node,endNode=i)[:10]  #获取最后十个，即：按id降序排列，获取前十个
                if cond.exists():
                    tmpDic['data'] = [item.bandwidth for item in cond] #here we only display bandwidth conditions
                    chartData.append(tmpDic)
                    
                    #get createTime {'name1':[time1,time2,time3],'name':[...]}
                    tmpKey = i.nodeName
                    createTime[tmpKey] = []
                    for item in cond:
                        createTime[tmpKey].append(time.mktime(item.createTime.timetuple()))
        
    #print chartData
    print 'end GetSingleChart()'
    return chartData,createTime

#to change netMsg(str) to float/bool
def readNetMsg(netMsg):
    data = {}
    print 'readNetMsg',netMsg
    #bandwidth = netMsg[NETWORK_BANDWITH]
    #print bandwidth
    #if bandwidth == '':
    print netMsg.has_key(NETWORK_BANDWITH)
    if netMsg.has_key(NETWORK_BANDWITH) == False:
        data[NETWORK_BANDWITH] = 0
    elif netMsg[NETWORK_BANDWITH] == '':
        data[NETWORK_BANDWITH] = 0
    else:
        bandwidth = netMsg[NETWORK_BANDWITH]
        bandwidth = bandwidth.split()
        data[NETWORK_BANDWITH] = float(bandwidth[0])
        if bandwidth[1] == 'Gbit/sec':
            data[NETWORK_BANDWITH] = data[NETWORK_BANDWITH]*1000
        elif bandwidth[1] == 'Kbit/sec':
            data[NETWORK_BANDWITH] = data[NETWORK_BANDWITH]/1000
        elif bandwidth[1] == 'bit/sec':
            data[NETWORK_BANDWITH] = data[NETWORK_BANDWITH]/1000000
    print data[NETWORK_BANDWITH]

    if netMsg.has_key(NETWORK_DELAY) == False:
        data[NETWORK_DELAY] = 0
    elif netMsg[NETWORK_DELAY] == '':
        data[NETWORK_DELAY] = 0
    else:
        delay = netMsg[NETWORK_DELAY]
        delay = delay.split()
        data[NETWORK_DELAY] = float(delay[0])
    print data[NETWORK_DELAY]

    
    if netMsg.has_key(NETWORK_JITTER) == False:
        data[NETWORK_JITTER] = 0
    elif netMsg[NETWORK_JITTER] == '':
        data[NETWORK_JITTER] = 0
    else:
        jitter = netMsg[NETWORK_JITTER]
        jitter = jitter.split()
        data[NETWORK_JITTER] = float(jitter[0])
    print data[NETWORK_JITTER]
    
    
    if netMsg.has_key(NETWORK_LOSS) == False:
        data[NETWORK_LOSS] = 0
    elif netMsg[NETWORK_LOSS] == '':
        data[NETWORK_LOSS] = 0
    else:
        loss = netMsg[NETWORK_LOSS]
        loss = loss.split()
        data[NETWORK_LOSS] = float(loss[0])
    print data[NETWORK_LOSS]

    '''try:
        conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'root',port = 3306,charset='utf8')
        cur = conn.cursor()
        
        conn.select_db('liaohui')
            
                
        cmd = "select * from networkmeasurement_schoolnode where nodeIp = %s"%st_ip
        print cmd
        cur.execute(cmd)
        node = cur.fetchone()
        print node
        st_id = node[0]
            
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])'''

    if netMsg.has_key(NETWORK_CONGESTION) == True and netMsg[NETWORK_CONGESTION] == 'YES':
        data[NETWORK_CONGESTION] = True
    else:
        data[NETWORK_CONGESTION] = False
    print data[NETWORK_CONGESTION]

    if netMsg.has_key(NETWORK_AVAIL) == True and netMsg[NETWORK_AVAIL] == 'YES':
        data[NETWORK_AVAIL] = True
    else:
        data[NETWORK_AVAIL] = False
    print data[NETWORK_AVAIL]
   
    return data
#use tool graphviz to draw trace path:sudo apt-get install graphviz
def graphvizFunc(tracerouteDic,picUrl=""):
    print 'graphvizFunc'
    #print picUrl
    #tranform tracerouteDic to two lists,IP_list=[key1,key2,...] and Room_list=[value1,value2,...]
    IP_list=[]
    Room_list=[]
    traceKeys = tracerouteDic.keys()
    traceKeys.sort()  #sort dic by key
    for key in traceKeys:
        IP_list.append(key)
        Room_list.append(tracerouteDic[key])
    #print 'iplist:',IP_list
    #print 'roomlist:',Room_list
    
    li = []
    li.append("digraph G {\n")
    last_line=""
    for n in range(len(IP_list)):
        num2 = n/5
        if num2 % 2 == 0:
            num1 = n%5*3
        else:
            num1 = 12 - n%5*3
        num2 *= -1
    
        if Room_list[n] != "":
            temp_String = str(n)+"[label=\""+IP_list[n]+" "+Room_list[n]+"\" pos = \"";
            
            temp_String = temp_String + str(num1) + "," + str(num2) + "!\"]\n"
        else:
            temp_String = str(n)+"[label=\""+IP_list[n]+"\" pos = \"";
            temp_String = temp_String + str(num1) + "," + str(num2) + "!\"]\n"
    
        li.append(temp_String);
        last_line = last_line + str(n) + "->"
    
    last_line = last_line[:-2]
    last_line += "\n"
    li.append(last_line)
    li.append("}")
    
    ISOTIMEFORMAT='%Y-%m-%d_%X'
    time_char = time.strftime(ISOTIMEFORMAT, time.gmtime(time.time()))
    #print "maybe it's here,li=",li
    #connection_file = "./" + time_char + "_draw_traceroute.dot"
    connection_file = picUrl+ time_char + "_draw_traceroute.dot"
    #print 'connection file:',connection_file
    f=file(connection_file,"w+")
    #f.writelines(li)
    print 'open'
    for i in li:
        print "i:",i
        f.write(i)
        f.flush()
    #print 'after write'
    f.close()
    
    #print 'before'
    command = "neato -Tsvg " + connection_file + " -o %s"%(picUrl)+time_char+".svg"
    #print '2222'
    rmCmd = "rm -rf %s*.svg"%(picUrl)
    #print '333'
    os.system(rmCmd) # remove all .svg files before when we call this func every time
    os.system(command)
    #print '333'
    os.system("chmod 777 -R *.svg")
    os.remove(connection_file)
    print 'end graphvizFunc'
    return time_char+".svg" #return pic's name
    
    
#function:to get point to point network cond
def SingleAction(request):
    print 'SingleAction'
    if request.method == "POST":
        print 'SingleAction,if request.method == POST '
        tmp = request.POST
        ##在apache部署后需要注释下面两行才能继续执行，在/var/log/apache2/error.log只打印一行就卡住了？？？？下面的一些在for循环中的print也是，注释后才能正常执行
        #for i,j in tmp.items():
        #    print i,j  #print msg from front page
#         netMsg = Client();
#         for key,value in netMsg.items():
#             DEFAULT_UDP_COND[key] = value #set true attribute
#         print DEFAULT_UDP_COND
    ######to get network infos,start Client
        #allnodes = SchoolNode.objects.all()
        #print allnodes
        print 'tmp:',tmp
        protocol =  tmp['protocol']
        st_IP = tmp['startNodeIp']
        end_IP = tmp['endNodeIp']
        st_name = tmp['startNodeName']
        ed_name = tmp['endNodeName']
        print st_IP,end_IP
        netMsg = Client(protocol.upper(),st_IP,end_IP); # to get network condition using action.Client.py
        print 'netMsg:',netMsg
        
        isReachable = True  #判断网络是否可达
        # st_ip不可达
        if netMsg == -1:
            netMsg = {NETWORK_BANDWITH:'0 (Mbs)',NETWORK_DELAY:'0 (ms)',NETWORK_JITTER:'0 (ms)',NETWORK_LOSS:'0 (%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'起始主机故障'}
            #netMsg = {NETWORK_BANDWITH:TAG_UNREACHABLE,NETWORK_DELAY:TAG_UNREACHABLE,NETWORK_JITTER:TAG_UNREACHABLE,NETWORK_LOSS:TAG_UNREACHABLE,NETWORK_CONGESTION:TAG_UNREACHABLE,NETWORK_AVAIL:'起始结点故障'}
            isReachable = False #起始结点不可达

        ###end_ip不可达
        if netMsg[NETWORK_AVAIL] == 'NO':
            netMsg = {NETWORK_BANDWITH:'0 (Mbps)',NETWORK_DELAY:'0 (ms)',NETWORK_JITTER:'0 (ms)',NETWORK_LOSS:'0 (%)',NETWORK_CONGESTION:'YES',NETWORK_AVAIL:'目标结点不可达'}
            isReachable = False #目标结点结点不可达
            #netMsg = {NETWORK_BANDWITH:TAG_UNREACHABLE,NETWORK_DELAY:TAG_UNREACHABLE,NETWORK_JITTER:TAG_UNREACHABLE,NETWORK_LOSS:TAG_UNREACHABLE,NETWORK_CONGESTION:TAG_UNREACHABLE,NETWORK_AVAIL:'目标结点不可达'}

        #设置返回给.js文件的数据
        for key,value in netMsg.items():
            DEFAULT_UDP_COND[key] = value #set true attribute
            #added by liaohui
            if isReachable == False and key != NETWORK_AVAIL:
                DEFAULT_UDP_COND[key] = TAG_UNREACHABLE #设置不可达时页面显示的结果
        
        #判断：如果丢包率过高，我们认为网络拥塞   
        if isReachable == True:
            DEFAULT_UDP_COND[NETWORK_CONGESTION] = isCongestion(DEFAULT_UDP_COND[NETWORK_LOSS])
        print DEFAULT_UDP_COND
        
        
        try:
            conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'root',port = 3306,charset='utf8')
            cur = conn.cursor()

            conn.select_db('network')

            st_name = "'"+st_name + "'"
            cmd = "select * from networkmeasurement_schoolnode where nodeName = %s"%st_name
            cur.execute(cmd)
            node = cur.fetchone()
            st_id = node[0]

            ed_name = "'"+ed_name + "'"
            cmd = "select * from networkmeasurement_schoolnode where nodeName = %s"%ed_name
            cur.execute(cmd)
            node = cur.fetchone()
            ed_id = node[0]

            tempProtocol = "'"+protocol + "'"
            cmd = "select * from networkmeasurement_netprotocol where protocolName = %s"%tempProtocol
            cur.execute(cmd)
            node = cur.fetchone()
            protocol_id = node[0]

            if protocol_id ==1:#for TCP,we get the data loss from passive data
                cmd = "select * from networkmeasurement_passive where startNode_id = %d and endNode_id = %d order by id desc"%(st_id,ed_id)
                print cmd
                cur.execute(cmd)
                index = cur.fetchone()
                if index == None:
                    loss = 0
                else:
                    loss = index[4]
                if isReachable:
                    DEFAULT_UDP_COND[NETWORK_LOSS] = str(loss) + ' %'  #tcp格式，默认无%
                #print DEFAULT_UDP_COND[NETWORK_LOSS]

            cur.execute('select * from networkmeasurement_active')

            data = readNetMsg(netMsg)   #将获取的各个指标转化成数据库对应的存储格式：str->double

            if protocol_id == 1:
                data[NETWORK_LOSS] = loss
            print 'data',data

            value = (st_id,ed_id,protocol_id,datetime.now(),data[NETWORK_BANDWITH],data[NETWORK_DELAY],data[NETWORK_JITTER],data[NETWORK_LOSS],data[NETWORK_CONGESTION],data[NETWORK_AVAIL])
            #print value
            '''sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
                   LAST_NAME, AGE, SEX, INCOME) \
                   VALUES ('%s', '%s', '%d', '%c', '%d' )" % ('Mac', 'Mohan', 20, 'M', 2000)'''
                   
            '''sql = "insert into networkmeasurement_active(startNode_id,endNode_id,protocol_id,createTime,\
            bandwidth,delay,jitter,loss,congestion,avail) values('%d','%d','%d','%s','%f','%f','%f','%f','%s','%s')"%value'''
            
            cur.execute('insert into networkmeasurement_active(startNode_id,endNode_id,protocol_id,createTime,\
            bandwidth,delay,jitter,loss,congestion,avail) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)

            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
        '''chartData = [{'name': '上海交通大学','data': [20, 21, 28.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 19.6]},
                     {'name': '华东师范大学','data': [5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]},
                     {'name': '复旦大学','data': [3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]},
                     {'name': '同济大学','data': [5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]}]'''
        
        chartData,time = GetSingleChart(protocol.upper(),st_IP)
        chartTime = [1,2,3,4,5,6,7,8,9,10]
        #print "tttttttime,",time
        reMsg = {"single":DEFAULT_UDP_COND,"chart":{"chartData":chartData,"chartTime":chartTime,"time":time}}   #we will decode this format by .js
        #time.sleep(4) #for test
        return HttpResponse(json.dumps(reMsg), content_type="application/json")
    print 'end SingleAction'


#threading for overallaction

def MyThread(protocol,st_IP,ed_IP,overallDic,start,end):
    print 'st_IP:',st_IP,'ed_ip:',ed_IP
    tmp_cond = Client(protocol.upper(),st_IP,ed_IP);
    
    if st_IP == '202.120.199.169' and ed_IP == '219.228.12.60':
        print 'tmp_cond:',tmp_cond
    if tmp_cond == -1:
        #tmp_cond = {NETWORK_BANDWITH:'0 (Mbs)',NETWORK_DELAY:'0 (ms)',NETWORK_JITTER:'0 (ms)',NETWORK_LOSS:'0 (%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'NO,起始结点故障'}
        tmp_cond = {NETWORK_BANDWITH:TAG_UNREACHABLE,NETWORK_DELAY:TAG_UNREACHABLE,NETWORK_JITTER:TAG_UNREACHABLE,NETWORK_LOSS:TAG_UNREACHABLE,NETWORK_CONGESTION:TAG_UNREACHABLE,NETWORK_AVAIL:'起始结点故障'}

        ###end client######3
    if tmp_cond[NETWORK_AVAIL] == 'NO':
        #tmp_cond = {NETWORK_BANDWITH:'0 (Mbs)',NETWORK_DELAY:'0 (ms)',NETWORK_JITTER:'0 (ms)',NETWORK_LOSS:'0 (%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'NO,目标结点不可达'}
        tmp_cond = {NETWORK_BANDWITH:TAG_UNREACHABLE,NETWORK_DELAY:TAG_UNREACHABLE,NETWORK_JITTER:TAG_UNREACHABLE,NETWORK_LOSS:TAG_UNREACHABLE,NETWORK_CONGESTION:TAG_UNREACHABLE,NETWORK_AVAIL:'目标结点不可达'}
    #tmp_cond = {NETWORK_BANDWITH:'100(Mbs)',NETWORK_DELAY:'0(ms)',NETWORK_JITTER:'0.1(ms)',NETWORK_LOSS:'0(%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}
    #do socket func in here
     #tmpNode = {itemB.nodeName:tmp_cond[]}
    if tmp_cond.has_key(NETWORK_BANDWITH):           
        overallDic[NETWORK_BANDWITH][start.nodeName][end.nodeName] = tmp_cond[NETWORK_BANDWITH]
    else:
        overallDic[NETWORK_BANDWITH][start.nodeName][end.nodeName] = '*' #'0 (Mbs)'
        
    if tmp_cond.has_key(NETWORK_DELAY):           
        overallDic[NETWORK_DELAY][start.nodeName][end.nodeName] = tmp_cond[NETWORK_DELAY]
    else:
        overallDic[NETWORK_DELAY][start.nodeName][end.nodeName] = '*' #'0 (ms)'
        
    if tmp_cond.has_key(NETWORK_JITTER):           
        overallDic[NETWORK_JITTER][start.nodeName][end.nodeName] = tmp_cond[NETWORK_JITTER]
    else:
        overallDic[NETWORK_JITTER][start.nodeName][end.nodeName] = '*' #'0 (ms)'
        
        
    if tmp_cond.has_key(NETWORK_CONGESTION):           
        overallDic[NETWORK_CONGESTION][start.nodeName][end.nodeName] = tmp_cond[NETWORK_CONGESTION]
    else:
        overallDic[NETWORK_CONGESTION][start.nodeName][end.nodeName] = '*' #'NO'
    
    if tmp_cond.has_key(NETWORK_LOSS):           
        overallDic[NETWORK_LOSS][start.nodeName][end.nodeName] = tmp_cond[NETWORK_LOSS]
        #判断，如果丢包率过高，则认为网络当前拥塞
        #if tmp_cond[NETWORK_LOSS] >= TAG_CONGESTION:
        overallDic[NETWORK_CONGESTION][start.nodeName][end.nodeName] = isCongestion(tmp_cond[NETWORK_LOSS])
    else:
        overallDic[NETWORK_LOSS][start.nodeName][end.nodeName] = '*' #'0 (%)'
    
    if tmp_cond.has_key(NETWORK_AVAIL):           
        overallDic[NETWORK_AVAIL][start.nodeName][end.nodeName] = tmp_cond[NETWORK_AVAIL]
    else:
        overallDic[NETWORK_AVAIL][start.nodeName][end.nodeName] = 'NO'
    
    
    
    
    

    


#function:to get overall datas
def OverallAction(request):
    print 'OverallAction'
    #{NETWORK_BANDWITH:'100(Mbs)',NETWORK_DELAY:'0(ms)',NETWORK_JITTER:'0.1(ms)',NETWORK_LOSS:'0(%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}
    if request.method == "POST":
        tmp = request.POST
        #for i,j in tmp.items():
            #print i,j 
        protocol =  tmp['protocol']
        #print protocol
        allNodes = SchoolNode.objects.all() #to get all node infos in database

        #for itemA in allNodes:
        #    print itemA.nodeIp
        #overallDic format:
        #{"bandwidth":{nodeA(start):{nodeA(end):'',nodeB:'5Mbps',nodeC:'15Mbps'},nodeB:{nodeA:'10Mbps',nodeB:'',nodeC:'15Mbps'},nodeC:{nodeA:'10Mbps',nodeB:'5Mbps',nodeC:''}},
        #"delay":{nodeA:{nodeA:'',nodeB:'5ms',nodeC:'15ms'},nodeB:{nodeA:'10ms',nodeB:'',nodeC:'15ms'},nodeC:{nodeA:'10ms',nodeB:'5ms',nodeC:''}}}
        #do overall testing
        overallDic = {NETWORK_BANDWITH:{},NETWORK_DELAY:{},NETWORK_JITTER:{},NETWORK_LOSS:{},NETWORK_CONGESTION:{},NETWORK_AVAIL:{}} #define dic we need to return
        for itemA in allNodes:
            overallDic[NETWORK_BANDWITH][itemA.nodeName]={}
            overallDic[NETWORK_DELAY][itemA.nodeName]={}
            overallDic[NETWORK_JITTER][itemA.nodeName]={}
            overallDic[NETWORK_LOSS][itemA.nodeName]={}
            overallDic[NETWORK_CONGESTION][itemA.nodeName]={}
            overallDic[NETWORK_AVAIL][itemA.nodeName]={}
            for itemB in allNodes:
                #print 'nodeA:',itemA.nodeName,'nodeB:',itemB.nodeName
                overallDic[NETWORK_BANDWITH][itemA.nodeName][itemB.nodeName]='-'
                overallDic[NETWORK_DELAY][itemA.nodeName][itemB.nodeName]='-'
                overallDic[NETWORK_JITTER][itemA.nodeName][itemB.nodeName]='-'
                overallDic[NETWORK_LOSS][itemA.nodeName][itemB.nodeName]='-'
                overallDic[NETWORK_CONGESTION][itemA.nodeName][itemB.nodeName]='-'
                overallDic[NETWORK_AVAIL][itemA.nodeName][itemB.nodeName]='-'
                      
        #print overallDic
        print 'end for one'
        '''
        for start in allNodes:
            for end in allNodes:
                #print 'start:',start.nodeName,'end:',end.nodeName
                #if two different nodes
                if start.nodeName != end.nodeName:
                    tmp_cond = {NETWORK_BANDWITH:'100(Mbs)',NETWORK_DELAY:'0(ms)',NETWORK_JITTER:'0.1(ms)',NETWORK_LOSS:'0(%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}
                    #do socket func in here
                    #tmpNode = {itemB.nodeName:tmp_cond[]}
                    
                    overallDic[NETWORK_BANDWITH][start.nodeName][end.nodeName] = tmp_cond[NETWORK_BANDWITH]
                    overallDic[NETWORK_DELAY][start.nodeName][end.nodeName] = tmp_cond[NETWORK_DELAY]
                    overallDic[NETWORK_JITTER][start.nodeName][end.nodeName] = tmp_cond[NETWORK_JITTER]
                    overallDic[NETWORK_LOSS][start.nodeName][end.nodeName] = tmp_cond[NETWORK_LOSS]
                    overallDic[NETWORK_CONGESTION][start.nodeName][end.nodeName] = tmp_cond[NETWORK_CONGESTION]
                    overallDic[NETWORK_AVAIL][start.nodeName][end.nodeName] = tmp_cond[NETWORK_AVAIL]
        '''
        count = 0
        threads = []
        for start in allNodes:
            for end in allNodes:
                #print 'start:',start.nodeName,'end:',end.nodeName
                #if two different nodes
                st_IP = start.nodeIp
                ed_IP = end.nodeIp
                if start.nodeName != end.nodeName:
                    t = threading.Thread(target = MyThread,args = (protocol.upper(),st_IP,ed_IP,overallDic,start,end))#start thread to get node to node network infos
                    threads.append(t)
                    
        if protocol == 'TCP':          
            for t in threads:
                t.start()
                time.sleep(1.5)
                t.join()
        elif protocol == 'UDP':                       
            for t in threads:
                t.start()
                t.join()
        elif protocol == 'ICMP':
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        
        #print overallDic            
                    
        for i,j in request.POST.items():
            print i,j
         
        print 'end for two'
        return HttpResponse(json.dumps(overallDic), content_type="application/json")
        #return response so that .js in html will get success msg.Or it will fail
    
#uoloadAction
def UploadAction(request):
    #we prefer to use chunk to upload files
    print 'UploadAction'
    if request.method == "POST":
        print 'in ,request.method=post'
        #print str(request.FILES["uploadFile"])
        baseDir = os.path.dirname(os.path.dirname(__file__))
#         print baseDir
        file = request.FILES["uploadFile"]
        #print file.name.decode('utf-8')
        if file:
            
            filePath = baseDir+'/templates/upload/'+str(int(time.time()*1000))+'_'+str(file)
            #add timestamp to identify every file
            #print filePath,file.size
            with open (filePath,'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            os.system('rm -rf %s'%filePath) #delete file in web server when file uploading was finished
        else:
            pass
        #return HttpResponse({"liaohui":"hui"},content_type="text/javascript")
        return HttpResponse(json.dumps({'liao':'hui','hui':'liao'}), content_type="application/json")


#get paasive infos from database   
def PassiveAction(request):
    print 'PassiveAction'
    if request.method == "POST":
        print 'PassiveAction,if request.method == POST'
        tmp = request.POST  #get infos posted from passive.js which datatype=json
        #print tmp
        start_ip = tmp["startNodeIp"]
        end_ip = tmp["endNodeIp"]
        start_name = tmp["startNodeName"]
        end_name = tmp["endNodeName"]
        start_time = tmp["startTime"]
        end_time = tmp["endTime"]
        #print start_ip,start_name,start_time,end_ip,end_name,end_time
        
        #to judge if node was in db
        if SchoolNode.objects.filter(nodeName=start_name,nodeIp=start_ip).exists() and SchoolNode.objects.filter(nodeName=end_name,nodeIp=end_ip).exists():
            start_node = SchoolNode.objects.get(nodeName=start_name,nodeIp=start_ip)
            end_node = SchoolNode.objects.get(nodeName=end_name,nodeIp=end_ip)
            print 'start_node',start_node
            print 'end_node',end_node
            #get all infos from db where createTime between start_time and end_time
            msg = Passive.objects.filter(startNode=start_node,endNode=end_node,createTime__range=(start_time,end_time))
            if msg.exists():
                '''
                chart type:
                chartData = [{'name': '上海交通大学','data': [20, 21, 28.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 19.6]},
                     {'name': '华东师范大学','data': [5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]},
                     {'name': '复旦大学','data': [3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]},
                     {'name': '同济大学','data': [5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]}]
                '''
                bandwidth = {'name':'bandwidth','data':[]}
                throughput = {'name':'throughput','data':[]}
                loss = {'name':'loss','data':[]}
                rtt = {'name':'rtt','data':[]}
                cpu = {'name':'cpu','data':[]}
                memory = {'name':'memory','data':[]}
                createTime = []
                for item in msg:
                    print item.id,item.startNode,item.endNode,item.createTime
                    bandwidth['data'].append(item.bandwidth)
                    throughput['data'].append(item.throughput)
                    loss['data'].append(item.loss)
                    rtt['data'].append(item.rtt)
                    memory['data'].append(item.memory)
                    cpu['data'].append(item.cpu)
                    createTime.append(time.mktime(item.createTime.timetuple())) #change to timestamp:time.mktime(item.createTime.timetuple())
                    
                chartData = {'bandwidth':[bandwidth],'throughput':[throughput],'loss':[loss],'rtt':[rtt],'cpu':[cpu],'memory':[memory],'time':createTime}
                print chartData
                return HttpResponse(json.dumps(chartData), content_type="application/json")
            else:
                print 'passive objects not exists'
                
        else:
            print 'school node not exists'
'''           
def TracerouteAction(request):
    print 'TracerouteAction'
    if request.method == "POST":
        #print 'TracerouteAction,if request.method == POST '
        tmp = request.POST
        protocol =  tmp['protocol']
        st_IP = tmp['startNodeIp']
        end_IP = tmp['endNodeIp']
        st_name = tmp['startNodeName']
        ed_name = tmp['endNodeName']
        #print st_IP,end_IP
        traceMsg = Client(protocol.upper(),st_IP,end_IP); # to get network condition using action.Client.py
        ##call graphvizFunc to draw trace path
        print 'traceroute Msg:',traceMsg
        
        return HttpResponse(json.dumps(traceMsg), content_type="application/json")    
'''
def TracerouteAction(request):
    print 'TracerouteAction'
    if request.method == "POST":
        #print 'TracerouteAction,if request.method == POST '
        tmp = request.POST
        protocol =  tmp['protocol']
        st_IP = tmp['startNodeIp']
        end_IP = tmp['endNodeIp']
        st_name = tmp['startNodeName']
        ed_name = tmp['endNodeName']
        #print st_IP,end_IP
        #traceMsg = {}
        traceMsg = Client(protocol.upper(),st_IP,end_IP); # to get network condition using action.Client.py
        #print 'traceroute Msg:',traceMsg
        traceMsg["00 Start"] = st_name.encode("utf-8")
        traceMsg["End"] = ed_name.encode("utf-8") ##add startNode name and endNode name
        #print 'traceroute Msg:',traceMsg
        
        ##call graphvizFunc to draw trace path
        picUrl = "assets/netFile/graphviz/"
        baseDir = os.path.dirname(os.path.dirname(__file__))
        print 'baseDir:',baseDir
        filePath = baseDir+'/templates/'+picUrl
        name = graphvizFunc(traceMsg,filePath)

        return HttpResponse(json.dumps({"url":"assets/netFile/graphviz/"+name}), content_type="application/json")    