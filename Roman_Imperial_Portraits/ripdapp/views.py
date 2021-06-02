"""
Definition of views for the RIPD app.
"""

from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from datetime import datetime

from ripdapp.models import Portrait, Emperor, Context, Location, Province
from ripdapp.forms import SignUpForm

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
    context =  {'title':'RIPD',
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
    
    # Can only be done by a super-user
    if request.user.is_superuser:
        pass
    
    # Read
        
    # Misschien pandas gebruiken?
    #filename = os.path.abspath(os.path.join(MEDIA_DIR, 'portraits_database.xlsx'))
    #tmp_path = os.path.abspath(os.path.join(MEDIA_DIR, filename))
    df = pd.read_excel(r'D:/Database.xlsx', engine='openpyxl')
    # Replaces NaN with empty: ""
    df = df.fillna('')  
    
    print (df)

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
        coordinates = row['Coordinates']
        print(coordinates)

        # First split up coördinates
        if coordinates != None and coordinates !="":
            coord_list = coordinates.split(",")
            lat = coord_list[0]
            long = coord_list[1]
            print(lat, long)

        else:
            # in case of "Unknown":
            lat = ""
            long = ""


        arachne = row['Arachne_number'] # process later
        
        lsa = row['LSA_number']
        if lsa == "":
            lsa = None
        
        height = row['Height']
        if height == "":
            height = None

        heightcom = row['Comment_on_height']
        group = row['Name_group']
        groupref = row['Reference_statue_group']
        
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
        relief = row['Relief']		
        recarved = row['Recarved']		
        contabu = row['Contabulata']	
        swbelt = row['Sword_belt']	
        paluda = row['Paludamentum']	 
        miniat = row['Miniature']	
        recarv = row['Recarved']	
        iddisp = row['Identity_disputed']
            
        # eerst iets gaan bouwen dat alles verwijderd wat aan een reeds ingelezen portrait is gerelateerd, 
        # id db graag behouden, zie A+M deletables verhaal!

        # Now we can create a completely fresh portrait record
        # Wissen oude, zie eigen werk dit klopt nog niet hoor
        port_obj = Portrait.objects.create() 
        # port_obj.idno = portid ergens gaat er iets mis met een float? Check Excel en CSV
        if name != None and name != "":            
            
            # Store original id
            port_obj.origstr = orig            
            port_obj.name = name
            
            port_obj.startdate = start
            port_obj.enddate = end
            
            port_obj.reference = refs
            
           # port_obj.arachne = arachne
            port_obj.lsa = lsa

            port_obj.height = height
            port_obj.height_comment = heightcom

            port_obj.group_name = group
            port_obj.group_reference = groupref
            
            # Boolean fields
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
            port_obj.relief = relief
            port_obj.recarved = recarved
            port_obj.contabulata = contabu
            port_obj.sword_belt = swbelt
            port_obj.paludamentum = paluda
            port_obj.minitatue = miniat
            port_obj.recarved = recarv
            port_obj.disputed = iddisp

            # Emperors

            # Here the name of the emperor will be stored if the name does not yet exist
            # and a link will be made between the Portrait table and the Emperor table
                        
            # eerst laten opzoeken 1030 checken met het verwijderen van alle gerelateerde gegevens tzt
            
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
                # emp = Emperor.objects.create(name = emperor) # Ok, komt er in maar hoe id ook alweer te gebruiken voor Portrait?
            
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
            # Province, zie example PASSIM?
            
             # First check if there is a province misschien dit erin zetten
            if province != None and province != "":
                # Try to find if the name of the province already exists in the Province table:
                provincefound = Province.objects.filter(name__iexact=province).first()
                if provincefound == None:
                    # If the name does not already exist, it needs to be added to the database
                    # and later on to the location table
                    province = Province.objects.create(name = province)
                # Hier onduidelijk lijkt voor een deel te werken.                 
                else:
                    # If the name of the province exists only a link should be made to this name from the Location table
                    province = provincefound    


            # Location

            # Here the name of the location and its attributes will be stored if the name does not yet exist
            # and a link will be made between the Portrait table and the Location table        
            # Let op "Unknown"
            
            # Try to find if the name of the location already exists in the Location table:
            locationfound = Location.objects.filter(name__iexact=location).first()
            if locationfound == None:
                # If the name does not already exist, it needs to be added to the database and the coordinates if available also need to best
                if location == "Unknown":
                    # In case the location is "Unknown" then there are no coordinates available
                    location = Location.objects.create(name = location)
                else:                     
                    # In other cases the coordinates should be known
                    location = Location.objects.create(name = location, lat_coord = lat, long_coord = long, province=province)
                # And a link should be made between this new location and the portrait
                port_obj.location = location
            else:
                # If the name of the location exists only a link should be made to this name from the Portrait table
                port_obj.location = locationfound

            

      # Save the results
        port_obj.save()
    #with open('d:\database.csv', 'r') as f: #, encoding='utf-8'
     #   reader = csv.reader(f, dialect='excel', delimiter='\t')
      #  rowDataList = list(reader)
       # for row in rowDataList:
        #    for col in row:
         #       print(col)
    # https://github.com/ErwinKomen/RU-passim/blob/master/passim/passim/reader/views.py
    # https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    # ID
    # Portrait zoals Manuscript?

    

        

    # class ManuscriptUploadExcel(ReaderImport):
    # Let op: views.py reader PASSIM https://github.com/ErwinKomen/RU-passim/blob/master/passim/passim/reader/excel.py



    # What we return is simply the home page
    return redirect('home')

