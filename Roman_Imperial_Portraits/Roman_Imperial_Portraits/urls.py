"""
Definition of urls for Roman_Imperial_Portraits.
"""

from django.conf.urls import include, url
import ripdapp.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', Roman_Imperial_Portraits.views.home, name='home'),
    # url(r'^Roman_Imperial_Portraits/', include('Roman_Imperial_Portraits.Roman_Imperial_Portraits.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', ripdapp.views.index, name='index'),
    url(r'^home$', ripdapp.views.index, name='home'),
    url(r'^about$', ripdapp.views.about, name='about'),
    url(r'^welcome$', ripdapp.views.welcome, name='welcome'),
    url(r'^browse$', ripdapp.views.browse, name='browse'),
    url(r'^advsearch$', ripdapp.views.advsearch, name='advsearch'),
    url(r'^reflinks$', ripdapp.views.reflinks, name='reflinks'),
   #url(r'^record$', ripdapp.views.record, name='record')
]
