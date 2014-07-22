from django.conf.urls import patterns, url

from manage_worksheets import views

urlpatterns = patterns('',
                url(r'^$', views.main, name='main'),
                url(r'^tags$', views.tags, name='tags'),
                )
