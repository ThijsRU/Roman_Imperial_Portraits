"""
Definition of 'viewsbasic' for the RIPD app: the views that make use of the basic app
"""

from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from datetime import datetime

# RIPD: basic app
from basic.views import BasicList, BasicDetails

# RIPD: forms and models
from ripdapp.forms import SignUpForm, PortraitForm
from ripdapp.models import Portrait, Emperor, Context, Location, Province, Material, PortraitMaterial, Arachne, \
    Wreathcrown, PortraitWreathcrown, Iconography, PortraitIconography


class PortraitEdit(BasicDetails):
    """The details of one emperor portrait"""

    model = Portrait
    mForm = PortraitForm
    prefix = 'prt'
    title = "Portrait"
    title_sg = "Portrait"
    rtype = "json"
    history_button = False 
    mainitems = []
    
    def add_to_context(self, context, instance):
        """Add to the existing context"""

        # Define the main items to show and edit
        context['mainitems'] = [
            {'type': 'plain', 'label': "Name:",         'value': instance.name,         'field_key': 'name'     },
            ]

        # Signal that we have select2
        context['has_select2'] = True

        # Return the context we have made
        return context


class PortraitDetails(PortraitEdit):
    """Like Portrait Edit, but then html output"""
    rtype = "html"

    def add_to_context(self, context, instance):
        # First get the 'standard' context from TestsetEdit
        context = super(PortraitDetails, self).add_to_context(context, instance)

        context['sections'] = []

        # Lists of related objects
        related_objects = []

        # Add all related objects to the context
        context['related_objects'] = related_objects

        # Return the context we have made
        return context
    

class PortraitListView(BasicList):
    """Search and list Christian feasts"""

    model = Portrait
    listform = PortraitForm
    prefix = "prt"
    has_select2 = True
    sg_name = "Portrait"
    plural_name = "Portraits"
    new_button = False  # Do *NOT* allow adding portraits right now...
    order_cols = ['origstr', 'name', 'emperor__name', 'material__name', 'location__name','height']   
    order_default = order_cols
    order_heads = [
        {'name': 'ID', 'order': 'o=2', 'type': 'str', 'field': 'origstr', 'linkdetails': True},
        {'name': 'Current location', 'order': 'o=1', 'type': 'str', 'field': 'name', 'linkdetails': True, 'main': True},
        {'name': 'Emperor', 'order': '', 'type': 'str', 'custom': 'emp_name'},
        {'name': 'Material', 'order': '', 'type': 'str', 'custom': 'mat_name'},
        {'name': 'Ancient city', 'order': '', 'type': 'str', 'custom': 'location'},
        {'name': 'Height', 'order': '', 'type': 'float', 'field': 'height', 'custom': 'links'},        
        #{'name': '',        'order': '',    'type': 'str', 'custom': 'links'}
        ]
    filters = [ 
        {"name": "Name",            "id": "filter_name",     "enabled": False},
        ]
    searches = [
        {'section': '', 'filterlist': [
            {'filter': 'name',   'dbfield': 'name',      'keyS': 'name'},
  
            ]},
        ]

    def get_field_value(self, instance, custom):
        sBack = ""
        sTitle = ""

        # Figure out what to do...
        if custom == "links":
            html = []
            html.append("[link]")
            sBack = ", ".join(html)
        elif custom == "emp_name":
            html = []
            html.append("<span>{}</span>".format(instance.emperor.name))  
            sBack = ", ".join(html)
        elif custom == "location":
            html = []
            html.append("<span>{}</span>".format(instance.location.name))  
            sBack = ", ".join(html)
        elif custom == "mat_name":
            html = []
            for item in instance.material.all():
                html.append("<div>{}</div>".format(item.name))
                sBack = "\n".join(html)
        # Return the stuff needed
        return sBack, sTitle


