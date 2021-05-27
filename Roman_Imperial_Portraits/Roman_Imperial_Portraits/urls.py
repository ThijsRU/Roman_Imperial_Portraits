"""
Definition of urls for Roman_Imperial_Portraits.
"""

from django.conf.urls import include, url
from django.core.urlresolvers import reverse, reverse_lazy
import django.contrib.auth.views

from datetime import datetime

import ripdapp.views
import ripdapp.forms

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', Roman_Imperial_Portraits.views.home, name='home'),
    # url(r'^Roman_Imperial_Portraits/', include('Roman_Imperial_Portraits.Roman_Imperial_Portraits.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', ripdapp.views.index, name='index'),
    url(r'^home$', ripdapp.views.index, name='home'),

    url(r'^tools/update$', ripdapp.views.update_from_excel, name='tools_update'),

    # Allow signup, login and logout
    url(r'^signup/$', ripdapp.views.signup, name='signup'),
    url(r'^login/user/(?P<user_id>\w[\w\d_]+)$', ripdapp.views.login_as_user, name='login_as'),

    url(r'^nlogin', ripdapp.views.nlogin, name='nlogin'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'login.html',
            'authentication_form': ripdapp.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page':  reverse_lazy('home'),
        },
        name='logout'),


]
