# -*- coding:utf-8 -*- 

from django.http import HttpResponse
from django.shortcuts import render_to_response
import json,os
from  GlobleVariable import *
from Client import *

#DEFAULT SETTING
DEFAULT_UDP_COND = {NETWORK_BANDWITH:'100(Mbs)',NETWORK_DELAY:'0(ms)',NETWORK_JITTER:'0.1(ms)',NETWORK_LOSS:'0(%)',NETWORK_CONGESTION:'NO',NETWORK_AVAIL:'YES'}

def JsonAction(request):
    print 'liaohui,JsonAction'
    if request.method == "POST":
        tmp = request.POST
        for i,j in tmp.items():
            print i,j  #print msg from front page
#         netMsg = Client();
#         for key,value in netMsg.items():
#             DEFAULT_UDP_COND[key] = value #set true attribute
#         print DEFAULT_UDP_COND
        
        return HttpResponse(json.dumps({"single":DEFAULT_UDP_COND}), content_type="application/json")

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