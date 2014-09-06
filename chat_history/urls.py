from django.conf.urls import patterns, url
from chat_history import views

urlpatterns = patterns('',
    url(r'^getlog/(?P<worksheet>.*)$', views.getlog, name="getlog"),
    )
