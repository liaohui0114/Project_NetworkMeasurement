# *-* coding:utf-8 *-*
from django.conf.urls import patterns, include, url
from django.contrib import admin
#liaohui
from django.conf import settings 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#liaohui
extrapatterns = patterns('',
    url(r'udp/$','networkmeasurement.views.udpFunc'),
    url(r'upload/$','networkmeasurement.views.UploadFunc'), 
    url(r'download/$','networkmeasurement.views.DownloadFunc'),
)
###################

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoTest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'assets/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),#liaohui,it's ok,why?
    #url(r'/assets/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    #liaohui,it can not find resouces like:css etc if we change / to ^
    url(r'^admin/', include(admin.site.urls)),
    url(r'^udp/$','networkmeasurement.views.udpFunc'),
    url(r'^upload/$','networkmeasurement.views.UploadFunc'),
    url(r'^download/$','networkmeasurement.views.DownloadFunc'),
    
    url(r'^(udp)|(upload)|(download)/',include(extrapatterns)),
    #include：think about this ,urls in extrapatterns will follow ^udp/,like:^udp/upload/$,udp/download/$
    url(r'^test/$','networkmeasurement.views.testFunc'),
    url(r'test/operateDB','networkmeasurement.views.operateDB'),
    #action following
    url(r'protocol/jsonAction','networkmeasurement.action.JsonAction.JsonAction'),  #ajax json from page
    url(r'action/uploadAction','networkmeasurement.action.JsonAction.UploadAction'),  #uploadAction
    
    
    
    ##########test###############url可以传递参数#########
    url(r'other/([a-zA-z0-9]+\.html)','networkmeasurement.views.OtherHyperLink'),
    #用()括起来的可被当成参数传入相应的方法如([a-zA-z0-9]+\.html)：,也可以给参数添加名字如(?P<name>xxx),见下一个规则
    url(r'other/(?P<targetHtml>www\.[a-zA-z0-9]*\.com(\.cn)?)','networkmeasurement.views.OtherHyperLink'),
    #style:(?P<paramName>msg),so we can use name:paramName to get msg in view
    #(?<name>exp)    匹配exp,并捕获文本到名称为name的组里，也可以写成(?'name'exp),def my_view(request, name):
)


#urlpatterns += staticfiles_urlpatterns() #liaohui