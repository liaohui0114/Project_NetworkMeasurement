# *-* coding:utf-8 *-*
from django.conf.urls import patterns, include, url
from django.contrib import admin
#liaohui
from django.conf import settings 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#liaohui
extrapatterns = patterns('',
    url(r'udp/$','networkmeasurement.views.UDPFunc'),
    url(r'tcp/$','networkmeasurement.views.TcpFunc'),
    url(r'icmp/$','networkmeasurement.views.IcmpFunc'),
    url(r'passive/$','networkmeasurement.views.PassiveFunc'),
    url(r'upload/$','networkmeasurement.views.UploadFunc'), 
    url(r'download/$','networkmeasurement.views.DownloadFunc'),
    url(r'passive/$','networkmeasurement.views.PassiveFunc'),
)
###################

urlpatterns = patterns('',
    # Examples:
    url(r'^$','networkmeasurement.views.ValidateUrlFunc'),#init html,index.html
    # url(r'^blog/', include('blog.urls')),
    url(r'assets/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),#liaohui,it's ok,why?
    #url(r'/assets/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    #liaohui,it can not find resouces like:css etc if we change / to ^
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$','networkmeasurement.views.IndexFunc'),
    url(r'^udp/$','networkmeasurement.views.UDPFunc'),
	url(r'^tcp/$','networkmeasurement.views.TcpFunc'),
	url(r'^icmp/$','networkmeasurement.views.IcmpFunc'),
	url(r'^passive/$','networkmeasurement.views.PassiveFunc'),
    url(r'^upload/$','networkmeasurement.views.UploadFunc'),
    url(r'^download/$','networkmeasurement.views.DownloadFunc'),
    url(r'^passive/$','networkmeasurement.views.PassiveFunc'),
    url(r'^predict/$','networkmeasurement.views.PredictFunc'),
    url(r'^login/$','networkmeasurement.views.LoginFunc'),
    url(r'^logout/$','networkmeasurement.views.LogoutFunc'),
    
    url(r'^(udp)|(upload)|(download)|(tcp)|(icmp)|(passive)/',include(extrapatterns)),
    #include：think about this ,urls in extrapatterns will follow ^udp/,like:^udp/upload/$,udp/download/$
    #url(r'^test/$','networkmeasurement.views.testFunc'),
    #url(r'test/operateDB','networkmeasurement.views.operateDB'),
    #action following
    url(r'action/SingleAction','networkmeasurement.action.JsonAction.SingleAction'),  #ajax json from page to test point to point network condition
    url(r'action/UploadAction','networkmeasurement.action.JsonAction.UploadAction'),  #uploadAction
    url(r'action/OverallAction','networkmeasurement.action.JsonAction.OverallAction'),  #overallAction
    url(r'action/PassiveAction','networkmeasurement.action.JsonAction.PassiveAction'),  #PassiveAction 
    url(r'action/TracerouteAction','networkmeasurement.action.JsonAction.TracerouteAction'),  #PassiveAction
    
    
    
    ##########test###############url可以传递参数#########
    #url(r'^other/\?id=([a-zA-z0-9]+\.html)','networkmeasurement.views.OtherHyperLink'),
    #用()括起来的可被当成参数传入相应的方法如([a-zA-z0-9]+\.html)：,也可以给参数添加名字如(?P<name>xxx),见下一个规则
    #url(r'^other/(?P<targetHtml>www\.[a-zA-z0-9]*\.com(\.cn)?)','networkmeasurement.views.OtherHyperLink'),
    #style:(?P<paramName>msg),so we can use name:paramName to get msg in view
    #(?<name>exp)    匹配exp,并捕获文本到名称为name的组里，也可以写成(?'name'exp),def my_view(request, name):
    #url(r'test/\?uid=(?P<uid>.*)&cn=(?P<cn>.*)&domainName=(?P<domainName>.*)&typeOf=(?P<typeOf>.*)&eduPersonStudentID=(?<eduPersonStudentID>.*)&employeeNumber=(?P<employeeNumber>.*)&msg=(?P<msg>.*)&date=(?P<date>.*)','networkmeasurement.views.IdentifyFunc'),
    #url(r'urltest/$','networkmeasurement.views.ValidateUrlFunc'),
)


#urlpatterns += staticfiles_urlpatterns() #liaohui