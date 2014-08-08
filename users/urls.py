from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name="my_login"),
    url(r'^account/$', views.account, name="account"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}, name="my_logout")
    )
