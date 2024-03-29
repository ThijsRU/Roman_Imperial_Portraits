"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelMultipleChoiceField, ModelChoiceField
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget, Select2MultipleWidget
from ripdapp.models import *
from basic.utils import ErrHandle

# ==================== Forms related to authentication =====================================

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                widget=forms.TextInput({'class': 'form-control','placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                widget=forms.PasswordInput({'class': 'form-control','placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


# ==================== FORMS RELATED TO VIEWSBASIC =========================================

class OrigIDWidget(ModelSelect2MultipleWidget):
    model = Portrait
    search_fields = [ 'origstr__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.origstr

    def get_queryset(self):
        qs = Portrait.objects.all().order_by('origstr').distinct()
        return qs

class NameWidget(ModelSelect2MultipleWidget):
    model = Portrait
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Portrait.objects.all().order_by('name').distinct()
        return qs

class PortraitOneWidget(ModelSelect2Widget):
    model = Portrait
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Portrait.objects.all().order_by('name').distinct()
        return qs

class PhotographerOneWidget(ModelSelect2Widget):
    model = Photographer
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Photographer.objects.all().order_by('name').distinct()
        return qs

class EmperorWidget(ModelSelect2MultipleWidget):
    model = Emperor
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Emperor.objects.all().order_by('name').distinct()
        return qs

class MaterialWidget(ModelSelect2MultipleWidget):
    model = Material
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self): # werkt niet       
        qs = Material.objects.all().order_by('name').distinct() 
        return qs

class ProvinceWidget(ModelSelect2MultipleWidget):
    model = Province
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Province.objects.all().order_by('name')     
        return qs

class AncientLocationWidget(ModelSelect2MultipleWidget):
    model = Location 
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Location.objects.all().order_by('name')    
        return qs

class CurrentLocationWidget(ModelSelect2MultipleWidget):
    model = CurrentLocation 
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = CurrentLocation.objects.all().order_by('name')    
        return qs

class ContextWidget(ModelSelect2MultipleWidget):
    model = Context
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):        
        qs = Context.objects.all().order_by('name')        
        return qs

class RecarvedWidget(ModelSelect2MultipleWidget):
    model = Recarved
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):        
        qs = Recarved.objects.all().order_by('name')        
        return qs

class IconWidget(ModelSelect2MultipleWidget):
    model = Iconography
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):        
        qs = Iconography.objects.all().order_by('name')        
        return qs

class AttributeWidget(ModelSelect2MultipleWidget):
    model = Attributes
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):        
        qs = Attributes.objects.all().order_by('name')        
        return qs

class WreathWidget(ModelSelect2MultipleWidget):
    model = Wreathcrown
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):        
        qs = Wreathcrown.objects.all().order_by('name')        
        return qs

class ReferencesWidget(ModelSelect2MultipleWidget):
    model = Portrait
    search_fields = [ 'reference__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.reference

    def get_queryset(self):   
        qs = Portrait.objects.exclude(reference__exact='').order_by('reference')      
        return qs

# Model PathPhoto:
#class PhotoNameWidget(ModelSelect2MultipleWidget):
#    model = Path
#    search_fields = [ 'path__icontains' ]
   
#    def label_from_instance(self, obj): # HIER moet wat aangepast worden, kan dat? HEbben we de name nodig??
#        return obj.folder

#    def get_queryset(self):
#        qs = Path.objects.all().order_by('folder').distinct()
#        return qs

class FolderWidget(ModelSelect2MultipleWidget):
    model = Path
    search_fields = [ 'folder__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.folder

    def get_queryset(self):
        qs = Path.objects.all().order_by('folder').distinct()
        return qs

class PathIDWidget(ModelSelect2MultipleWidget):
    model = Path
    search_fields = [ 'id__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.id

    def get_queryset(self):
        qs = Path.objects.all().order_by('id').distinct()
        return qs

class PathWidget(ModelSelect2MultipleWidget):
    model = Path
    search_fields = [ 'path__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.path

    def get_queryset(self):
        qs = Path.objects.all().order_by('path').distinct()
        return qs




# Model Photographer:

class PhotographerWidget(ModelSelect2MultipleWidget):
    model = Photographer
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):        
        qs = Photographer.objects.all().order_by('name')        
        return qs


class PhotographerForm(forms.ModelForm):
    """One form to handle the Photographer searching and details view""" 

    phgrname = forms.CharField(label="Photographer", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching photographer input-sm', 'placeholder': 'Name of the photographer...',  'style': 'width: 77%;'}))
    
    phgrlist = ModelMultipleChoiceField(queryset=None, required=False, 
                                widget=PhotographerWidget(attrs={'data-placeholder': 'Select multiple photographers...', 'style': 'width: 77%;', 'class': 'searching'}))
    
    class Meta:
        ATTRS_FOR_FORMS = {'class': 'form-control'};

        model = Photographer
        fields = ['id', 'name'] 
        widgets={'name': forms.TextInput(attrs={'placeholder': 'Name of the Photographer...', 'style': 'width: 77%;', 'class': 'searching'}),
                 'id':   forms.TextInput(attrs={'placeholder': 'Id of the photographer...', 'style': 'width: 100%;'}),                  
                 }

    def __init__(self, *args, **kwargs):
        # Start by executing the standard handling
        super(PhotographerForm, self).__init__(*args, **kwargs)
        oErr = ErrHandle()
        try:
            # Set other parameters            
            #self.fields['id'].required = False #gaat mis
            self.fields['name'].required = False # gaat goed            
            self.fields['phgrlist'].queryset = Photographer.objects.all().order_by('id') # gaat ook goed
               
            # Get the instance, moet ik hier meer mee doen?
            if 'instance' in kwargs:
                instance = kwargs['instance']                            
                
        except:
            msg = oErr.get_error_message()
            oErr.DoError("PhotographerForm")

        # Return the response
        return None

# AANPASSEN!!!

class PhotoPathForm(forms.ModelForm):
    """One form to handle the PhotoPath searching and details view""" 

    name = forms.CharField(label="Photo name", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the photo...',  'style': 'width: 100%;'}))

    photoname = forms.CharField(label="Photo name", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the photo...',  'style': 'width: 100%;'}))

    photo_path = forms.CharField(label="Photo path", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the path...',  'style': 'width: 100%;'}))
    
    origstr = forms.CharField(label="RIPD id", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching photographer input-sm', 'placeholder': 'ID of the path...',  'style': 'width: 77%;'}))
        
    pathid = forms.CharField(label="Path ID", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching photographer input-sm', 'placeholder': 'ID of the path...',  'style': 'width: 77%;'}))

    phidlist = ModelMultipleChoiceField(queryset=None, required=False, 
                                widget=PathIDWidget(attrs={'data-placeholder': 'Select multiple photographers...', 'style': 'width: 77%;', 'class': 'searching'}))
       
    #phnamelist = ModelMultipleChoiceField(queryset=None, required=False, 
    #                                widget=PhotoNameWidget(attrs={'data-placeholder': 'Select multiple names of photos...', 'style': 'width: 77%;', 'class': 'searching'}))

    pathname = forms.CharField(label="Path name", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching photographer input-sm', 'placeholder': 'Path of the photo...',  'style': 'width: 77%;'}))

    phpathlist = ModelMultipleChoiceField(queryset=None, required=False, 
                                widget=PathWidget(attrs={'data-placeholder': 'Select multiple paths of photos...', 'style': 'width: 77%;', 'class': 'searching'}))

    folder = forms.CharField(label="Folder of the photo", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching photographer input-sm', 'placeholder': 'Number of the folder...',  'style': 'width: 77%;'}))

    phfolderlist = ModelMultipleChoiceField(queryset=None, required=False, 
                                widget=FolderWidget(attrs={'data-placeholder': 'Select multiple photo folder...', 'style': 'width: 77%;', 'class': 'searching'}))

    ## Portrait part
    origidlist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=OrigIDWidget(attrs={'data-placeholder': 'Select multiple original ids...', 'style': 'width: 77%;', 'class': 'searching'})) 

    namelist  = ModelMultipleChoiceField(queryset=None, required=False, 
                widget=NameWidget(attrs={'data-placeholder': 'Select location, museum and number...', 'style': 'width: 77%;', 'class': 'searching'}))
       
    ## Photographer part
    phgrname = forms.CharField(label="Photographer", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching photographer input-sm', 'placeholder': 'Name of the photographer...',  'style': 'width: 77%;'}))
    
    phgrlist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=PhotographerWidget(attrs={'data-placeholder': 'Select multiple photographers...', 'style': 'width: 77%;', 'class': 'searching'}))

    # =========== PhotoPath-specific ===========================

    class Meta:
        ATTRS_FOR_FORMS = {'class': 'form-control'};

        model = Path
        fields = ['id', 'path'] # , 'folder'
        widgets={'id':   forms.TextInput(attrs={'placeholder': 'Id of the photo/path...', 'style': 'width: 77%;'}),                  
                 'path':  forms.TextInput(attrs={'placeholder': 'Path of the photo...', 'style': 'width: 77%;'}),                  
                 'folder': forms.TextInput(attrs={'placeholder': 'Folder of the photo...', 'style': 'width: 77%;'}),                  
                 }

    def __init__(self, *args, **kwargs):
        # Start by executing the standard handling
        super(PhotoPathForm, self).__init__(*args, **kwargs)
        oErr = ErrHandle()
        try:
            # Set other parameters              
            self.fields['path'].required = False #gaat mis ok dit is ook die regel, en waarom gaat het mis?
                        
            # Path
            self.fields['phpathlist'].queryset = Path.objects.all().order_by('id')   # wordt niks opgepikt         
            self.fields['phidlist'].queryset = Path.objects.all().order_by('id')   # wordt niks opgepikt         
            self.fields['phfolderlist'].queryset = Path.objects.all().order_by('folder')
            
            # Portrait
            self.fields['origidlist'].queryset = Portrait.objects.all().order_by('origstr')
            self.fields['namelist'].queryset = Portrait.objects.all().order_by('name')            
            
            # Photographer
            self.fields['phgrlist'].queryset = Photographer.objects.all().order_by('name')

            # Get the instance, moet ik hier meer mee doen?
            if 'instance' in kwargs:
                instance = kwargs['instance']                            
                
        except:
            msg = oErr.get_error_message()
            oErr.DoError("PhotoPathForm")

        # Return the response
        return None


class AddPhotoForm(forms.ModelForm):
    # Field to upload a file with the picture
    picfile = forms.FileField(label="Select the picture file to be uploaded", required=False,
                              widget=forms.ClearableFileInput(attrs={'multiple': False}))
    
    class Meta:
        ATTRS_FOR_FORMS = {'class': 'form-control'};

        model = Path
        fields = ['id', 'portrait', 'photographer'] # , 'folder'
        widgets={'id':   forms.TextInput(attrs={'placeholder': 'Id of the photo/path...', 'style': 'width: 77%;'}),   
                 'portrait': PortraitOneWidget(attrs={'data-placeholder': 'Select a portrait...', 'style': 'width: 77%;', 'class': 'searching'}),
                 'photographer': PhotographerOneWidget(attrs={'data-placeholder': 'Select a photographer...', 'style': 'width: 77%;', 'class': 'searching'}),
                 # folder?
                 }

    def __init__(self, *args, **kwargs):
        # Start by executing the standard handling
        super(AddPhotoForm, self).__init__(*args, **kwargs)
        oErr = ErrHandle()
        try:

            self.fields['portrait'].required = False
            self.fields['photographer'].required = False

            #self.fields['folder'].required = False

            # Get the instance, moet ik hier meer mee doen?
            if 'instance' in kwargs:
                instance = kwargs['instance']   

                self.fields['portrait'].initial = instance.portrait
                self.fields['portrait'].queryset = Portrait.objects.filter(id=instance.portrait.id)

                #self.fields['folder'].queryset = Portrait.objects.filter(id=instance.portrait.id)
                
        except:
            msg = oErr.get_error_message()
            oErr.DoError("AddPhotoForm")

        # Return the response
        return None

  
class PortraitForm(forms.ModelForm):
    """One form to handle the Portrait searching and details view"""  
    
    origidlist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=OrigIDWidget(attrs={'data-placeholder': 'Select multiple original ids...', 'style': 'width: 77%;', 'class': 'searching'})) 

    empname = forms.CharField(label="Emperor", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 77%;'}))
    
    date_from   = forms.IntegerField(label=_("Date start"), required = False,
                widget=forms.TextInput(attrs={'placeholder': _('Starting from (year)...'),  'style': 'width: 100%;', 'class': 'searching'}))
    
    date_until  = forms.IntegerField(label=_("Date until"), required = False,
                widget=forms.TextInput(attrs={'placeholder': _('Until (year)...'),  'style': 'width: 100%;', 'class': 'searching'}))

    ####### These are added because there need to be a 'fieldkey' viewsbasic.py
    material = forms.CharField(label="Material", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))    
    height = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))    
    height_comment = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))    
    miniature = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    location = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    province = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))    
    context = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    part_statue_group = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    group_name = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    together = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    group_reference = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))    
    photo_folder = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    
    photographer = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the photographer...',  'style': 'width: 100%;'}))
    
    photo_path = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    
    recarvedstatue = forms.CharField(label="Height", required=False, 
                             widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))

    #####

    namelist  = ModelMultipleChoiceField(queryset=None, required=False, 
                widget=NameWidget(attrs={'data-placeholder': 'Select location, museum and number...', 'style': 'width: 77%;', 'class': 'searching'}))
   
    emplist = ModelMultipleChoiceField(queryset=None, required=False, 
              widget=EmperorWidget(attrs={'data-placeholder': 'Select multiple emperors...', 'style': 'width: 77%;', 'class': 'searching'}))
        
    matlist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=MaterialWidget(attrs={'data-placeholder': 'Select multiple materials...', 'style': 'width: 77%;', 'class': 'searching'}))  
    
    recarvedlist = ModelMultipleChoiceField(queryset=None, required=False, 
                                widget=RecarvedWidget(attrs={'data-placeholder': 'Select context(s)...', 'style': 'width: 77%;', 'class': 'searching'}))
               
    locname = forms.CharField(label="Location", required=False, 
                              widget=forms.TextInput(attrs={'class': 'typeahead searching locations input-sm', 'placeholder': 'Name of the ancient city...',  'style': 'width: 100%;'}))
    
    ancloclist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=AncientLocationWidget(attrs={'data-placeholder': 'Select multiple names of ancient cities...', 'style': 'width: 77%;', 'class': 'searching'}))
        
    curlocname = forms.CharField(label="Location", required=False, 
                              widget=forms.TextInput(attrs={'class': 'typeahead searching current locations input-sm', 'placeholder': 'Name of the current location...',  'style': 'width: 100%;'}))
    
    curloclist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=CurrentLocationWidget(attrs={'data-placeholder': 'Select multiple current locations...', 'style': 'width: 77%;', 'class': 'searching'}))
                    
    provlist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=ProvinceWidget(attrs={'data-placeholder': 'Select multiple provinces...', 'style': 'width: 77%;', 'class': 'searching'}))
      
    contlist = ModelMultipleChoiceField(queryset=None, required=False, 
                                widget=ContextWidget(attrs={'data-placeholder': 'Select multiple contexts...', 'style': 'width: 77%;', 'class': 'searching'}))
        
    iconlist = ModelMultipleChoiceField(queryset=None, required=False, 
              widget=IconWidget(attrs={'data-placeholder': 'Select multiple icons...', 'style': 'width: 77%;', 'class': 'searching'}))
        
    attrlist = ModelMultipleChoiceField(queryset=None, required=False, 
                                widget=AttributeWidget(attrs={'data-placeholder': 'Select multiple attributes...', 'style': 'width: 77%;', 'class': 'searching'}))
        
    wreathlist = ModelMultipleChoiceField(queryset=None, required=False, 
              widget=WreathWidget(attrs={'data-placeholder': 'Select multiple wreaths or crowns...', 'style': 'width: 77%;', 'class': 'searching'}))
    
    arachid = forms.CharField(label="Arachne", required=False, 
                              widget=forms.TextInput(attrs={'class': 'typeahead searching arachne input-sm', 'placeholder': 'Arachne id of the portrait...',  'style': 'width: 100%;'}))
    
    lsaid = forms.CharField(label="LSA", required=False, 
                              widget=forms.TextInput(attrs={'class': 'typeahead searching arachne input-sm', 'placeholder': 'LSA id of the portrait...',  'style': 'width: 100%;'}))
    

    # Werkt nog niet goed, EK vragen. Sowieso moeten de lege niet getoond worden.
    referenceslist = ModelMultipleChoiceField(queryset=None, required=False, 
              widget=ReferencesWidget(attrs={'data-placeholder': 'Select multiple references...', 'style': 'width: 77%;', 'class': 'searching'}))
    
    # This is to circumvent the standard filter option for the Booleans: False
    disputed_free = forms.NullBooleanField()
    disputed = disputed_free
    
    buste_free = forms.NullBooleanField()
    buste = buste_free

    statue_free = forms.NullBooleanField()
    statue = statue_free

    equestrian_free = forms.NullBooleanField()
    equestrian = equestrian_free

    beard_free = forms.NullBooleanField()
    beard = beard_free

    part_group_free = forms.NullBooleanField()
    part_group = part_group_free
    
    recarvedboo_free = forms.NullBooleanField()
    recarvedboo = recarvedboo_free
    
    toga_free = forms.NullBooleanField()
    toga = toga_free

    cuirass_free = forms.NullBooleanField()
    cuirass = cuirass_free 
    
    heroic_semi_nude_free = forms.NullBooleanField()
    heroic_semi_nude = heroic_semi_nude_free

    seated_free = forms.NullBooleanField()
    seated = seated_free

    paludamentum_free = forms.NullBooleanField()
    paludamentum = paludamentum_free

    sword_belt_free = forms.NullBooleanField()
    sword_belt = sword_belt_free

    contabulata_free = forms.NullBooleanField()
    contabulata = contabulata_free

    headgear_free = forms.NullBooleanField()
    headgear = headgear_free

    capite_velato_free = forms.NullBooleanField()
    capite_velato = capite_velato_free

    corona_laurea_free = forms.NullBooleanField()
    corona_laurea = corona_laurea_free

    corona_civica_free = forms.NullBooleanField()
    corona_civica = corona_civica_free

    corona_radiata_free = forms.NullBooleanField()
    corona_radiata = corona_radiata_free
    
    # =========== Portrait-specific ===========================
    
    class Meta:
        ATTRS_FOR_FORMS = {'class': 'form-control'};

        model = Portrait
        fields = ['name', 'origstr',  'startdate', 'enddate', 'reference', 'lsa'] # eea lijkt te werken
        widgets={'name':             forms.TextInput(attrs={'placeholder': 'Modern location, museum or inventory number', 'style': 'width: 100%;', 'class': 'searching'}),
                 'origstr':          forms.TextInput(attrs={'placeholder': 'Original id of the portrait...', 'style': 'width: 100%;'}),
                 'startdate':        forms.TextInput(attrs={'placeholder': 'Earliest possible year...','style': 'width: 20%;'}), 
                                                          # aan te passen, "vanaf een jaar" dus de input dient als startpunt om te bepalen
                                                          # vanaf welk jaartal de portraits meegenomen moeten worden, dus "50" is alles vanaf 50
                                                          # range of years, SelectDateWidget? Date Range in Passim?
                 'enddate':          forms.TextInput(attrs={'placeholder': 'Latest possible year...','style': 'width: 20%;'}), 
                 'reference':        forms.TextInput(attrs={'placeholder': 'Reference contains...', 'style': 'width: 100%;'}),                 
                 'lsa':              forms.TextInput(attrs={'placeholder': 'LSA id of the portrait...', 'style': 'width: 77%;'}),
                 'arachne':         forms.TextInput(attrs={'placeholder': 'Arachne id of the portrait...', 'style': 'width: 100%;'}), 
                 } 

    def __init__(self, *args, **kwargs):
        # Start by executing the standard handling
        super(PortraitForm, self).__init__(*args, **kwargs)
        oErr = ErrHandle()
        try:
            # Set other parameters            
            self.fields['name'].required = False                        
            self.fields['disputed_free'].required = None
            self.fields['part_group_free'].required = None
            self.fields['buste_free'].required = None
            self.fields['recarvedboo_free'].required = None
            self.fields['startdate'].required = False
            self.fields['enddate'].required = False
            self.fields['buste_free'].required = False
            self.fields['statue_free'].required = None
            self.fields['beard_free'].required = None
            self.fields['equestrian_free'].required = None
            self.fields['corona_laurea_free'].required = None
            self.fields['corona_civica_free'].required = None
            self.fields['corona_radiata_free'].required = None                 
            self.fields['toga_free'].required = None
            self.fields['cuirass_free'].required = None
            self.fields['heroic_semi_nude_free'].required = None
            self.fields['seated_free'].required = None
            self.fields['paludamentum_free'].required = None
            self.fields['sword_belt_free'].required = None
            self.fields['contabulata_free'].required = None
            self.fields['headgear_free'].required = None
            self.fields['capite_velato_free'].required = None            
            self.fields['lsa'].required = False
            
            # in fields staat eea verzameld maar hier gaat het niet goed
            self.fields['origidlist'].queryset = Portrait.objects.all().order_by('origstr')
            self.fields['namelist'].queryset = Portrait.objects.all().order_by('name')
            self.fields['emplist'].queryset = Emperor.objects.all().order_by('name')
            self.fields['matlist'].queryset = Material.objects.all().order_by('name') 
            self.fields['recarvedlist'].queryset = Recarved.objects.all().order_by('name')
            self.fields['provlist'].queryset = Province.objects.all().order_by('name')
            self.fields['ancloclist'].queryset = Location.objects.all().order_by('name')             
            self.fields['curloclist'].queryset = CurrentLocation.objects.all().order_by('name')             
            self.fields['contlist'].queryset = Context.objects.all().order_by('name')
            self.fields['iconlist'].queryset = Iconography.objects.all().order_by('name')
            self.fields['attrlist'].queryset = Attributes.objects.all().order_by('name')
            self.fields['wreathlist'].queryset = Wreathcrown.objects.all().order_by('name')            
            self.fields['referenceslist'].queryset = Portrait.objects.all().order_by('reference')  
               
            # Get the instance, moet ik hier meer mee doen?
            if 'instance' in kwargs:
                instance = kwargs['instance']
                            
                emperor = instance.emperor
                if emperor != None:
                    self.fields['empname'].initial = emperor.name
                
                elif instance != None:
                    pass
        except:
            msg = oErr.get_error_message()
            oErr.DoError("PortraitForm")

        # Return the response
        return None




