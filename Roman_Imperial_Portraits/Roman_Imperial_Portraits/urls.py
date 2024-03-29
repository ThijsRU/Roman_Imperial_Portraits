"""
Definition of urls for Roman_Imperial_Portraits.
"""
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import include, url
from django.urls import reverse, reverse_lazy
from django.contrib import admin
import django.contrib.auth.views

from django.views.decorators.csrf import csrf_exempt

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
    url(r'^$', ripdapp.views.about, name='about'), # about ipv index.html
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/ripdapp/content/favicon.ico')),
    url(r'^home$', ripdapp.views.about, name='home'), # home twee keer
    url(r'^about$', ripdapp.views.about, name='home'),
    url(r'^references$', ripdapp.views.references, name='references'),
    url(r'^links$', ripdapp.views.links, name='links'),    
    url(r'^tools/update$', ripdapp.views.update_from_excel, name='tools_update'),
    url(r'^tools/update_photofolders$', ripdapp.views.update_from_excel_photofolder, name='tools_update_photofolder'),
    url(r'^tools/update_coordinates$', ripdapp.views.update_from_excel_coordinates, name='tools_update_coordinates'), 
    url(r'^tools/update_currlocs$', ripdapp.views.update_cur_loc_coord_excel, name='tools_update_cur_loc_coord_excel'), 
    url(r'^tools/update_table1$', ripdapp.views.update_from_excel_table1, name='tools_update_table1'),  
    url(r'^tools/update_table2$', ripdapp.views.update_from_excel_table2, name='tools_update_table2'),   
    url(r'^tools/update_table3$', ripdapp.views.update_from_excel_table3, name='tools_update_table3'),

    url(r'^portrait/list', PortraitListView.as_view(), name='portrait_list'),
    url(r'^portrait/details(?:/(?P<pk>\d+))?/$', PortraitDetails.as_view(), name='portrait_details'),
    url(r'^portrait/edit(?:/(?P<pk>\d+))?/$', PortraitEdit.as_view(), name='portrait_edit'),

    url(r'^portrait/map/', csrf_exempt(PortraitMapView.as_view()), name='portrait_map'),

    url(r'^photographer/list', PhotographerListView.as_view(), name='photographer_list'),
    url(r'^photographer/details(?:/(?P<pk>\d+))?/$', PhotographerDetails.as_view(), name='photographer_details'),
    url(r'^photographer/edit(?:/(?P<pk>\d+))?/$', PhotographerEdit.as_view(), name='photographer_edit'),

    url(r'^photopath/list', PhotoPathListView.as_view(), name='path_list'),
    url(r'^photopath/details(?:/(?P<pk>\d+))?/$', PhotoPathDetails.as_view(), name='path_details'),
    url(r'^photopath/edit(?:/(?P<pk>\d+))?/$', PhotoPathEdit.as_view(), name='path_edit'),
    url(r'^photo/add/details(?:/(?P<pk>\d+))?/$', AddPhotoDetails.as_view(), name='addphoto_details'),
    url(r'^photo/add/edit(?:/(?P<pk>\d+))?/$', AddPhotoEdit.as_view(), name='addphoto_edit'),

    

    # Definitions are kind of separate
    url(r'^definitions$', RedirectView.as_view(url='/'+pfx+'admin/'), name='definitions'),

    # Allow signup, login and logout
    url(r'^signup/$', ripdapp.views.signup, name='signup'),
    url(r'^login/user/(?P<user_id>\w[\w\d_]+)$', ripdapp.views.login_as_user, name='login_as'),

    url(r'^nlogin', ripdapp.views.nlogin, name='nlogin'),
    url(r'^login/$', LoginView.as_view
        (
            template_name= 'login.html',
            authentication_form= ripdapp.forms.BootstrapAuthenticationForm,
            extra_context= {'title': 'Log in','year': datetime.now().year,}
        ),
        name='login'),
    url(r'^logout$',  LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
      
    # Enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Enable the admin:
    url(r'^admin/', admin.site.urls, name='admin_base'),

    # For working with ModelWidgets from the select2 package https://django-select2.readthedocs.io
    url(r'^select2/', include('django_select2.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # for showing pictures in Browse
