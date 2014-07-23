from django.conf.urls import patterns, url

from manage_worksheets import views

urlpatterns = patterns('',
    url(r'^$', views.main, name='main'),
    url(r'^tags$', views.tags, name='tags'),
    url(r'^worksheet_details/(?P<worksheet_id>.*)$',
        views.worksheet_details, name='worksheet_details'),
    url(r'^worksheet_list$',
        views.worksheet_list, name='worksheet_list'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^takedata$', views.takedata, name='takedata'),
    url(r'^u/(?P<worksheet_id>.*)$', views.details, name='details'),
    )
