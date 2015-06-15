# -*- coding: utf-8 -*- 
from django.shortcuts import render, render_to_response
from django.template import loader,Context
from django.http import HttpResponse,HttpResponseRedirect
from networkmeasurement import models
import os
import MySQLdb
import json
import networkmeasurement.action.MySqlOperation
from networkmeasurement.action.MySqlOperation import TableSchoolNode
from networkmeasurement.action import FormModule
import time,datetime
from django.utils.timezone import utc
# Create your views here.

    
def UDPFunc(request):
    print 'view:udpFunc'
#     t = Context({'liao':'liao'})
#     return render_to_response("active-udp.html",t)
    if request.method == 'POST':
            print 'liaohui,get post from json'
            form = FormModule.UDPForm(request.POST)
            if form.is_valid():                
                print "liaohui,isvalid",form
                return HttpResponse(json.dumps({"LIAOHUI":"LIAOHUI"}), content_type="application/json")
                #username = uf.cleaned_data["username"]
                #passwd = uf.cleaned_data["passwd"]
                #print username,passwd
                #b operation
    #             user = User.objects.filter(username__exact=username,password__exact=passwd) #to judge if there exist same username in db
    #             if user:
    #                 #set cookies,use HttpResponse instance
    #                 response =  HttpResponseRedirect('/index/')                
    #                 response.set_cookie('username', username, 3600)
    #                 return response
    #             else:
    #                 return HttpResponseRedirect('/login/')
    else:
        #print 'view:udpFunc,else!'
        form = FormModule.UDPForm()  #only call once??
        #print 'view:udpFunc,else end!'
        
    return render_to_response("active-udp.html",{'form':form})   
    
def UploadFunc(request):
    print 'view.Uploadfunc'
    t = Context({'liao':'liao'})
    return render_to_response("updown-upload.html",t)
def DownloadFunc(request):
    t = Context({'liao':'liao'})
    return render_to_response("updown-download.html",t)

def PassiveFunc(request):
    print 'view:PassiveFunc'
#     t = Context({'liao':'liao'})
#     return render_to_response("active-udp.html",t)
    if request.method == 'POST':
            print 'liaohui,get post from json'
            form = FormModule.PassiveForm(request.POST)
            if form.is_valid():                
                print "liaohui,isvalid",form
                return HttpResponse(json.dumps({"LIAOHUI":"LIAOHUI"}), content_type="application/json")
                #username = uf.cleaned_data["username"]
                #passwd = uf.cleaned_data["passwd"]
                #print username,passwd
                #b operation
    #             user = User.objects.filter(username__exact=username,password__exact=passwd) #to judge if there exist same username in db
    #             if user:
    #                 #set cookies,use HttpResponse instance
    #                 response =  HttpResponseRedirect('/index/')                
    #                 response.set_cookie('username', username, 3600)
    #                 return response
    #             else:
    #                 return HttpResponseRedirect('/login/')
    else:
        form = FormModule.PassiveForm()  #only call once??
    return render_to_response("passive.html",{'form':form})
    print 'view:PassiveFunc end!'
        
        
def testFunc(request):
    #tmp = models.Passive(bandwidth=2048,throughput=12,rtt=10,loss=0,cpu=52.3,memory=256,endNode_id=2,startNode_id=3)
    #print datetime.datetime.fromtimestamp(time.time())
    #tmp.save()
#      tb = TableSchoolNode('192.168.1.152','上海交通大学')
#      tb.InsertNode()
#     t = Context({'liao':'liao'})
#     return render_to_response("jqueyTest.html",t)
    if request.method == 'POST':
        form = FormModule.UDPForm(request.POST)
        if form.is_valid():
            pass
            #username = uf.cleaned_data["username"]
            #passwd = uf.cleaned_data["passwd"]
            #print username,passwd
            #b operation
#             user = User.objects.filter(username__exact=username,password__exact=passwd) #to judge if there exist same username in db
#             if user:
#                 #set cookies,use HttpResponse instance
#                 response =  HttpResponseRedirect('/index/')                
#                 response.set_cookie('username', username, 3600)
#                 return response
#             else:
#                 return HttpResponseRedirect('/login/')
    else:
        form = FormModule.UDPForm()
    #return render_to_response("jqueyTest.html",{'form':form}) 
    return render_to_response("test.html",{'form':form})      

def operateDB(request):
    print "liaohui,operateDB()"
    response_data = []  
    try:
        conn= MySQLdb.connect(
                host='localhost',
                port = 3306,
                user='root',
                passwd='root',
                db ='liaohui',
                )
        cur = conn.cursor()
        cur.execute('select * from user')
        
        results = cur.fetchall()
        for id,name in results:
            print id,name
            tmp={}
            tmp["id"] = id
            tmp["name"] = name
            response_data.append(tmp)
            
        print response_data
        print json.dumps(response_data)
              
        conn.commit()
        cur.close()
        conn.close()
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    except MySQLdb.Error,e:
        print 'Mysql Error %d:%s'%(e.args[0],e.args[1])
        
def OtherHyperLink(request,targetHtml):
    print targetHtml
    return HttpResponseRedirect("http://www.baidu.com")
        