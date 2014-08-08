from django.conf.urls import patterns, url

from manage_worksheets import views, ajax

urlpatterns = patterns('',

    # html pages
    url(r'^$', views.main, name='main'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^w/(?P<worksheet_id>.*)$', views.details, name='details'),

    # ajax functions
    url(r'^tags$', ajax.tags, name='tags'),
    url(r'^worksheet_details/(?P<worksheet_id>.*)$',
        ajax.worksheet_details, name='worksheet_details'),
    url(r'^worksheet_list$',
        ajax.worksheet_list, name='worksheet_list'),
    url(r'^worksheets_for_tag/(?P<tag_id>\d+)', ajax.worksheets_for_tag,
        name='worksheets_for_tag'),
    )
