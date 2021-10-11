"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelMultipleChoiceField, ModelChoiceField
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget


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

class EmperorWidget(ModelSelect2MultipleWidget):
    model = Emperor
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Emperor.objects.all().order_by('name')     
        return qs

class MaterialWidget(ModelSelect2MultipleWidget):
    model = Material
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): # is er een self? werkt niet zoals bij Passim
        return obj.name

    def get_queryset(self): # werkt niet       
        qs = Material.objects.all().order_by('name') # gaat dit goed? Niet zoals bij Keyword in Passim. Hier komt hij niet als de site opstart.
        #dit wordt gebruikt als er naar Browse wordt gegaan     
        return qs

class ProvinceWidget(ModelSelect2MultipleWidget):
    model = Province
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Province.objects.all().order_by('name')     
        return qs

class ContextWidget(ModelSelect2MultipleWidget):
    model = Context
    search_fields = [ 'name__icontains' ]
   
    def label_from_instance(self, obj): 
        return obj.name

    def get_queryset(self):
        qs = Province.objects.all().order_by('name')     
        return qs

class PortraitForm(forms.ModelForm):
    """One form to handle the Portrait searching and details view"""

    # Buiten model Portrait, zoals emperor en de rest Keyword is een voorbeeld voor Emperor and Context
    # het werkt een beetje...nog niet de juiste resultaten
    #empname = forms.CharField(label="Emperor", required=False,     #                         widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
   
    emplist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=EmperorWidget(attrs={'data-placeholder': 'Select multiple emperors...', 'style': 'width: 100%;', 'class': 'searching'}))
    

    wreathname = forms.CharField(label="WreathCrown", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching wreathcrown input-sm', 'placeholder': 'Name of the wreath or crown...',  'style': 'width: 100%;'}))
    
    matlist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=MaterialWidget(attrs={'data-placeholder': 'Select multiple materials...', 'style': 'width: 100%;', 'class': 'searching'})) #, 

    #matname = forms.CharField(label="Material", required=False,     #                          widget=forms.TextInput(attrs={'class': 'typeahead searching material input-sm', 'placeholder': 'Name of the material...',  'style': 'width: 100%;'}))
    
    #date_from   = forms.IntegerField(label=_("Date start"), required = False,
    #                                 widget=forms.TextInput(attrs={'placeholder': 'Starting from...',  'style': 'width: 30%;', 'class': 'searching'}))
    #date_until  = forms.IntegerField(label=_("Date until"), required = False,
    # 3                                widget=forms.TextInput(attrs={'placeholder': 'Until (including)...',  'style': 'width: 30%;', 'class': 'searching'}))
            locname = forms.CharField(label="Location", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching location input-sm', 'placeholder': 'Name of the ancient city...',  'style': 'width: 100%;'}))
    
    provname = forms.CharField(label="Province", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching province input-sm', 'placeholder': 'Name of the province...',  'style': 'width: 100%;'}))
        provlist = ModelMultipleChoiceField(queryset=None, required=False, 
                               widget=ProvinceWidget(attrs={'data-placeholder': 'Select one province...', 'style': 'width: 100%;', 'class': 'searching'}))
    contname = forms.CharField(label="Context", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching context input-sm', 'placeholder': 'Name of the context...',  'style': 'width: 100%;'}))
    
    #contlist = ModelMultipleChoiceField(queryset=None, required=False, 
    #                           widget=ContextWidget(attrs={'data-placeholder': 'Select one context...', 'style': 'width: 100%;', 'class': 'searching'}))

    # Icon werkt helemaal niet, wat gaat er niet goed? Erwin vragen, met lijsten werken?
    iconname = forms.CharField(label="Iconography cuirass", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching iconography input-sm', 'placeholder': 'Name of the icon...',  'style': 'width: 100%;'}))
    
    attrname = forms.CharField(label="Attributes", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching attributes input-sm', 'placeholder': 'Name of the attribute...',  'style': 'width: 100%;'}))
    
    arachid = forms.CharField(label="Arachne", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching arachne input-sm', 'placeholder': 'Arachne id of the portrait...',  'style': 'width: 100%;'}))
    
    # Let op, in PASSIM is er een aantal Status, Manuscript type en Keyword, zijn lijsten, meerdere te selecteren. EK evt vragen
    
    # This is to circumvent the standard filter option for the Booleans: False
    disputed_free = forms.NullBooleanField()
    buste_free = forms.NullBooleanField()
    statue_free = forms.NullBooleanField()
    part_group_free = forms.NullBooleanField()
    recarvedboo_free = forms.NullBooleanField()
    toga_free = forms.NullBooleanField()            
    cuirass_free = forms.NullBooleanField()
    heroic_semi_nude_free = forms.NullBooleanField()
    seated_free = forms.NullBooleanField()
    paludamentum_free = forms.NullBooleanField()
    sword_belt_free = forms.NullBooleanField()
    capite_velato_free = forms.NullBooleanField()
    corona_laurea_free = forms.NullBooleanField()
    corona_civica_free = forms.NullBooleanField()
    corona_radiata_free = forms.NullBooleanField()
    
    # hier booleans
    
    # hoe zit het met typeahead?
    typeaheads = ['emperor', 'location', 'province', 'context', 'wreathname'] # werkt nog niet, hoe zit het oin PASSIM? Erwin vragen

   # libname_ta  = forms.CharField(label=_("Library"), required=False, 
    
    # widget=forms.TextInput(attrs={'class': 'typeahead searching libraries input-sm', 'placeholder': 'Name of library...',  'style': 'width: 100%;'}))
    

    # zie Author als voorbeeld Equal goldlistview keyS keyfk check it out

    # =========== Portrait-specific ===========================
    
    class Meta:
        ATTRS_FOR_FORMS = {'class': 'form-control'};

        model = Portrait
        fields = ['name', 'origstr',  'startdate', 'enddate', 'reference', 'lsa'] # eea lijkt te werken
        widgets={'name':             forms.TextInput(attrs={'placeholder': 'Name of the portrait...', 'style': 'width: 100%;', 'class': 'searching'}),
                 #'name':             forms.RadioSelect(attrs={'style': 'width: 100%;'}),
                 #'disputed':         forms.NullBooleanSelect(),
                 #'location':         forms.TextInput(attrs={'style': 'width: 100%;'}),
                 #'location':         forms.SelectMultiple(attrs={'style': 'width: 100%;'}),
                 #'recarvedboo':      forms.NullBooleanSelect(),
                 'origstr':          forms.TextInput(attrs={'placeholder': 'Original id of the portrait...', 'style': 'width: 100%;'}),
                 'startdate':        forms.NumberInput(), # aan te passen, "vanaf een jaar" dus de input dient als startpunt om te bepalen
                                                          # vanaf welk jaartal de portraits meegenomen moeten worden, dus "50" is alles vanaf 50
                                                          # range of years, SelectDateWidget? Date Range in Passim?
                 'enddate':          forms.NumberInput(), # aan te passen, "tot een bepaald jaar" PASSIM?
                 #'statue':           forms.NullBooleanSelect(),
                 #'bust':             forms.Select(), # deze doet het wel maar bij andere werkt het niet
                 #'toga':             forms.NullBooleanSelect(),
                 #'cuirass':          forms.NullBooleanSelect(),
                 #'heroic_semi_nude': forms.NullBooleanSelect(),
                 #'seated':           forms.NullBooleanSelect(),
                 #'paludamentum':     forms.NullBooleanSelect(),
                 #'sword_belt':       forms.NullBooleanSelect(),
                 #'capite_velato':    forms.NullBooleanSelect(),
                 #'corona_laurea':    forms.NullBooleanSelect(),
                 #'corona_civica':    forms.NullBooleanSelect(),
                 #'corona_radiata':   forms.NullBooleanSelect(),
                 'reference':         forms.TextInput(attrs={'placeholder': 'Reference contains...', 'style': 'width: 100%;'}),                 
                 'lsa':              forms.TextInput(attrs={'placeholder': 'LSA id of the portrait...', 'style': 'width: 100%;'}),
                 
                 } 

    def __init__(self, *args, **kwargs):
        # Start by executing the standard handling
        super(PortraitForm, self).__init__(*args, **kwargs)
        oErr = ErrHandle()
        try:
            # Set other parameters
            # Ok, hij doet de laatste steeds
            
            self.fields['name'].required = False            
            self.fields['disputed_free'].required = None
            self.fields['part_group_free'].required = None
            self.fields['buste_free'].required = None
            self.fields['recarvedboo_free'].required = None
            self.fields['startdate'].required = False
            self.fields['enddate'].required = False
            self.fields['buste_free'].required = False
            self.fields['statue_free'].required = None
            self.fields['corona_laurea_free'].required = None
            self.fields['corona_civica_free'].required = None
            self.fields['corona_radiata_free'].required = None                 
            self.fields['toga_free'].required = None
            self.fields['cuirass_free'].required = None
            self.fields['heroic_semi_nude_free'].required = None
            self.fields['seated_free'].required = None
            self.fields['paludamentum_free'].required = None
            self.fields['sword_belt_free'].required = None
            self.fields['capite_velato_free'].required = None            
            self.fields['lsa'].required = False
            
            # in fields staat eea verzameld maar hier gaat het niet goed
            self.fields['emplist'].queryset = Emperor.objects.all().order_by('name')
            self.fields['matlist'].queryset = Material.objects.all().order_by('name') # er gaat iets met die queryset? 
            self.fields['provlist'].queryset = Province.objects.all().order_by('name')
            self.fields['contlist'].queryset = Context.objects.all().order_by('name')
            
          
            # Get the instance
            if 'instance' in kwargs:
                instance = kwargs['instance']
                # Material
                                
                # Check if there is an emperor specified TH: hier verder iets mee doen?? MAANDAG
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




