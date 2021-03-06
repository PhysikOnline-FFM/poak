from django.conf.urls import patterns, url

from manage_worksheets import views, ajax

urlpatterns = patterns('',
    # html pages
    url(r'^$', views.main, name='main'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^sso/submit/(?P<worksheet_id>.*)$', views.sso_submit, name='sso_submit'),
    url(r'^w/(?P<worksheet_pk>\d+)/login$', views.loggedin_details, name='loggedin_details'),
    url(r'^w/(?P<worksheet_pk>\d+)/delete$', views.delete, name='delete'),
    url(r'^w/(?P<worksheet_pk>\d+)/tags$', views.choose_tags, name='choose_tags'),
    url(r'^w/(?P<worksheet_pk>\d*)$', views.details, name='details'),

    # redirect
    url(r'^pokalid/(?P<worksheet_id>.*)$', views.redirect_from_pid),

    # ajax functions
    url(r'^tags$', ajax.tags, name='tags'),
    url(r'^worksheet_details/(?P<worksheet_pk>\d+)$', ajax.worksheet_details, name='worksheet_details'),
    url(r'^worksheet_list$', ajax.worksheet_list, name='worksheet_list'),
    url(r'^worksheets_for_tag/(?P<tag_id>\d+)', ajax.worksheets_for_tag, name='worksheets_for_tag'),
    url(r'^minus_tag/(?P<tag_id>\d+)', ajax.minus_tag, name='minus_tag'),
    url(r'^sso/move/(?P<from_id>\w+?)/(?P<to_id>\w+)', ajax.move, name='move'),
    url(r'^check/(?P<worksheet_id>\w+)$', ajax.check_wsid, name='check_wsid'),
)
