"""
Definition of urls for Roman_Imperial_Portraits.
"""

from django.conf.urls import include, url
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import admin
import django.contrib.auth.views

from django.conf import settings # for showing pictures in Browse
from django.conf.urls.static import static # for showing pictures in Browse

from django.views.generic.base import RedirectView

from datetime import datetime

# Imports from the RIPD app
import ripdapp.views
import ripdapp.viewsbasic
import ripdapp.forms

from ripdapp.viewsbasic import *

# Non-standard settings
pfx = ""

admin.autodiscover()

# Set admin stie information
admin.site.site_header = "Roman Imperial Portraits Database"
admin.site.site_title = "ripd Admin"

urlpatterns = [
    # Standard pages
    url(r'^$', ripdapp.views.index, name='index'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/ripdapp/content/favicon.ico')),
    url(r'^home$', ripdapp.views.index, name='home'),

    url(r'^tools/update$', ripdapp.views.update_from_excel, name='tools_update'),

    url(r'^portrait/list', PortraitListView.as_view(), name='portrait_list'),
    url(r'^portrait/details(?:/(?P<pk>\d+))?/$', PortraitDetails.as_view(), name='portrait_details'),
    url(r'^portrait/edit(?:/(?P<pk>\d+))?/$', PortraitEdit.as_view(), name='portrait_edit'),

    # Definitions are kind of separate
    url(r'^definitions$', RedirectView.as_view(url='/'+pfx+'admin/'), name='definitions'),

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

    # Enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls), name='admin_base'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # for showing pictures in Browse
