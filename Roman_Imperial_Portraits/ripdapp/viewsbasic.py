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
    Wreathcrown, PortraitWreathcrown, Iconography, PortraitIconography, Photo

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

        # Define the main items to show and edit TH: HIER VERDER zie PASSIM niet 
        # class ManuscriptEdit(BasicDetails):
        # https://github.com/ErwinKomen/RU-passim/blob/master/passim/passim/seeker/views.py#L8399
        context['mainitems'] = [            
            {'type': 'plain', 'label': "Emperor: ", 'value': instance.emperor.name, 'field_key': 'emperor'},           
            {'type': 'plain', 'label': "Portrait type: ", 'value': instance.get_types(), 'field_key': 'types'},
            {'type': 'plain', 'label': "Alternative: ", 'value': instance.get_alternatives(), 'field_key': 'alternatives'},
            {'type': 'plain', 'label': "Subtype: ", 'value': instance.get_subtypes(), 'field_key': 'subtypes'},
                                  
            {'type': 'plain', 'label': "Identity disputed: ", 'value': instance.disputed, 'field_key': 'disputed'},
            {'type': 'plain', 'label': "Re-carved: ", 'value': instance.recarvedboo, 'field_key': 'recarved_boolean'},
           
            # Hieronder gaat het mis. Nu ok?
            {'type': 'plain', 'label': "Original identity: ", 'value': instance.get_recarvedstatue(), 'field_key': 'recarvedstatue'},
            
            {'type': 'plain', 'label': "Original ID: ", 'value': instance.origstr,'field_key': 'origstr'},
            
            {'type': 'plain', 'label': "Reference(s): ", 'value': instance.reference,'field_key': 'reference'},
            # Arachne
            #{'type': 'plain', 'label': "Arachne: ", 'value': instance.get_arachne(),'field_key': 'arachne'},
            {'type': 'plain', 'label': "LSA: ", 'value': instance.lsa,'field_key': 'lsa'},

            {'type': 'plain', 'label': "Start date: ", 'value': instance.startdate,'field_key': 'startdate'},
            {'type': 'plain', 'label': "End date: ", 'value': instance.enddate,'field_key': 'enddate'},
            {'type': 'plain', 'label': "Reason for dating: ", 'value': instance.reason_date,'field_key': 'reason_date'},
                        
            {'type': 'plain', 'label': "Material: ", 'value': instance.get_materials(), 'field_key': 'material'},
            {'type': 'plain', 'label': "Height: ", 'value': instance.height,'field_key': 'height'},
            {'type': 'plain', 'label': "Height specified: ", 'value': instance.height_comment,'field_key': 'height_comment'},
            {'type': 'plain', 'label': "Miniature: ", 'value': instance.miniature, 'field_key': 'miniature'},

            {'type': 'plain', 'label': "Name: ", 'value': instance.name, 'field_key': 'name'},
            {'type': 'plain', 'label': "Ancient city: ", 'value': instance.location.name,'field_key': 'location'},
            # Province TO DO            
            {'type': 'plain', 'label': "Context: ", 'value': instance.context.name,'field_key': 'context'},

            {'type': 'plain', 'label': "Part of statue group: ", 'value': instance.part_group, 'field_key': 'miniature'},
            {'type': 'plain', 'label': "Name group: ", 'value': instance.group_name,'field_key': 'group_name'},
            {'type': 'plain', 'label': "Reference: ", 'value': instance.group_reference,'field_key': 'group_reference'},
            
            {'type': 'plain', 'label': "Statue: ", 'value': instance.statue, 'field_key': 'statue'},
            {'type': 'plain', 'label': "Bust: ", 'value': instance.buste, 'field_key': 'bust'},
            {'type': 'plain', 'label': "Toga: ", 'value': instance.toga, 'field_key': 'toga'},
            {'type': 'plain', 'label': "Capite velato : ", 'value': instance.capite_velato, 'field_key': 'capite_velato'},
            {'type': 'plain', 'label': "Cuirass: ", 'value': instance.cuirass, 'field_key': 'cuirass'},            
            
            {'type': 'plain', 'label': "Iconography cuirass: ", 'value': instance.get_iconography(), 'field_key': 'iconography'},
            
            {'type': 'plain', 'label': "Heroic nudity: ", 'value': instance.heroic_semi_nude, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Enthroned: ", 'value': instance.seated, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Equestrian: ", 'value': instance.equestrian, 'field_key': 'cuirass'},
            
            {'type': 'plain', 'label': "Beard: ", 'value': instance.beard, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Paludamentum: ", 'value': instance.paludamentum, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Sword belt: ", 'value': instance.sword_belt, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Contabulata: ", 'value': instance.contabulata, 'field_key': 'cuirass'},

            {'type': 'plain', 'label': "Headgear: ", 'value': instance.headgear, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Corona laurea: ", 'value': instance.corona_laurea, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Corona civica: ", 'value': instance.corona_civica, 'field_key': 'cuirass'},
            {'type': 'plain', 'label': "Corona radiata: ", 'value': instance.corona_radiata, 'field_key': 'cuirass'},

            {'type': 'plain', 'label': "Other: ", 'value': instance.get_wreathcrown(), 'field_key': 'wreathcrown'},

            #TH: hier gaat er ook nog iets niet goed
            #{'type': 'plain', 'label': "Additional attributes: ", 'value': instance.get_attributes(), 'field_key': 'attributes'},

          

           # {'type': 'plain', 'label': "Province: ", 'value': instance.location.province.name,'field_key': 'province'},
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
        # Regel met plaatje, name empty, order idem, type str custom, zie onder custom: 'picture'
        {'name': 'Folder No', 'order': '', 'type': 'int', 'custom': 'picture', 'linkdetails': True},
        {'name': 'ID', 'order': 'o=1', 'type': 'int', 'field': 'origstr', 'linkdetails': True},
        {'name': 'Current location', 'order': 'o=2', 'type': 'str', 'field': 'name', 'linkdetails': True, 'main': True},
        {'name': 'Emperor', 'order': '', 'type': 'str', 'custom': 'emp_name'},
        {'name': 'Material', 'order': '', 'type': 'str', 'custom': 'mat_name'},
        {'name': 'Ancient city', 'order': '', 'type': 'str', 'custom': 'location'},        
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
                       
        if custom == "emp_name":            
            html = []
            html.append("<span>{}</span>".format(instance.emperor.name))  
            sBack = ", ".join(html)
        elif custom == "picture":            
            # Find number of folder
            # Find folder
            # Find first photo
            ext_list = ['jpg','jpeg','png']
            html = []
            for item in instance.portrait_photo.all():                
                # Find id of the corresponding photo folder
                folder = str(item.folder)  
                # Use that number to go to that folder in the MEDIA_DIR
                path = os.path.join(PICTURES_DIR, folder)
                # Make a list of all contents in the foldder
                photo_list = os.listdir(path)
                # Find out if there are items in the list
                if len(photo_list) > 0:
                    # Pick the first item of that list, let op, je hebt hier alleen de naam!
                    item_1 = photo_list[0]
                    # Now seek for way to access the photo... 
                    # use path and 
                    print(item_1)
                    # Split the file name up
                    item_1_list = item_1.split(".")
                    # Get extension part of the name of the image
                    ext = item_1_list[-1].lower()   

                    # Now check that the extension of the photograph Wat is het? Check extensie in lijst met acceptable extensies (te maken)
                    if ext in ext_list:                                      
                        # Try to find if the path to the first image of the portrait already exists in the Photo table:
                        path_test = item.path
                        # If there is no path to the first image in the database, the path should be created and added
                        if path_test == None or path_test =="": 
                            # This is the full path
                            path_test = os.path.join(path, item_1)

                            # We do not need the full path, only from /media onwards, split up                            
                            path_test_split = path_test.split("writable\\")
                                                                                   
                            # Grab the last part
                            path_temp = path_test_split[-1]

                            # Changes slashes to forward
                            path_final = path_temp.replace('\\', '/')

                            print(path_final)
                            
                            # Store the path in the db 
                            item.path = path_final 
                            item.save()
                                                                                                           
                        # single quote of class gebruiken in css, evt later               
                        html.append("<img src='/{}' style='max-width: 75px; width: auto; height: auto;'/>".format(item.path)) # ?? hier alleen maar parameters opgeven
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


