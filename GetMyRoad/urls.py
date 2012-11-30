from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.views import home, logout, find_places

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('social_auth.urls')),
    url(r'', include('core.urls')),
    url(r'^$', home, name="home"),
    url(r'^find-places/$', find_places, name="find-places"),
    url(r'^logout/$', logout, name='logout'),
)
