"""
Definition of 'viewsbasic' for the RIPD app: the views that make use of the basic app
"""
import os, sys
from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from datetime import datetime
from django.utils.translation import gettext as _

from basic.utils import ErrHandle

# RIPD: basic app
from basic.views import BasicList, BasicDetails

# RIPD: forms and models
from ripdapp.forms import SignUpForm, PortraitForm
from ripdapp.models import Portrait, Emperor, Context, Location, Province, Material, PortraitMaterial, Arachne, \
    Wreathcrown, PortraitWreathcrown, Iconography, PortraitIconography, Path, Photographer, Information, Table_1, Table_2, Table_3 

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

    #nextitems = [] # for testing how to split up the labels and values in the Portrait View
    
    def custom_init(self, instance):
        # Check and set the authentication if needed
        auth = Information.get_kvalue("authenticated")
        if auth.lower() in ['true', 'ok', 'set']:
            self.authenticated = True
        return None
        
    def add_to_context(self, context, instance):
        """Add to the existing context"""
        
        # Here the most fields and tables related to each portrait are collected 
        # and added to the context, but only when there is data available
        def add_if_available(arThis, type, label, value, field_key):
            print(label) #to test if the labels and values are ok
            print(value) 
            # TH: hier afvangen wat niet getoond moet worden, is dat alvast te testen?
            
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
                    list = ["Toga: ","Headgear: ", "Identity disputed: ", "Re-carved: ", "Miniature: ", "Statue: ", "Bust: ", "Capite velato: ", 
                            "Cuirass: ", "Heroic nudity: ", "Enthroned: ", "Equestrian: ", "Beard: ", "Paludamentum: ", "Sword belt: ", 
                            "Contabulata: ", "Headgear: ", "Corona laurea: ", "Corona civica: ", "Corona radiata: "]
                    print(label, value) 
                    value = "NO"  
                    if label in list:                        
                        #pass --> TH dit dit omzetten wanneer de lijst van Sam er is, zal wel schema zijn
                        oAddThis = {'type': type, 'label': label, 'value': value, 'field_key': field_key}                    
                        arThis.append( oAddThis )
                    else:
                        oAddThis = {'type': type, 'label': label, 'value': value, 'field_key': field_key}                    
                        arThis.append( oAddThis )
                # The rest will be processed here
                else:
                    oAddThis = {'type': type, 'label': label, 'value': value, 'field_key': field_key}
                    arThis.append( oAddThis )

        # Define the main items to show        
        context['mainitems'] = [            
            {'type': 'plain', 'label': "RIPD id: ", 'value': instance.origstr, 'field_key': 'origstr'},
            {'type': 'plain', 'label': "Emperor: ", 'value': instance.emperor.name, 'field_key': 'empname'},   #get_emperor_markdown()        
            #{'type': 'plain', 'label': "Emperor: ", 'value': instance.get_emperor_markdown(), 'field_key': 'empname'},   #get_emperor_markdown()        
            {'type': 'plain', 'label': "Portrait type: ", 'value': instance.get_types()}, 
            ] # waarom niet alles zo? Of selectie wat hier moet komen en de rest in diesections? waarom werken die niet?

        # One by one evaluate the remaining items
        #add_if_available(context['mainitems'], "plain", "Alternative: ", instance.get_alternatives(), 'alternatives')
        add_if_available(context['mainitems'], "plain", "Subtype: ", instance.get_subtypes(), 'subtypes') 
        add_if_available(context['mainitems'], "plain", "Identity disputed: ", instance.get_disputed, 'disputed')         
        add_if_available(context['mainitems'], "plain", "Re-carved: ", instance.get_recarved, 'recarvedboo')
        add_if_available(context['mainitems'], "plain", "Original identity: ", instance.get_recarvedstatue(), 'recarvedstatue') 
                 
        add_if_available(context['mainitems'], "plain", "RIPD id: ", instance.origstr, 'origstr')  
        add_if_available(context['mainitems'], "plain", "Reference(s): ", instance.reference, 'reference') 
        
        #add_if_available(context['mainitems'], "plain", "Arachne: ", instance.get_arachne(), 'arachid')  
        #add_if_available(context['mainitems'], "plain", "LSA: ", instance.lsa, 'lsa') 
        #add_if_available(context['mainitems'], "plain", "LSA: ", instance.get_lsa_markdown(), 'lsa') 

        #add_if_available(context['mainitems'], "plain", "Start date: ", instance.startdate, 'startdate') 
        #add_if_available(context['mainitems'], "plain", "End date: ", instance.enddate, 'enddate') 
        #add_if_available(context['mainitems'], "plain", "Reason for dating: ", instance.reason_date, 'reason_date') 

        #add_if_available(context['mainitems'], "plain", "Material: ", instance.get_materials(), 'material') 
        #add_if_available(context['mainitems'], "plain", "Height: ", instance.height, 'height') 
        #add_if_available(context['mainitems'], "plain", "Height specified: ", instance.height_comment, 'height_comment') 
        #add_if_available(context['mainitems'], "plain", "Miniature: ", instance.miniature, 'miniature')
                
        #add_if_available(context['mainitems'], "plain", "Name: ", instance.get_name_markdown, 'name')
        #add_if_available(context['mainitems'], "plain", "Ancient city: ", instance.location.name, 'location')
        #add_if_available(context['mainitems'], "plain", "Province: ", instance.get_province(), 'province')         
        #add_if_available(context['mainitems'], "plain", "Context: ", instance.get_context(), 'context') 

        #add_if_available(context['mainitems'], "plain", "Part of statue group: ", instance.part_group, 'part_statue_group')         
        #add_if_available(context['mainitems'], "plain", "Name group: ", instance.group_name, 'group_name') 
        #add_if_available(context['mainitems'], "plain", "Together with: ", instance.get_together(), 'together')
        #add_if_available(context['mainitems'], "plain", "Reference: ", instance.group_reference, 'group_reference') 
        #add_if_available(context['mainitems'], "plain", "Statue: ", instance.statue, 'statue')     
        #add_if_available(context['mainitems'], "plain", "Bust: ", instance.buste, 'buste')
        #add_if_available(context['mainitems'], "plain", "Toga: ", instance.toga, 'toga')
        #add_if_available(context['mainitems'], "plain", "Capite velato: ", instance.capite_velato, 'capite_velato')
        #add_if_available(context['mainitems'], "plain", "Cuirass: ", instance.cuirass, 'cuirass')            
        #add_if_available(context['mainitems'], "plain", "Iconography cuirass: ", instance.get_iconography(), 'iconography')          
        #add_if_available(context['mainitems'], "plain", "Heroic nudity: ", instance.heroic_semi_nude, 'heroic_semi_nude')
        #add_if_available(context['mainitems'], "plain", "Enthroned: ", instance.seated, 'seated')
        #add_if_available(context['mainitems'], "plain", "Equestrian: ", instance.equestrian, 'equestrian')
        #add_if_available(context['mainitems'], "plain", "Beard: ", instance.beard, 'beard')
        #add_if_available(context['mainitems'], "plain", "Paludamentum: ", instance.paludamentum, 'paludamentum')
        #add_if_available(context['mainitems'], "plain", "Sword belt: ", instance.sword_belt, 'sword_belt')
        #add_if_available(context['mainitems'], "plain", "Contabulata: ", instance.contabulata, 'contabulata')        
        #add_if_available(context['mainitems'], "plain", "Headgear: ", instance.headgear, 'headgear')
        #add_if_available(context['mainitems'], "plain", "Corona laurea: ", instance.corona_laurea, 'corona_laurea')
        #add_if_available(context['mainitems'], "plain", "Corona civica: ", instance.corona_civica, 'corona_civica')
        #add_if_available(context['mainitems'], "plain", "Corona radiata: ", instance.corona_radiata, 'corona_radiata')        
        #add_if_available(context['mainitems'], "plain", "Other: ", instance.get_wreathcrown(), 'wreathcrown')
        #add_if_available(context['mainitems'], "plain", "Additional attributes: ", instance.get_attributes(), 'attributes')
        #add_if_available(context['mainitems'], "plain", "Photo folder: ", instance.get_photofolder(), 'photo_folder') # Hierna? mis?
                
        add_if_available(context['mainitems'], "plain", "Photo by © : ", instance.get_photographer(), 'photographer') 
        add_if_available(context['mainitems'], "plain", "Photo: ", instance.get_photopath(), 'photo_path') 

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





        # Sections: References / Date / Material and Height / Statue group / Location / Attributes
        # TH: alles bij elkaar lijkt mij
        context['sections'] = [
            {'name': 'References', 'id': 'portrait_references', 'fields': [
                {'type': 'safeline',    'label': "References: ", 'value': instance.get_reference()},
                {'type': 'safeline',    'label': "LSA: ", 'value': instance.get_lsa_markdown()},
                {'type': 'safeline',    'label': "Arachne: ", 'value': instance.get_arachne()},
                ]},
            {'name': 'Date', 'id': 'portrait_date', 'fields': [
                {'type': 'safeline',    'label': "Start date: ", 'value': instance.startdate},
                {'type': 'safeline',    'label': "End date: ", 'value': instance.enddate},
                {'type': 'safeline',    'label': "Reason for dating: ", 'value': instance.get_reason_date()},
                ]},
            {'name': 'Material and Height', 'id': 'portrait_material_height', 'fields': [
                {'type': 'safeline',    'label': "Material: ", 'value': instance.get_materials()},
                {'type': 'safeline',    'label': "Height: ", 'value': instance.get_height()},
                {'type': 'safeline',    'label': "Height specified: ", 'value': instance.get_height_comment()},
                {'type': 'safeline',    'label': "Miniature: ", 'value': instance.get_miniature()},
                ]},
            {'name': 'Statue group', 'id': 'portrait_statue_group', 'fields': [
                {'type': 'safeline',    'label': "Part of statue group: ", 'value': instance.get_part_group()},
                {'type': 'safeline',    'label': "Name group: ", 'value': instance.get_group_name()},
                {'type': 'safeline',    'label': "Together with: ", 'value': instance.get_together()},
                {'type': 'safeline',    'label': "Reference: ", 'value': instance.get_group_reference()},
                ]},
            {'name': 'Location', 'id': 'portrait_location', 'fields': [
                {'type': 'safeline',    'label': "Name: ", 'value': instance.get_name_markdown()},
                {'type': 'safeline',    'label': "Current location: ", 'value': instance.currentlocation.name},
                {'type': 'safeline',    'label': "Ancient city: ", 'value': instance.location.name},
                {'type': 'safeline',    'label': "Province: ", 'value': instance.get_province()},
                {'type': 'safeline',    'label': "Context: ", 'value': instance.get_context()},                
                ]},                
            {'name': 'Attributes', 'id': 'portrait_attributes', 'fields': [
                {'type': 'safeline',    'label': "Statue: ", 'value': instance.get_statue()},
                {'type': 'safeline',    'label': "Bust: ", 'value': instance.get_buste()},
                {'type': 'safeline',    'label': "Toga: ", 'value': instance.get_toga()},
                {'type': 'safeline',    'label': "Capite velato: ", 'value': instance.get_capite_velato()},
                {'type': 'safeline',    'label': "Cuirass: ", 'value': instance.get_cuirass()},

                {'type': 'safeline',    'label': "Iconography cuirass: ", 'value': instance.get_iconography()},
                {'type': 'safeline',    'label': "Heroic nudity: ", 'value': instance.get_heroic_semi_nude()},
                {'type': 'safeline',    'label': "Enthroned: ", 'value': instance.get_seated()},
                {'type': 'safeline',    'label': "Equestrian: ", 'value': instance.get_equestrian()},

                {'type': 'safeline',    'label': "Beard: ", 'value': instance.get_beard()},
                {'type': 'safeline',    'label': "Paludamentum: ", 'value': instance.get_paludamentum()},
                {'type': 'safeline',    'label': "Sword belt: ", 'value': instance.get_sword_belt()},
                {'type': 'safeline',    'label': "Contabulata: ", 'value': instance.get_contabulata()},

                {'type': 'safeline',    'label': "Headgear: ", 'value': instance.get_headgear()},
                {'type': 'safeline',    'label': "Corona laurea: ", 'value': instance.get_corona_laurea()},
                {'type': 'safeline',    'label': "Corona civica: ", 'value': instance.get_corona_civica()},
                {'type': 'safeline',    'label': "Corona radiata: ", 'value': instance.get_corona_radiata()},
                {'type': 'safeline',    'label': "Other: ", 'value': instance.get_wreathcrown()},
                {'type': 'safeline',    'label': "Additional attributes: ", 'value': instance.get_attributes()},
                ]}]
             
        # Lists of related objects
        related_objects = []

        # Add all related objects to the context
        context['related_objects'] = related_objects

        # Return the context we have made TH: sections gaan hier mee
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
    order_cols = ['id', 'name', 'emperor__name', 'material__name', 'location__name','height', 'startdate', 'enddate']   
    order_default = order_cols
    order_heads = [
        # Regel met plaatje, name empty, order idem, type str custom, zie onder custom: 'picture'
        {'name': 'Photo', 'order': '', 'type': 'int', 'custom': 'picture', 'linkdetails': True},
        {'name': 'ID', 'order': 'o=1', 'type': 'int', 'field': 'id', 'linkdetails': True},
        {'name': 'Current location', 'order': 'o=2', 'type': 'str', 'field': 'name', 'linkdetails': True, 'main': True},
        {'name': 'Emperor', 'order': '', 'type': 'str', 'custom': 'emp_name'},
        {'name': 'Material', 'order': '', 'type': 'str', 'custom': 'mat_name'},
        {'name': 'Ancient city', 'order': '', 'type': 'str', 'custom': 'location'},        
        {'name': 'From', 'order': '', 'type': 'int', 'field': 'startdate'},
        {'name': 'Until', 'order': '', 'type': 'int', 'field': 'enddate'},
        ]
    
    filter_sections = [
            {"id": "main",      "section": ""},
            {"id": "identity",  "section": _("Identity")},
            {"id": "material",  "section": _("Material")},
            {"id": "recarved",  "section": _("Recarved")},
            {"id": "date",      "section": _("Date")},
            {"id": "provenance","section": _("Provenance")},
            {"id": "costume",   "section": _("Costume")},
            {"id": "headgear",  "section": _("Headgear")},
            {"id": "references","section": _("References")},
            ]

    filters = [             
            {"name": _("RIPD id"),         "id": "filter_id",              "enabled": False, "section": "identity", "show": "none"}, 
            {"name": _("Name"),            "id": "filter_name",            "enabled": False, "section": "identity", "show": "none"},
            {"name": _("Emperor"),         "id": "filter_emperor",         "enabled": False, "section": "identity", "show": "none"},
            {"name": _("Disputed"),        "id": "filter_disputed",        "enabled": False, "section": "identity", "show": "label"},
            {"name": _("Material"),        "id": "filter_material",        "enabled": False, "section": "material", "show": "none"},
            {"name": _("Statue"),          "id": "filter_statue",          "enabled": False, "section": "material", "show": "label"}, 
            {"name": _("Buste"),           "id": "filter_buste",           "enabled": False, "section": "material", "show": "label"},           
            {"name": _("Recarved"),         "id": "filter_recarvedboo",    "enabled": False, "section": "recarved", "show": "label"}, 
            {"name": _("Original identity"),"id": "filter_orig_identity",  "enabled": False, "section": "recarved", "show": "none"},                        
            {"name": _("Date range"),       "id": "filter_daterange",      "enabled": False, "section": "date", "show": "label"},           
            {"name": _("Ancient city"),     "id": "filter_ancient_city",     "enabled": False, "section": "provenance", "show": "none"}, 
            {"name": _("Current location"), "id": "filter_current_location", "enabled": False, "section": "provenance", "show": "none"}, 
            {"name": _("Statue group"),     "id": "filter_statue_group",     "enabled": False, "section": "provenance", "show": "label"}, 
            {"name": _("Province"),         "id": "filter_province",         "enabled": False, "section": "provenance", "show": "none"}, 
            {"name": _("Context"),          "id": "filter_context",          "enabled": False, "section": "provenance", "show": "none"},             
            {"name": _("Toga"),                "id": "filter_toga",             "enabled": False, "section": "costume", "show": "label"},
            {"name": _("Cuirass"),             "id": "filter_cuirass",          "enabled": False, "section": "costume", "show": "label"},
            {"name": _("Heroic nudity"),       "id": "filter_heroic_semi_nude", "enabled": False, "section": "costume", "show": "label"},
            {"name": _("Enthroned"),           "id": "filter_seated",           "enabled": False, "section": "costume", "show": "label"},
            {"name": _("Paludamentum"),        "id": "filter_paludamentum",     "enabled": False, "section": "costume", "show": "label"},
            {"name": _("Sword belt"),          "id": "filter_sword_belt",       "enabled": False, "section": "costume", "show": "label"},
            {"name": _("Capite velato"),       "id": "filter_capite_velato",    "enabled": False, "section": "costume", "show": "label"},
            {"name": _("Iconography cuirass"), "id": "filter_icon_cuirass",     "enabled": False, "section": "costume", "show": "none"},
            {"name": _("Other attributes"),    "id": "filter_attributes",       "enabled": False, "section": "costume", "show": "none"},
            {"name": _("Corona laurea"),     "id": "filter_corona_laurea",      "enabled": False, "section": "headgear", "show": "label"},
            {"name": _("Corona civica"),     "id": "filter_corona_civica",      "enabled": False, "section": "headgear", "show": "label"},
            {"name": _("Corona radiata"),    "id": "filter_corona_radiata",     "enabled": False, "section": "headgear", "show": "label"},
            {"name": _("Other"),             "id": "filter_wreath_crown",       "enabled": False, "section": "headgear", "show": "none"},
            {"name": _("References"),        "id": "filter_reference",          "enabled": False, "section": "references", "show": "none"},
            {"name": _("Arachne"),           "id": "filter_arachne",            "enabled": False, "section": "references", "show": "none"},
            {"name": _("LSA"),               "id": "filter_lsa",                "enabled": False, "section": "references", "show": "none"},
            ]

    searches = [
        {'section': '', 'filterlist': [
            {'filter': 'id',             'dbfield': 'origstr',  'keyList': 'origidlist' },
            {'filter': 'name',           'dbfield': 'name',     'keyList': 'namelist' },    
            {'filter': 'emperor',        'fkfield': 'emperor',  'keyList': 'emplist', 'infield': 'name'},
            {'filter': 'disputed',       'dbfield': 'disputed', 'keyS': 'disputed_free'},
            {'filter': 'material',       'fkfield': 'material', 'keyList': 'matlist', 'infield': 'name'}, 
            {'filter': 'statue',         'dbfield': 'statue',   'keyS': 'statue_free'},
            {'filter': 'buste',          'dbfield': 'buste',    'keyS': 'buste_free'}, 
            {'filter': 'recarvedboo',    'dbfield': 'recarvedboo', 'keyS': 'recarvedboo_free'},
            {'filter': 'orig_identity',  'fkfield': 'recarved_from', 'keyList': 'recarvedlist', 'infield': 'name'}, 
            {'filter': 'daterange',      'dbfield': 'startdate', 'keyS': 'date_from'},
            {'filter': 'daterange',      'dbfield': 'enddate',   'keyS': 'date_until'}, 
            {'filter': 'ancient_city',   'fkfield': 'location',  'keyS': 'locname', 'keyId': 'location', 'keyFk': "name"},
            {'filter': 'current_location','fkfield': 'currentlocation', 'keyList': 'curloclist', 'infield': 'name'},     
            {'filter': 'statue_group',    'dbfield': 'part_group', 'keyS': 'part_group_free'},          
            {'filter': 'province',        'fkfield': 'location__province', 'keyList': 'provlist', 'infield': 'name'},     
            {'filter': 'context',         'fkfield': 'context', 'keyList': 'contlist', 'infield': 'name'},
            {'filter': 'toga',            'dbfield': 'toga',             'keyS': 'toga_free'},
            {'filter': 'cuirass',         'dbfield': 'cuirass',          'keyS': 'cuirass_free'},
            {'filter': 'heroic_semi_nude','dbfield': 'heroic_semi_nude', 'keyS': 'heroic_semi_nude_free'},
            {'filter': 'seated',          'dbfield': 'seated',           'keyS': 'seated_free'},
            {'filter': 'paludamentum',    'dbfield': 'paludamentum',     'keyS': 'paludamentum_free'},
            {'filter': 'sword_belt',      'dbfield': 'sword_belt',       'keyS': 'sword_belt_free'},
            {'filter': 'icon_cuirass',    'fkfield': 'iconography',      'keyList': 'iconlist', 'infield': 'name'}, 
            {'filter': 'attributes',      'fkfield': 'attribute',        'keyList': 'attrlist', 'keyFk': "name"},
            {'filter': 'capite_velato',   'dbfield': 'capite_velato',    'keyS': 'capite_velato_free'},     
            {'filter': 'corona_laurea',   'dbfield': 'corona_laurea',    'keyS': 'corona_laurea_free'},
            {'filter': 'corona_civica',   'dbfield': 'corona_civica',    'keyS': 'corona_civica_free'},
            {'filter': 'corona_radiata',  'dbfield': 'corona_radiata',   'keyS': 'corona_radiata_free'},            
            {'filter': 'wreath_crown',    'fkfield': 'wreathcrown',      'keyList': 'wreathlist', 'infield': 'name'}, 
            {'filter': 'reference',       'dbfield': 'reference',        'keyList': 'referenceslist'}, # 'keyS': 'reference'                       
            {'filter': 'arachne',         'fkfield': 'arachne_portrait', 'keyS': 'arachid', 'keyId': 'arachne', 'keyFk': "arachne"},
            {'filter': 'lsa',             'dbfield': 'lsa',              'keyS': 'lsa'},
            ]},
        ]

    # https://cls.ru.nl/staff/ekomen/passimutils

    def add_to_context(self, context, initial):
        oErr = ErrHandle()
        try:

            filtercount = 0
            for oItem in self.filters:
                if oItem['enabled']:
                    filtercount += 1
            context['filtercount'] = filtercount
            for section in self.filter_sections:
                section['enabled'] = False
                # See if this needs enabling
                for oItem in self.filters:
                    if oItem['section'] == section['id'] and oItem['enabled']:
                        section['enabled'] = True
                        break
            context['filter_sections'] = self.filter_sections

            # Possibly take over generic_search
            #context['generic_search'] = self.qd.get("wer-generic", "")

            # Calculate how many items will be shown on the map
            #qs_mapview = self.qs.exclude(locatie__x_coordinaat="onbekend")
            #context['mapcount'] = qs_mapview.count()

            # Add a user_button definition
            context['mode'] = "list"
            #context['language'] = self.language
            #context['user_button'] = render_to_string("seeker/map_list_switch.html", context, self.request)

            context['no_result_count'] = True

            context['authenticated'] = True

        except:
            msg = oErr.get_error_message()
            oErr.DoError("PortraitListview/add_to_context")

        return context

    def custom_init(self):
        # Check and set the authentication if needed
        auth = Information.get_kvalue("authenticated")
        if auth.lower() in ['true', 'ok', 'set']:
            self.authenticated = True
        return None

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

    def adapt_search(self, fields):
        lstExclude=None
        qAlternative = None

        # The search for start and/or enddate needs to be modified in order to be able to search 
        # using the startdate and/or enddate and ranges. 

        # First get the date_from and/or date_until          
        date_from = fields.get("date_from")
        date_until = fields.get("date_until")

        # In case there is both a date_from and date_until:
        if not date_from is None and not date_until is None: 
            fields['date_from'] =  Q(enddate__gte=date_from) & Q(startdate__lte=date_from) 

        # If there is only date_from input than all portraits AFTER the input year should be listed (GTE)
        elif not date_from is None and date_until is None:
             fields['date_from'] =  Q(enddate__gte=date_from)      

        # If there is date_until input...
        if not date_until is None:
            qExpr_both_inputs = Q(startdate__lte=date_until) & Q(enddate__gte=date_until) # for both inputs
            qExpr_only_until = Q(startdate__lte=date_until) # for only date_until

            # If there is ONLY date_unitil input, all portraits BEFORE the input should be listed (LTE)
            if date_from is None:
                fields['date_until'] = qExpr_only_until # ipv qExpr
            else:
                # If there are both inputs, not only should the portraits be listed that have a 
                # daterange in which one of the input falls but ALL portraits that have dateranges 
                # that fall inbetween those inputs
                fields['date_until'] = "" 
                # What about ranges that do not overlap with date_from and date_until?
                qBetween_both_inputs = Q(startdate__gte=date_from) & Q(enddate__lte=date_until)
                # Combine the query:
                fields['date_from'] = ( fields['date_from'] ) | ( qExpr_both_inputs ) | ( qBetween_both_inputs )

        return fields, lstExclude, qAlternative


#class Table1Edit(BasicDetails):
#    """Table 1: Number of extant imperial portraits and bases."""

#    model = Table_1
#    mForm = PortraitForm
#    prefix = 'tab1'
#    title = "Portrait"
#    title_sg = "Portrait"
#    rtype = "json"
#    history_button = False 
#    mainitems = []

#    def add_to_context(self, context, instance):
#        """Add to the existing context"""

#        #if instance.settype == "hc" and context['is_app_editor'] and self.manu == None and self.codico == None:
#        context['mainitems'].append(
#        {'type': 'safe', 'label': "Show/hide:", 'value': self.get_hc_buttons(instance),
#         'title': 'Optionally show Table 1 '})
                
#        # Signal that we have select2
#        context['has_select2'] = True

#        #Return the context we have made
#        return context

#    def get_table_buttons(self, instance):
#        """Get buttons to show/hide the three tables of the Additional materials section)"""

#        sBack = ""
#        lHtml = []
#        abbr = None
#        button_list = [
#            {'label': 'Table_1','id': 'basic_table1_set', 'show': False}, # aanpassen basic_super_set
#            {'label': 'Table_2','id': 'basic_table2_set', 'show': True},
#            {'label': 'Table_3','id': 'basic_table3_set', 'show': True},
#            ]
#        oErr = ErrHandle()
#        try:
#            for oButton in button_list:
#                lHtml.append("<a role='button' class='btn btn-xs jumbo-1' data-toggle='collapse' data-target='#{}' >{}</a>".format(
#                    oButton['id'], oButton['label']))
#            sBack = "<span>&nbsp;</span>".join(lHtml)
#        except:
#            msg = oErr.get_error_message()
#            oErr.DoError("Table1/get_hc_buttons") # ??

#        return sBack
