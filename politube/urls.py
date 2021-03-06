from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import politube.views

urlpatterns = patterns('',
    url(r'^$', politube.views.home, name='home'),
    url(r'^about/', politube.views.about, name='about'),
    url(r'^plenary/', include('plenary.urls')),
    url(r'^deputy/', include('deputy.urls')),
    url(r'^videos_tools/', include('videos_tools.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
