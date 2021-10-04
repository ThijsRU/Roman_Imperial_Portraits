"""
Definition of 'viewsbasic' for the RIPD app: the views that make use of the basic app
"""
import os, sys
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
    Wreathcrown, PortraitWreathcrown, Iconography, PortraitIconography, Path, Photographer 

from Roman_Imperial_Portraits.settings import PICTURES_DIR

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
        
        # Here the most fields and tables related to each portrait are collected 
        # and added to the context, but only when there is data available
        def add_if_available(arThis, type, label, value, field_key):
            # print(label) to test if the labels and values are ok
            # print(value) 
            
            # Filter out the fields without data
            if value == "" or value == "-" or value == None:
                pass
            # The rest will be processed here:
            else: 
                # Convert the values of the boolean fields 
                # in the Portrait table, first True --> YES
                if value == True:
                    value = "YES"
                    oAddThis = {'type': type, 'label': label, 'value': value , 'field_key': field_key}
                    arThis.append( oAddThis )                
                # then False --> NO
                elif value == False:
                    value = "NO"
                    oAddThis = {'type': type, 'label': label, 'value': value, 'field_key': field_key}
                    arThis.append( oAddThis )
                # The rest will be processed here
                else:
                    oAddThis = {'type': type, 'label': label, 'value': value, 'field_key': field_key}
                    arThis.append( oAddThis )

        # Define the main items to show        
        context['mainitems'] = [            
            {'type': 'plain', 'label': "ID: ", 'value': instance.origstr, 'field_key': 'orid_id'},
            {'type': 'plain', 'label': "Emperor: ", 'value': instance.emperor.name, 'field_key': 'emperor'},           
            {'type': 'plain', 'label': "Portrait type: ", 'value': instance.get_types(), 'field_key': 'types'},
            ]

        # One by one evaluate the remaining items
        add_if_available(context['mainitems'], "plain", "Alternative: ", instance.get_alternatives(), 'alternatives')
        add_if_available(context['mainitems'], "plain", "Subtype: ", instance.get_subtypes(), 'subtypes') 

        add_if_available(context['mainitems'], "plain", "Identity disputed: ", instance.disputed, 'disputed')
        add_if_available(context['mainitems'], "plain", "Re-carved: ", instance.recarvedboo, 'recarved_boolean')
        add_if_available(context['mainitems'], "plain", "Original identity: ", instance.get_recarvedstatue(), 'recarvedstatue')

        # Waarom moet de door Sam gemaakte ID's er niet in?               
        add_if_available(context['mainitems'], "plain", "Original ID: ", instance.origstr, 'origstr')         
        add_if_available(context['mainitems'], "plain", "Reference(s): ", instance.reference, 'reference') 
        add_if_available(context['mainitems'], "plain", "Arachne: ", instance.get_arachne(), 'arachne') 
        add_if_available(context['mainitems'], "plain", "LSA: ", instance.lsa, 'lsa') 

        add_if_available(context['mainitems'], "plain", "Start date: ", instance.startdate, 'startdate') 
        add_if_available(context['mainitems'], "plain", "End date: ", instance.enddate, 'enddate') 
        add_if_available(context['mainitems'], "plain", "Reason for dating: ", instance.reason_date, 'reason_date') 

        add_if_available(context['mainitems'], "plain", "Material: ", instance.get_materials(), 'material') 
        add_if_available(context['mainitems'], "plain", "Height: ", instance.height, 'height') 
        add_if_available(context['mainitems'], "plain", "Height specified: ", instance.height_comment, 'height_commnt') 
        add_if_available(context['mainitems'], "plain", "Miniature: ", instance.miniature, 'miniature')
        
        add_if_available(context['mainitems'], "plain", "Name: ", instance.name, 'name')
        add_if_available(context['mainitems'], "plain", "Ancient city: ", instance.location.name, 'location')
        add_if_available(context['mainitems'], "plain", "Province: ", instance.get_province(), 'province')         
        add_if_available(context['mainitems'], "plain", "Context: ", instance.get_context(), 'context') 

        add_if_available(context['mainitems'], "plain", "Part of statue group: ", instance.part_group, 'part_statue_group')         
        add_if_available(context['mainitems'], "plain", "Name group: ", instance.group_name, 'group_name') 
        add_if_available(context['mainitems'], "plain", "Together with: ", instance.get_together(), 'together')
        add_if_available(context['mainitems'], "plain", "Reference: ", instance.group_reference, 'group_reference') 

        add_if_available(context['mainitems'], "plain", "Statue: ", instance.statue, 'statue')     
        add_if_available(context['mainitems'], "plain", "Bust: ", instance.buste, 'buste')
        add_if_available(context['mainitems'], "plain", "Toga: ", instance.toga, 'toga')
        add_if_available(context['mainitems'], "plain", "Capite velato: ", instance.capite_velato, 'capite_velato')
        add_if_available(context['mainitems'], "plain", "Cuirass: ", instance.cuirass, 'cuirass')            
        add_if_available(context['mainitems'], "plain", "Iconography cuirass: ", instance.get_iconography(), 'iconography')          
        add_if_available(context['mainitems'], "plain", "Heroic nudity: ", instance.heroic_semi_nude, 'heroic nude')
        add_if_available(context['mainitems'], "plain", "Enthroned: ", instance.seated, 'seated')
        add_if_available(context['mainitems'], "plain", "Equestrian: ", instance.equestrian, 'equestrian')

        add_if_available(context['mainitems'], "plain", "Beard: ", instance.beard, 'beard')
        add_if_available(context['mainitems'], "plain", "Paludamentum: ", instance.paludamentum, 'paludamentum')
        add_if_available(context['mainitems'], "plain", "Sword belt: ", instance.sword_belt, 'sword_belt')
        add_if_available(context['mainitems'], "plain", "Contabulata: ", instance.contabulata, 'contabulata')
        
        add_if_available(context['mainitems'], "plain", "Headgear: ", instance.headgear, 'headgear')
        add_if_available(context['mainitems'], "plain", "Corona laurea: ", instance.corona_laurea, 'corona_laurea')
        add_if_available(context['mainitems'], "plain", "Corona civica: ", instance.corona_civica, 'corona_civica')
        add_if_available(context['mainitems'], "plain", "Corona radiata: ", instance.corona_radiata, 'corona_radiata')        
        add_if_available(context['mainitems'], "plain", "Other: ", instance.get_wreathcrown(), 'wreathcrown')

        add_if_available(context['mainitems'], "plain", "Additional attributes: ", instance.get_attributes(), 'attributes')

        #add_if_available(context['mainitems'], "plain", "Photo folder: ", instance.get_photofolder(), 'photo folder')
                
        add_if_available(context['mainitems'], "plain", "Photo by © : ", instance.get_photographer(), 'photographer') # dit werkt niet meer
        add_if_available(context['mainitems'], "plain", "Photo: ", instance.get_photopath(), 'photo path') # idem

        # class ManuscriptEdit(BasicDetails):
        # https://github.com/ErwinKomen/RU-passim/blob/master/passim/passim/seeker/views.py#L8399


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
        # Regel met plaatje, name empty, order idem, type str custom, zie onder custom: 'picture'
        {'name': 'Photo', 'order': '', 'type': 'int', 'custom': 'picture', 'linkdetails': True},
        {'name': 'ID', 'order': 'o=1', 'type': 'int', 'field': 'origstr', 'linkdetails': True},
        {'name': 'Current location', 'order': 'o=2', 'type': 'str', 'field': 'name', 'linkdetails': True, 'main': True},
        {'name': 'Emperor', 'order': '', 'type': 'str', 'custom': 'emp_name'},
        {'name': 'Material', 'order': '', 'type': 'str', 'custom': 'mat_name'},
        {'name': 'Ancient city', 'order': '', 'type': 'str', 'custom': 'location'},        
        ]
    # Nog geen typeahead, maar er is al een beetje op name te zoeken!
    filters = [ 
        {"name": "Name",                "id": "filter_name",            "enabled": False},
        {"name": "Emperor",             "id": "filter_emperor",         "enabled": False},
        {"name": "Material",            "id": "filter_material",        "enabled": False},
        {"name": "Disputed",            "id": "filter_disputed",        "enabled": False},
        {"name": "Recarved",            "id": "filter_recarvedboo",     "enabled": False},
        {"name": "Original identity",   "id": "filter_orig_identity",   "enabled": False},
        {"name": "Ancient city",        "id": "filter_ancient_city",    "enabled": False},
        {"name": "Province",            "id": "filter_province",        "enabled": False},
        {"name": "Statues",             "id": "filter_statue",          "enabled": False},
        {"name": "Busts",               "id": "filter_bust",            "enabled": False},
        {"name": "Context",             "id": "filter_context",         "enabled": False},
        {"name": "Toga",                "id": "filter_toga",            "enabled": False},
        {"name": "Cuirass",             "id": "filter_cuirass",         "enabled": False},
        {"name": "Heroic nudity",       "id": "filter_heroic_semi_nude","enabled": False},
        {"name": "Enthroned",           "id": "filter_seated",          "enabled": False},
        {"name": "Paludamentum",        "id": "filter_paludamentum",    "enabled": False},
        {"name": "Sword belt",          "id": "filter_sword_belt",      "enabled": False},
        {"name": "Capite velato",       "id": "filter_capite_velato",   "enabled": False},
        {"name": "Iconography cuirass", "id": "filter_icon_cuirass",    "enabled": False},
        {"name": "Other attributes",    "id": "filter_attributes",      "enabled": False},
        {"name": "Corona laurea",       "id": "filter_corona_laurea",   "enabled": False},
        {"name": "Corona civica",       "id": "filter_corona_civica",   "enabled": False},
        {"name": "Corona radiata",      "id": "filter_corona_radiata",  "enabled": False},
        {"name": "References",          "id": "filter_reference",      "enabled": False},
        {"name": "Arachne",             "id": "filter_arachne",         "enabled": False},
        {"name": "LSA",                 "id": "filter_lsa",             "enabled": False}

        ]
    searches = [
        {'section': '', 'filterlist': [
            {'filter': 'name',           'dbfield': 'name',                   'keyS': 'name'},
            {'filter': 'emperor',        'fkfield': 'emperor', 'keyS': 'empname', 'keyId': 'emperor', 'keyFk': "name"}, # PASSIM library voorbeeld?
            {'filter': 'disputed',       'dbfield': 'disputed',               'keyS': 'disputed'},            
            {'filter': 'recarvedboo',    'dbfield': 'recarvedboo',            'keyS': 'recarvedboo'},
            {'filter': 'orig_identity',  'dbfield': 'origstr',                'keyS': 'origstr'},
            {'filter': 'ancient_city',   'fkfield': 'location', 'keyS': 'locname', 'keyId': 'location', 'keyFk': "name"}, # PASSIM library voorbeeld?
            {'filter': 'province',       'fkfield': 'location__province', 'keyS': 'provname', 'keyId': 'province', 'keyFk': "name"}, # PASSIM library voorbeeld?
            {'filter': 'statue',         'dbfield': 'statue',                 'keyS': 'statue'},
            {'filter': 'bust',           'dbfield': 'buste',                  'keyS': 'buste'},
            {'filter': 'context',         'fkfield': 'context', 'keyS': 'contname', 'keyId': 'context', 'keyFk': "name"}, 
            {'filter': 'material',        'fkfield': 'material', 'keyS': 'matname','keyId': 'material', 'keyFk': "name"},
            {'filter': 'toga',            'dbfield': 'toga',              'keyS': 'toga'},
            {'filter': 'cuirass',         'dbfield': 'cuirass',           'keyS': 'cuirass'},
            {'filter': 'heroic_semi_nude','dbfield': 'heroic_semi_nude', 'keyS': 'heroic_semi_nude'},
            {'filter': 'seated',          'dbfield': 'seated',           'keyS': 'seated'},
            {'filter': 'paludamentum',    'dbfield': 'paludamentum',     'keyS': 'paludamentum'},
            {'filter': 'sword_belt',      'dbfield': 'sword_belt',       'keyS': 'sword_belt'},
            {'filter': 'icon_cuirass',    'fkfield': 'iconography',      'keyS': 'iconname', 'keyId': 'iconography', 'keyFk': "name"}, 
            {'filter': 'attributes',      'fkfield': 'attribute',        'keyS': 'attrname', 'keyId': 'attributes', 'keyFk': "name"},
            {'filter': 'capite_velato',   'dbfield': 'capite_velato',    'keyS': 'capite_velato'},
            {'filter': 'corona_laurea',   'dbfield': 'corona_laurea',    'keyS': 'corona_laurea'},
            {'filter': 'corona_civica',   'dbfield': 'corona_civica',    'keyS': 'corona_civica'},
            {'filter': 'corona_radiata',  'dbfield': 'corona_radiata',   'keyS': 'corona_radiata'},
            {'filter': 'reference',       'dbfield': 'reference',        'keyS': 'reference'},
            {'filter': 'arachne',         'fkfield': 'arachne_portrait', 'keyS': 'arachid', 'keyId': 'arachne', 'keyFk': "arachne"},            
            {'filter': 'lsa',             'dbfield': 'lsa',              'keyS': 'lsa'},

            ]},
        ]

    # https://cls.ru.nl/staff/ekomen/passimutils

    def get_field_value(self, instance, custom):
        sBack = ""
        sTitle = ""                       
        if custom == "emp_name":            
            html = []
            html.append("<span>{}</span>".format(instance.emperor.name)) 
            sBack = ", ".join(html)
        elif custom == "picture":            
            # If there are images available, get the first one            
            html = []
            # Pickup all available paths 
            qs = instance.path_portrait.all()
            # Only go forward when there is an image available
            if len(qs) > 0:
                # Select the first on                
                item1 = qs.first()                  
                # Add the path to the html
                html.append("<img src='/{}' style='max-width: 75px; width: auto; height: auto;'/>".format(item1)) 
                sBack = "\n".join(html)
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


