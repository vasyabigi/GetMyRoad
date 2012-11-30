from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.views import home, logout, find_places, build_road

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('social_auth.urls')),
    url(r'', include('core.urls')),
    url(r'^$', home, name="home"),
    url(r'^find-places/$', find_places, name="find-places"),
    url(r'^select-categories/$', find_places, name="select-categories"),
    url(r'^build-road/$', build_road, name="build-road"),
    url(r'^logout/$', logout, name='logout'),
)
