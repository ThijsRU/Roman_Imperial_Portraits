"""
Definition of views for the RIPD app.
"""

from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from datetime import datetime

from ripdapp.forms import SignUpForm

from ripdapp.models import Portrait, Emperor, Context, Location, Province, Material, PortraitMaterial, Arachne, \
    Wreathcrown, PortraitWreathcrown, Iconography, PortraitIconography, Type, PortraitType, Subtype, PortraitSubtype, \
    Alternative, PortraitAlternative, Recarved, PortraitRecarved, Together, PortraitTogether, Attributes, PortraitAttributes, \
    Iconography, PortraitIconography, Path, Photographer 

from Roman_Imperial_Portraits.settings import PICTURES_DIR

# Import Portrait Database Excel 

import io, sys, os
import openpyxl
from openpyxl.utils.cell import get_column_letter
from openpyxl.cell import Cell
from openpyxl import Workbook
from io import StringIO

import csv

import pandas as pd

from Roman_Imperial_Portraits.settings import MEDIA_DIR # ander niveau



def index(request):
    """Show the homepage"""

    assert isinstance(request, HttpRequest)

    # Specify the template
    template_name = "ripdapp/index.html"
    # Define the initial context
    context =  {'title':'Homepage',
                'year': datetime.now().year,
                'current_time': datetime.now().strftime("%A, %d %B, %Y at %X"),
                'pfx': '',
                'site_url': admin.site.site_url}
    # OLD CODE
    # now = datetime.now()
    #
    #html_content = "<html><head><title>Hello, Django</title></head><body>"
    #html_content += "<strong>Hello Django!</strong> on " + now.strftime("%A, %d %B, %Y at %X")
    #html_content += "</body></html>"

    #return HttpResponse(html_content)

    # Render and return the page
    return render(request, template_name, context)


def login_as_user(request, user_id):
    assert isinstance(request, HttpRequest)

    # Find out who I am
    supername = request.user.username
    super = User.objects.filter(username__iexact=supername).first()
    if super == None:
        return nlogin(request)

    # Make sure that I am superuser
    if super.is_staff and super.is_superuser:
        user = User.objects.filter(username__iexact=user_id).first()
        if user != None:
            # Perform the login
            login(request, user)
            return HttpResponseRedirect(reverse("home"))

    return home(request)

def nlogin(request):
    """Renders the not-logged-in page."""
    assert isinstance(request, HttpRequest)
    context =  {    'title':'Not logged in', 
                    'message':'Radboud University RIPD utility.',
                    'year': datetime.now().year,}

    return render(request,'nlogin.html', context)

def signup(request):
    """Provide basic sign up and validation of it """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the form
            form.save()
            # Create the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # also make sure that the user gets into the STAFF,
            #      otherwise he/she may not see the admin pages
            user = authenticate(username=username, 
                                password=raw_password,
                                is_staff=True)
            user.is_staff = True
            user.save()

            # Log in as the user
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def update_from_excel(request):
    """Check if contents can be updated from the MEDIA excel file"""
    
    # Maybe use empty db? Please view WRITABLE. "Trajan " and "Trajan" are both in the database.

    # Can only be done by a super-user
    if request.user.is_superuser:
        pass
    
    # Read the Excel file with pandas from MEDIA_DIR
   
    data_sam = os.path.abspath(os.path.join(MEDIA_DIR, 'database.xlsx'))
    df = pd.read_excel(data_sam, engine='openpyxl')

    # Replaces NaN with empty: ""
    df = df.fillna('')  

    # Create list with acceptable extensions for the images of the portraits
    ext_list = ['jpg','jpeg','png','JPG']

    # Iterate over all rows in the data frame
    for index, row in df.iterrows():
        print(row['ID'], row['Name'])
        
        orig = row['ID']
        name = row['Name']        
        start = row['Start_date']        
        end = row['End_date']  
        reason = row['Reason_for_dating']
        refs = row['Reference']        
        emperor = row['Emperor']
        context = row['Context']
        location = row['Place']         
        province = row['Province']

        # Coordinates
        coordinates = row['Coordinates']
        
        # Split up the coordinates
        if coordinates != None and coordinates !="":
            coord_list = coordinates.split(",")
            # Store separately
            lat = coord_list[0]
            long = coord_list[1]
        else:
            # in case of "Unknown"
            lat = ""
            long = ""
        
        # Portrait type
        porttype = row['Portrait_type']

        # Create empty list to store all portrait types
        # as there maybe more than one for some portraits
        # separate by a ";"        
        porttype_list = []    
           
        if porttype != None and porttype != "":
            if ";" in porttype: 
                porttype_list_temp = porttype.split(";")
                for porttype in porttype_list_temp:
                    porttype_list.append(porttype.strip())                
            else:
                porttype_list.append(porttype)
        
        # Alternative name
        alternative = row['Alternative_name'] 
     
        # Create empty list to store all alternative names
        # as there maybe more than one for some portraits
        # separate by a ";" 
        alternative_list = []    
           
        if alternative != None and alternative != "":
            if ";" in alternative: 
                alternative_list_temp = alternative.split(";")
                for alternative in alternative_list_temp:
                    alternative_list.append(alternative.strip())                
            else:
                alternative_list.append(alternative)
        
        # Subtype
        subtype = row['Subtype'] 

        # Create empty list to store all subtype items
        # as there maybe more than one for some portraits
        # separate by a ";" 
        subtype_list = []    
           
        if subtype != None and subtype != "":
            if ";" in subtype: 
                subtype_list_temp = subtype.split(";")
                for subtype in subtype_list_temp:
                    subtype_list.append(subtype.strip())                
            else:
                subtype_list.append(subtype)
        
        # Material
        material = row['Material'] 

        # Create empty list to store all materials 
        # as there maybe more than one for some portraits
        # separate by a ";" 
        material_list = []    
           
        if material != None and material != "":
            if ";" in material:
                material_list_temp = material.split(";")
                for material in material_list_temp:
                    material_list.append(material.strip())                
            else:
                material_list.append(material)
        
        # Arachne 
        arachne = row['Arachne_number']

        # Create empty list to store all Arachne id's 
        # as there maybe more than one for some portraits
        # separate by a ";" 
        arachne_list = []    
           
        if arachne != None and arachne != "":
            if ";" in str(arachne): # to make sure it is a string for now, view ID 3
                arachne_list_temp = arachne.split(";")
                for arachne in arachne_list_temp:
                    arachne_list.append(arachne.strip())                
            else:
                arachne_list.append(arachne)
        
        # LSA
        lsa = row['LSA_number']
        if lsa == "":
            lsa = None

        # Height
        height = row['Height']
        if height == "":
            height = None
        heightcom = row['Comment_on_height']
        
        # Group
        groupname = row['Name_group']
        groupref = row['Reference_statue_group']

        # Photo
        photo = row['PHOTO_ID']
        if photo != None and photo != "":
            photo = int(photo)

        # Paths
        path_list =[]
        
        # Note for possible future enhancements, if case there will be multiple photographers for 1 portrait, some
        # changes need to be made, for instance the name associated with each new photo will have to be stored and linked not
        # to a specific folder/portrait but to an specific photo. One way to do so is to make a spreadsheet with names and abbreviations
        # of the names of the photographers and add them to the END of each filename (and to the db table photographers) and retrieve 
        # the abbreviations from the filename within the process below, link the name to the abbreviations thus to the path of the new photo

        # TH: overwegen waard om dit alvast toch klaar te maken en te testen, bijvoorbeeld folder 467 from portrait 464

        # First make a string of the photo id (name folder)
        folder = str(photo)  
        # Use that string to go to that folder in the MEDIA_DIR and store the path        
        path = os.path.join(PICTURES_DIR, folder)
        # Make a list of all contents/images in that folder         
        photo_list = os.listdir(path)            
        # Find out if there is a photo available
        if len(photo_list) > 0:
            print(photo_list)
            for item in photo_list:
                # Split the file name up
                photo_split_list = item.split(".")                
                # Get extension part of the name of the image
                ext = photo_split_list[-1].lower()                    
                # Check that the extension of the photograph is in the list 
                if ext in ext_list:                                 
                    # Create the path of this image of this portrait
                    path_temp = os.path.join(path, item)                            
                    # We do not want to store the full path, only from /media onwards, 
                    # so path_temp needs to be split up                            
                    path_temp_split = path_temp.split("writable\\")
                    # Grab the last part
                    path_temp = path_temp_split[-1]
                    # Changes slashes to forward
                    path_final = path_temp.replace('\\', '/')
                    # Add the path to the list                               
                    path_list.append(path_final)

        print(path_list)     

        # Photographer
        photographer = row['Photo_by'] 
        
        # Other wreath or crown
        wreath = row['Other_wreath_or_crown']

        # Create empty list to store all other wreath or crown
        # as there maybe more than one for some portraits
        # separate by a ";" 
        wreath_list = []    
           
        if wreath != None and wreath != "":
            if ";" in wreath: 
                wreath_list_temp = wreath.split(";")
                for wreath in wreath_list_temp:
                    wreath_list.append(wreath.strip())                
            else:
                wreath_list.append(wreath)
        
        # Iconography on cuirass
        iconography = row['Iconography_cuirass']

        # Create empty list to store all other iconography items
        # as there maybe more than one for some portraits
        # separate by a ";" 
        iconography_list = []    
           
        if iconography != None and iconography != "":
            if ";" in iconography: 
                iconography_list_temp = iconography.split(";")
                for iconography in iconography_list_temp:
                    iconography_list.append(iconography.strip())                
            else:
                iconography_list.append(iconography)

        # Additional attributes
        attributes = row['Additional_attributes']

        # Create empty list to store all other iconography items
        # as there maybe more than one for some portraits
        # separate by a ";" 
        attributes_list = []    
           
        if attributes != None and attributes != "":
            if ";" in attributes: 
                attributes_list_temp = attributes.split(";")
                for attributes in attributes_list_temp:
                    attributes_list.append(attributes.strip())                
            else:
                attributes_list.append(attributes)

        # Recarved statue
        recarved = row['Recarved_statue']

        # Create empty list to store all other iconography items
        # as there maybe more than one for some portraits
        # separate by a ";" 
        recarved_list = []    
           
        if recarved != None and recarved != "":
            if ";" in recarved: 
                recarved_list_temp = recarved.split(";")
                for recarved in recarved_list_temp:
                    recarved_list.append(recarved.strip())                
            else:
                recarved_list.append(recarved)

        # Together with
        together = row['Together_with']

        # Create empty list to store all other together items
        # as there maybe more than one for some portraits
        # separate by a ";" 
        together_list = []    
           
        if together != None and together != "":
            if ";" in together: 
                together_list_temp = together.split(";")
                for together in together_list_temp:
                    together_list.append(together.strip())                
            else:
                together_list.append(together)
              
        # Boolean fields
        group = row['Part_of_statue_group']
        tantequem= row['Terminus_ante_quem']
        tpostquem= row['Terminus_post_quem']
        beard = row['Beard']	
        buste = row['Buste']	
        cuirabuste = row['Cuirassed_buste']	
        velato = row['Capite_velato']	
        headgear = row['Headgear']	
        laurea = row['Corona_laurea']	
        civica = row['Corona_civica']	
        radiata = row['Corona_radiata']	       
        statue = row['Statue']	
        toga = row['Toga']	
        equest = row['Equestrian']	
        cuira = row['Cuirass']	
        heroic = row['Heroic_semi_nude']	
        seated = row['Seated']		
        recarved = row['Recarved']		
        contabu = row['Contabulata']	
        swbelt = row['Sword_belt']	
        paluda = row['Paludamentum']	 
        miniat = row['Miniature']	
        recarv = row['Recarved']	
        iddisp = row['Identity_disputed']
         
       # Now alle fields from each record can be stored

        # Create a new portrait if there is a new one 
        port_obj = Portrait.objects.filter(origstr=orig).first()
        if port_obj == None:
            # Now we can create a completely fresh portrait 
            port_obj = Portrait.objects.create() 
            port_obj.origstr = orig
        
        # Store range of fields in Portrait table    
        # Maybe add folder of the photo's
        port_obj.name = name
        port_obj.startdate = start
        port_obj.enddate = end
        port_obj.reason_date = reason     
        port_obj.reference = refs
        port_obj.lsa = lsa
        port_obj.height = height
        port_obj.height_comment = heightcom
        port_obj.group_name = groupname
        port_obj.group_reference = groupref
            
        # Store Boolean fields in Portrait table
        port_obj.part_group = group            
        port_obj.terminus_ante_quem = tantequem
        port_obj.terminus_post_quem = tpostquem
        port_obj.beard = beard
        port_obj.buste = buste
        port_obj.cuirrassed_buste = cuirabuste
        port_obj.capite_velato = velato
        port_obj.headgear = headgear
        port_obj.corona_laurea = laurea
        port_obj.corona_civica = civica
        port_obj.corona_radiata = radiata
        port_obj.statue = statue
        port_obj.toga = toga
        port_obj.equestrian = equest
        port_obj.cuirass = cuira
        port_obj.heroic_semi_nude = heroic
        port_obj.seated = seated
        port_obj.recarvedboo = recarved
        port_obj.contabulata = contabu
        port_obj.sword_belt = swbelt
        port_obj.paludamentum = paluda
        port_obj.minitatue = miniat
        port_obj.recarved = recarv
        port_obj.disputed = iddisp
        
        # Emperor

        # Here the name of the emperor will be stored if the name does not yet exist
        # and a link will be made between the Portrait table and the Emperor table
            
        # Try to find if the name of the emperor already exists in the Emperor table:
        emperorfound = Emperor.objects.filter(name__iexact=emperor).first()
        if emperorfound == None:
                # If the name does not already exist, it needs to be added to the database
                emperor = Emperor.objects.create(name = emperor)
                # And a link should be made between this new emperor and the portrait
                port_obj.emperor = emperor
        else:
            # If the name of the emperor exists only a link should be made to this name from the Portrait table
            port_obj.emperor = emperorfound
            
        # Context

        # Here the name of the context will be stored if the name does not yet exist
        # and a link will be made between the Portrait table and the Context table            

        # First check if there is a context
        if context != None and context != "":
            # Try to find if the name of the context already exists in the Context table:
            contextfound = Context.objects.filter(name__iexact=context).first()
            if contextfound == None:
                # If the name does not already exist, it needs to be added to the database
                context = Context.objects.create(name = context)
                # And a link should be made between this new context and the portrait
                port_obj.context = context
            else:
                # If the name of the context exists only a link should be made to this name from the Portrait table
                port_obj.context = contextfound
        
       # Province
        if province != None and province != "":
            # Try to find if the name of the province already exists in the Province table:
            provincefound = Province.objects.filter(name__iexact=province).first()
            if provincefound == None:
                # If the name does not already exist, it needs to be added to the database
                province2 = Province.objects.create(name = province)
            else:
                province2 = provincefound
            
        # Location

        # Here the name of the location and its attributes will be stored if the name does not yet exist
        # and a link will be made between the Portrait table and the Location table        
        # Let op "Unknown"
            
        # Try to find if the name of the location already exists in the Location table:
        locationfound = Location.objects.filter(name__iexact=location).first()
        if locationfound == None:
            # If the name does not already exist, it needs to be added to the database and the coordinates if available also need to best
            if location == "Unknown" or lat == "":
                # In case the location is "Unknown" then there are no coordinates available
                location = Location.objects.create(name = location)
            else:                     
                # In other cases the coordinates should be known
                location = Location.objects.create(name = location, lat_coord = lat, long_coord = long, province=province2)
            # And a link should be made between this new location and the portrait
            port_obj.location = location
        else:
            # If the name of the location exists only a link should be made to this name from the Portrait table
            port_obj.location = locationfound
        
        # Photographer
        if photographer != None and photographer != "":
            # Try to find if the name of the photographer already exists in the Photographer table:
            grapherfound = Photographer.objects.filter(name__iexact=photographer).first()
            if grapherfound == None:
                # If the name does not already exist, it needs to be added to the database
                photographer2 = Photographer.objects.create(name = photographer)
            else:
                photographer2 = grapherfound

                       
        # Arachne
        if arachne_list != "":
            for arachne in arachne_list:  
                # Try to find if the id of the arachne already exists in the Arachne table:
                arachnefound = Arachne.objects.filter(arachne__iexact=arachne).first()
                if arachnefound == None:
                    # If the id does not already exist, it needs to be added to the database
                    # And a link should be made between this new arachne code and the corresponding portrait id
                    Arachne.objects.create(arachne = arachne, portrait = port_obj)
                        
                else:
                    pass 
        
        # Path
        if path_list != "": 
            for path in path_list:  
                # Try to find if the id of the path already exists in the Path table:
                pathfound = Path.objects.filter(path__iexact=path).first()
                if pathfound == None:
                    print(pathfound)
                    # If the id does not already exist, it needs to be added to the database
                    # And a link should be made between this new path  and the corresponding portrait id
                    if photographer != None and photographer != "":   
                        Path.objects.create(path = path, portrait = port_obj, folder = folder, photographer = photographer2)
                    else:
                        Path.objects.create(path = path, portrait = port_obj, folder = folder)                           

                else:
                    pass 
                        
        # Material
        if material_list != "":
            for material in material_list:  
                # Try to find if the name of the material already exists in the Material table:
                materialfound = Material.objects.filter(name__iexact=material).first()
                if materialfound == None:
                    # If the name does not already exist, it needs to be added to the database
                    material = Material.objects.create(name = material)
                    # And a link should be made between this new material and corresponding Portrait table
                    PortraitMaterial.objects.create(portrait = port_obj, material = material)
                else:
                    # In case there is a materialfound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a portrait and a material
                    portmtrllink = PortraitMaterial.objects.filter(portrait = port_obj, material = materialfound).first()
                    if portmtrllink == None:
                        # If the material already exists, but not the link, than only a link should be 
                        # made between portrait and the material
                        PortraitMaterial.objects.create(portrait = port_obj, material = materialfound)
            
        # Other wreath and crown (view Material)
        if wreath_list != "":
            for wreath in wreath_list:  
                # Try to find if the name of the wreath already exists in the Wreathcrown table:
                wreathfound = Wreathcrown.objects.filter(name__iexact=wreath).first()
                if wreathfound == None:
                    # If the name does not already exist, it needs to be added to the database
                    wreath = Wreathcrown.objects.create(name = wreath)
                    # And a link should be made between this new wreath and corresponding portrait id
                    PortraitWreathcrown.objects.create(portrait = port_obj, wreathcrown = wreath)
                else:
                    # In case there is a wreathfound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a wreath and a portrait
                    portwreathlink = PortraitWreathcrown.objects.filter(portrait = port_obj, wreathcrown = wreathfound).first()
                    if portwreathlink == None:
                        # If the wreath already exists, but not the link, than only a link should be 
                        # made between portrait and the wreath
                        PortraitWreathcrown.objects.create(portrait = port_obj, wreathcrown = wreathfound)
     
        # Portrait Type
        if porttype_list != "":
            for ptype in porttype_list:  
                # Try to find if the name of the type already exists in the Type table:
                ptypefound = Type.objects.filter(name__iexact=ptype).first()
                if ptypefound == None:
                    # If the name does not already exist, it needs to be added to the database
                    ptype = Type.objects.create(name = ptype)
                    # And a link should be made between this new type and corresponding portrait id
                    PortraitType.objects.create(portrait = port_obj, type = ptype)
                else:
                    # In case there is a ptypefound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a type and a portrait
                    porttypelink = PortraitType.objects.filter(portrait = port_obj, type = ptypefound).first()
                    if porttypelink == None:
                        # If the type already exists, but not the link, than only a link should be 
                        # made between portrait and the type
                        PortraitType.objects.create(portrait = port_obj, type = ptypefound)
        
        # Alternative name
        if alternative_list != "":
            for altname in alternative_list:  
                # Try to find if the alternative name already exists in the Alternative table:
                altnamefound = Alternative.objects.filter(name__iexact=altname).first()
                if altnamefound == None:
                    # If the name does not already exist, it needs to be added to the database
                    alternative = Alternative.objects.create(name = altname)
                    # And a link should be made between this new alternative name and corresponding portrait id
                    PortraitAlternative.objects.create(portrait = port_obj, alternative = alternative)
                else:
                    # In case there is a altnamefound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a alternative name and a portrait
                    altnamelink = PortraitAlternative.objects.filter(portrait = port_obj, alternative = altnamefound).first()
                    if altnamelink == None:
                        # If the alternative name already exists, but not the link, than only a link should be 
                        # made between portrait and the alternative name
                        PortraitAlternative.objects.create(portrait = port_obj, alternative = altnamefound)

        # Subtype 
        if subtype_list != "":
            for subtype in subtype_list:  
                # Try to find if the name of the subtype already exists in the Subtype table:
                subtypefound = Subtype.objects.filter(name__iexact=subtype).first()
                if subtypefound == None:
                    # If the name does not already exist, it needs to be added to the database
                    subtype = Subtype.objects.create(name = subtype)
                    # And a link should be made between this new subtype and corresponding portrait id
                    PortraitSubtype.objects.create(portrait = port_obj, subtype = subtype)
                else:
                    # In case there is a subtypefound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a subtype and a portrait
                    subtypelink = PortraitSubtype.objects.filter(portrait = port_obj, subtype = subtypefound).first()
                    if subtypelink == None:
                        # If the subtype already exists, but not the link, than only a link should be 
                        # made between portrait and the subtype
                        PortraitSubtype.objects.create(portrait = port_obj, subtype = subtypefound)
        
        # Recarved
        if recarved_list != "":
            for recarv in recarved_list:  
                # Try to find if the name of the recarved already exists in the Recarved table:
                recarvfound = Recarved.objects.filter(name__iexact=recarv).first()
                if recarvfound == None:
                    # If the name does not already exist, it needs to be added to the database
                    recarved = Recarved.objects.create(name = recarv)
                    # And a link should be made between this new recarved item and corresponding portrait id
                    PortraitRecarved.objects.create(portrait = port_obj, recarved = recarved)
                else:
                    # In case there is a recarvfound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a recarved item and a portrait
                    recarvedlink = PortraitRecarved.objects.filter(portrait = port_obj, recarved = recarvfound).first()
                    if recarvedlink == None:
                        # If the recarved item already exists, but not the link, than only a link should be 
                        # made between portrait and the recarved item
                        PortraitRecarved.objects.create(portrait = port_obj, recarved = recarvfound)
        
        # Together with
        if together_list != "":
            for togeth in together_list:  
                # Try to find if the name of the together item already exists in the Together table:
                togethfound = Together.objects.filter(name__iexact=togeth).first()
                if togethfound == None:
                    # If the name does not already exist, it needs to be added to the database
                    together = Together.objects.create(name = togeth)
                    # And a link should be made between this new recarved item and corresponding portrait id
                    PortraitTogether.objects.create(portrait = port_obj, together = together)
                else:
                    # In case there is a togethfound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a recarved item and a portrait
                    togethlink = PortraitTogether.objects.filter(portrait = port_obj, together = togethfound).first()
                    if togethlink == None:
                        # If the recarved item already exists, but not the link, than only a link should be 
                        # made between portrait and the recarved item
                        PortraitTogether.objects.create(portrait = port_obj, together = togethfound)
        
        # Attributes
        if attributes_list != "":
            for attrib in attributes_list:  
                # Try to find if the name of the attribute already exists in the Attributes table:
                attribfound = Attributes.objects.filter(name__iexact=attrib).first()
                if attribfound == None:
                    # If the name does not already exist, it needs to be added to the database
                    attribute = Attributes.objects.create(name = attrib)
                    # And a link should be made between this new attribute and corresponding portrait id
                    PortraitAttributes.objects.create(portrait = port_obj, attribute = attribute)
                else:
                    # In case there is a attribfound, check for a link, if so, nothing should happen, 
                    # than there is already a link between an attribute and a portrait
                    attriblink = PortraitAttributes.objects.filter(portrait = port_obj, attribute = attribfound).first()
                    if attriblink == None:
                        # If the atribute already exists, but not the link, than only a link should be 
                        # made between portrait and the atribute
                        PortraitAttributes.objects.create(portrait = port_obj, attribute = attribfound)
        
        # Iconography
        if iconography_list != "":
            for icono in iconography_list:  
                # Try to find if the name of the iconography already exists in the Wreathcrown table:
                iconofound = Iconography.objects.filter(name__iexact=icono).first()
                if iconofound == None:
                    # If the name does not already exist, it needs to be added to the database
                    iconography = Iconography.objects.create(name = icono)
                    # And a link should be made between this new iconography item and corresponding portrait id
                    PortraitIconography.objects.create(portrait = port_obj, iconography = iconography)
                else:
                    # In case there is a iconofound, check for a link, if so, nothing should happen, 
                    # than there is already a link between a iconography item and a portrait
                    iconolink = PortraitIconography.objects.filter(portrait = port_obj, iconography = iconofound).first()
                    if iconolink == None:
                        # If the iconography item already exists, but not the link, than only a link should be 
                        # made between portrait and the iconography item
                        PortraitIconography.objects.create(portrait = port_obj, iconography = iconofound)

      # Save the results
        port_obj.save()
    
    # What we return is simply the home page
    return redirect('home')

