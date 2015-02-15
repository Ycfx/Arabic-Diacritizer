from django.conf.urls import patterns, include, url
from django.contrib import admin
from tashkeel import views

urlpatterns = patterns('',
    url(r'^$', views.index),              
    url(r'^tashkeel_v1/$', views.tashkeel_v1),
    url(r'^tashkeel_v2/$', views.tashkeel_v2),
    url(r'^evaluate/$', views.Evaluate),
    url(r'^tashkeelandevaluate/$', views.TashkeelAndEvaluate),
    url(r'^deletediac/$', views.DeletDiac),
    url(r'^gettestsents/$', views.GetTestSents),
    url(r'^getdict/$', views.getdict),
)
