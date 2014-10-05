from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'poak.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^poak/admin/', include(admin.site.urls)),
    url(r'^poak/u/', include('users.urls', namespace='users')),
    url(r'^poak/', include('manage_worksheets.urls', namespace='manage_worksheets')),
    url(r'^poak/blog/comments/', include('fluent_comments.urls')),
)
