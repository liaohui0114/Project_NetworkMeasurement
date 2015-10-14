# -*- coding: utf-8 -*- 
from django.shortcuts import render, render_to_response
from django.template import loader,Context
from django.http import HttpResponse,HttpResponseRedirect
#from networkmeasurement import models
import os
import MySQLdb
import json
import networkmeasurement.action.MySqlOperation
from networkmeasurement.action.MySqlOperation import TableSchoolNode
from networkmeasurement.action import FormModule
import time,datetime
from django.utils.timezone import utc
from models import *
import base64,hashlib
# Create your views here.

VALIDATE_KEY = '28cce32073c56f138d8c328e5ccdf3728fd248d7'
VALIDATE_URL = 'https://sjtusp.ecnu.edu.cn/secure'
def IsValid(msg,dateInfo):
    hashfun = hashlib.md5()
    value = VALIDATE_KEY+dateInfo
    hashfun.update(value)
    if hashfun.hexdigest()==msg:
        print 'Isvalid,true:',msg
        return True
    else:
        print 'IsValid,false'
        return False

#function:to judge if the user have login already.If we can get the cookies which imply we have login
def IsLogin(request):
    print 'view:IsLogin'
    username = request.COOKIES.get('username') #TO GET THE COOKIES
    if username:
        print ' login'
        return True
    else:
        print 'not login'
        return False
def IndexFunc(request):
    return render_to_response("index.html",{})

def LoginFunc(request):
    print 'view:LoginFunc'
    if IsLogin(request):
        return HttpResponseRedirect("/tcp/")  #if user have login already,then redirect to passive.html
    else:
        if request.method == 'POST':
            form = FormModule.LoginForm(request.POST)
            if form.is_valid():                
                username = form.cleaned_data["username"]
                passwd = form.cleaned_data["passwd"]
                print username,passwd
                # operation
                if username=="liaohui" and passwd=="liaohui":
                     #set cookies,use HttpResponse instance
                     response =  HttpResponseRedirect('/tcp/')                
                     response.set_cookie('username', username, 3600)  #set cookie imply that we have login
                     return response
                else:
                     return HttpResponse("Wrong id or password,<a href='/login/'>login</login>")
        else:
            form = FormModule.LoginForm()  #only call once??
        return render_to_response("login.html",{"form":form})
    
def LogoutFunc(request):
    response = HttpResponse("You have already logout,<a href=%s>Login</a>"%(VALIDATE_URL))
    if request.COOKIES.get('username'):
        response.delete_cookie('username') #user HttpResponse instance to delete cookies
    return response       
    
def UDPFunc(request):
    print 'view:udpFunc'
    if IsLogin(request):
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
    else:
        #return HttpResponse("Please login first,<a href='/login/'>Login</a>")
        return HttpResponseRedirect(VALIDATE_URL)
    
def UploadFunc(request):
    print 'view.Uploadfunc'
    if IsLogin(request):
        t = Context({'liao':'liao'})
        return render_to_response("updown-upload.html",t)
    else:
        #return HttpResponse("Please login first,<a href='/login/'>Login</a>")
        return HttpResponseRedirect(VALIDATE_URL)

def DownloadFunc(request):
    if IsLogin(request):
        t = Context({'liao':'liao'})
        return render_to_response("updown-download.html",t)
    else:
        #return HttpResponse("Please login first,<a href='/login/'>Login</a>")
        return HttpResponseRedirect(VALIDATE_URL)

def PassiveFunc(request):
    print 'view:PassiveFunc'
#     t = Context({'liao':'liao'})
#     return render_to_response("active-udp.html",t)
    if IsLogin(request):
        if request.method == 'POST':
                print 'liaohui,get post from json'
                form = FormModule.PassiveForm(request.POST)
                if form.is_valid():                
                    print "liaohui,isvalid",form
                    return HttpResponse(json.dumps({"LIAOHUI":"LIAOHUI"}), content_type="application/json")
        else:
            form = FormModule.PassiveForm()  #only call once??
        
        return render_to_response("passive.html",{'form':form})
    else:
        #return HttpResponse("Please login first,<a href='/login/'>Login</a>")
        return HttpResponseRedirect(VALIDATE_URL)

def PredictFunc(request):
    print 'view:PassiveFunc'
#     t = Context({'liao':'liao'})
#     return render_to_response("active-udp.html",t)
    if IsLogin(request):
        if request.method == 'POST':
                form = FormModule.PassiveForm(request.POST)
                if form.is_valid():                
                    #print "liaohui,isvalid",form
                    return HttpResponse(json.dumps({"LIAOHUI":"LIAOHUI"}), content_type="application/json")
        else:
            form = FormModule.PassiveForm()  #only call once??
        
        return render_to_response("predict.html",{'form':form})
    else:
        #return HttpResponse("Please login first,<a href='/login/'>Login</a>")
        return HttpResponseRedirect(VALIDATE_URL)        
        
def testFunc(request):
    #tmp = models.Passive(bandwidth=2048,throughput=12,rtt=10,loss=0,cpu=52.3,memory=256,endNode_id=2,startNode_id=3)
    #print datetime.datetime.fromtimestamp(time.time())
    #tmp.save()
#      tb = TableSchoolNode('192.168.1.152','上海交通大学')
#      tb.InsertNode()
#     t = Context({'liao':'liao'})
#     return render_to_response("jqueyTest.html",t)

    #get() return on line ,filter return one or more lindes
    #__gte >=,__lte:<=
    #__startswidth:like "xxx%"
    #__range=(a,b),between a and b
    
    if NetProtocol.objects.filter(protocolName='TCP'):
        pt = NetProtocol.objects.get(protocolName='TCP')
        print 'pt exists'
    else:
        print 'pt not exists'
    #print pt.id,pt.protocolName
    
    ps = Active.objects.filter(protocol=pt)
    if ps.exists():
        print "exits"
        for item in ps:
            print item.createTime,item.startNode,item.endNode
    else:
        print 'not exits'
    
    
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
	
def TcpFunc(request):
    print 'view:tcpFunc'
#     t = Context({'liao':'liao'})
#     return render_to_response("active-udp.html",t)
    if IsLogin(request):
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
            print 'view:tcpFunc,else!'
            form = FormModule.UDPForm()  #only call once??
            print 'view:tcpFunc,else end!'
            
        return render_to_response("active-tcp.html",{'form':form})
    else:
        #return HttpResponse("Please login first,<a href='/login/'>Login</a>")
        return HttpResponseRedirect(VALIDATE_URL)

def IcmpFunc(request):
    print 'view:icmpFunc'
#     t = Context({'liao':'liao'})
#     return render_to_response("active-udp.html",t)
    if IsLogin(request):
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
            print 'view:icmpFunc,else!'
            form = FormModule.UDPForm()  #only call once??
            print 'view:icmpFunc,else end!'
            
        return render_to_response("active-icmp.html",{'form':form})
    else:
        #return HttpResponse("Please login first,<a href='/login/'>Login</a>")
        return HttpResponseRedirect(VALIDATE_URL)

def ValidateUrlFunc(request):
    print 'ValidateUrlFunc'
    if IsLogin(request):
        return HttpResponseRedirect('/tcp/')
    else:
        #third part validation:when we have login,the server will return url by get method like:
        #http://202.121.178.195/?uid=bGlhb2h1aQ==&cn=5buW6L6J&domainName=c2p0dS5lZHUuY24=&typeOf=5a2m55SfO3N0dWRlbnQ=&eduPersonStudentID=&employeeNumber=&msg=f71ea8f78b17ef31905e49c0310b1be6&date=2015-07-24|12:10:04
        # to identify if the following params were existed in urls by GET method
        urlIdentifier = ['uid','cn','domainName','typeOf','eduPersonStudentID','employeeNumber','msg','date']
        #to store data from url,default value:''
        dictIdentifier = {'uid':'','cn':'','domainName':'','typeOf':'','eduPersonStudentID':'','employeeNumber':'','msg':'','date':''}
        isValidate = True #to judge if the url contains the whole identifier like:uid,cn,domainName...
        if request.method == 'GET':
            for item in urlIdentifier:
                if request.GET.__contains__(item):                
                    
                    if item=='msg' or item=='date':
                        dictIdentifier[item] = request.GET.get(item)  #store infos
                    else:    
                        dictIdentifier[item] = base64.decodestring(request.GET.get(item)) #use base64 to decode excepte msg and date
                        #print dictIdentifier[item]
                else:
                    #print item+' does exists'
                    isValidate = False
            print 'dictIdentifier:',dictIdentifier       
            if isValidate and IsValid(dictIdentifier['msg'],dictIdentifier['date']):
                #set cookies,use HttpResponse instance
                response =  HttpResponseRedirect('/tcp/')                
                response.set_cookie('username', dictIdentifier["uid"], 3600)  #set cookie imply that we have login
                return response
            else:
                return HttpResponseRedirect(VALIDATE_URL)