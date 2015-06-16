# -*- coding:utf-8 -*- 

from django.http import HttpResponse
from django.shortcuts import render_to_response
import json,os,datetime
from  GlobleVariable import *
from Client import *
from networkmeasurement.models import SchoolNode,Passive
from time import sleep

#DEFAULT SETTING
DEFAULT_UDP_COND = {NETWORK_BANDWITH:'100(Mbs)',NETWORK_DELAY:'0(ms)',NETWORK_JITTER:'0.1(ms)',NETWORK_LOSS:'0(%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}
DEFAULT_OVERALL_COND = {NETWORK_BANDWITH:'',NETWORK_DELAY:'',NETWORK_JITTER:'',NETWORK_LOSS:'',NETWORK_CONGESTION:'',NETWORK_AVAIL:''}


#function:to get point to point network cond
def SingleAction(request):
    print 'SingleAction'
    if request.method == "POST":
        print 'SingleAction,if request.method == POST '
        tmp = request.POST
        print tmp
        ##在apache部署后需要注释下面两行才能继续执行，在/var/log/apache2/error.log只打印一行就卡住了？？？？下面的一些在for循环中的print也是，注释后才能正常执行
        #for i,j in tmp.items():
        #    print i,j  #print msg from front page
#         netMsg = Client();
#         for key,value in netMsg.items():
#             DEFAULT_UDP_COND[key] = value #set true attribute
#         print DEFAULT_UDP_COND
        print 'chartData'
        chartData = [{'name': '上海交通大学','data': [20, 21, 28.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 19.6]},
                     {'name': '华东师范大学','data': [5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]},
                     {'name': '复旦大学','data': [3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]},
                     {'name': '同济大学','data': [5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]}]
        chartTime = [1,2,3,4,5,6,7,8,9,10]
        print chartData
        reMsg = {"single":DEFAULT_UDP_COND,"chart":{"chartData":chartData,"chartTime":chartTime}}   #we will decode this format by .js
        sleep(4) #for test
        return HttpResponse(json.dumps(reMsg), content_type="application/json")
    print 'end SingleAction'
#function:to get overall datas
def OverallAction(request):
    print 'OverallAction'
    #{NETWORK_BANDWITH:'100(Mbs)',NETWORK_DELAY:'0(ms)',NETWORK_JITTER:'0.1(ms)',NETWORK_LOSS:'0(%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}
    if request.method == "POST":
        print 'OverallAction,if'
        allNodes = SchoolNode.objects.all() #to get all node infos in database
        
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
                overallDic[NETWORK_BANDWITH][itemA.nodeName][itemB.nodeName]=''
                overallDic[NETWORK_DELAY][itemA.nodeName][itemB.nodeName]=''
                overallDic[NETWORK_JITTER][itemA.nodeName][itemB.nodeName]=''
                overallDic[NETWORK_LOSS][itemA.nodeName][itemB.nodeName]=''
                overallDic[NETWORK_CONGESTION][itemA.nodeName][itemB.nodeName]=''
                overallDic[NETWORK_AVAIL][itemA.nodeName][itemB.nodeName]=''
                      
        print overallDic
        print 'end for one'
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
        
        print overallDic
        print 'end for two'            
                    
        for i,j in request.POST.items():
            print i,j
         
        return HttpResponse(json.dumps(overallDic), content_type="application/json")
        #return response so that .js in html will get success msg.Or it will fail
    
#uoloadAction
def UploadAction(request):
    #we prefer to use chunk to upload files
    print 'UploadAction'
    if request.method == "POST":
#         print str(request.FILES["uploadFile"])
        baseDir = os.path.dirname(os.path.dirname(__file__))
#         print baseDir
        file = request.FILES["uploadFile"]
        print file.name
        if file:
            filePath = baseDir+'/templates/upload/'+str(file)
            print filePath
            print file.size
            with open (filePath,'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
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
                    
                rtnMsg = {'bandwidth':[bandwidth],'throughput':[throughput],'loss':[loss],'rtt':[rtt],'cpu':[cpu],'memory':[memory],'time':createTime}
                print rtnMsg
                return HttpResponse(json.dumps(rtnMsg), content_type="application/json")
            else:
                print 'passive objects not exists'
                
        else:
            print 'school node not exists'
            
        
