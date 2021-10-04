"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

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

class PortraitForm(forms.ModelForm):
    """One form to handle the Portrait searching and details view"""

    # Buiten model Portrait, zoals emperor en de rest Keyword is een voorbeeld voor Emperor and Context
    # het werkt een beetje...nog niet de juiste resultaten
    empname = forms.CharField(label="Emperor", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching emperor input-sm', 'placeholder': 'Name of the emperor...',  'style': 'width: 100%;'}))
    
    matname = forms.CharField(label="Material", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching material input-sm', 'placeholder': 'Name of the material...',  'style': 'width: 100%;'}))
    
    locname = forms.CharField(label="Location", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching location input-sm', 'placeholder': 'Name of the ancient city...',  'style': 'width: 100%;'}))
    
    provname = forms.CharField(label="Province", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching province input-sm', 'placeholder': 'Name of the province...',  'style': 'width: 100%;'}))
        contname = forms.CharField(label="Context", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching context input-sm', 'placeholder': 'Name of the context...',  'style': 'width: 100%;'}))
    
    # Icon werkt helemaal niet, wat gaat er niet goed? Erwin vragen, met lijsten werken?
    iconname = forms.CharField(label="Iconography cuirass", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching iconography input-sm', 'placeholder': 'Name of the icon...',  'style': 'width: 100%;'}))
    
    attrname = forms.CharField(label="Attributes", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching attributes input-sm', 'placeholder': 'Name of the attribute...',  'style': 'width: 100%;'}))
    
    arachid = forms.CharField(label="Arachne", required=False,                               widget=forms.TextInput(attrs={'class': 'typeahead searching arachne input-sm', 'placeholder': 'Arachne id of the portrait...',  'style': 'width: 100%;'}))
   
    # locname= forms.SelectMultiple()
    
    # hoe zit het met typeahead?
    typeaheads = ['emperor', 'material', 'location', 'province', 'context'] # werkt nog niet, hoe zit het oin PASSIM? Erwin vragen

   # libname_ta  = forms.CharField(label=_("Library"), required=False, 
    
    # widget=forms.TextInput(attrs={'class': 'typeahead searching libraries input-sm', 'placeholder': 'Name of library...',  'style': 'width: 100%;'}))
    

    # zie Author als voorbeeld Equal goldlistview keyS keyfk check it out

    # =========== Portrait-specific ===========================
    
    class Meta:
        ATTRS_FOR_FORMS = {'class': 'form-control'};

        model = Portrait
        fields = ['name', 'disputed', 'recarvedboo', 'origstr', 'statue', 'buste', 'toga', 'cuirass', 'heroic_semi_nude','seated', 'paludamentum', 
                  'sword_belt', 'capite_velato', 'corona_laurea', 'corona_civica', 'corona_radiata', 'reference', 'lsa'] # eea lijkt te werken
       
        widgets={'name':             forms.TextInput(attrs={'placeholder': 'Name of the portrait...', 'style': 'width: 100%;', 'class': 'searching'}),
                 'disputed':         forms.NullBooleanSelect(),
                 'location':         forms.TextInput(attrs={'style': 'width: 100%;'}),
                 'recarvedboo':      forms.NullBooleanSelect(),   
                 'origstr':          forms.TextInput(attrs={'placeholder': 'Original id of the portrait...', 'style': 'width: 100%;'}),
                 'statue':           forms.NullBooleanSelect(),
                 'bust':             forms.Select(), # deze doet het wel maar bij andere werkt het niet
                 'toga':             forms.NullBooleanSelect(),
                 'cuirass':          forms.NullBooleanSelect(),
                 'heroic_semi_nude': forms.NullBooleanSelect(),
                 'seated':           forms.NullBooleanSelect(),
                 'paludamentum':     forms.NullBooleanSelect(),
                 'sword_belt':       forms.NullBooleanSelect(),
                 'capite_velato':    forms.NullBooleanSelect(),
                 'corona_laurea':    forms.NullBooleanSelect(),
                 'corona_civica':    forms.NullBooleanSelect(),
                 'corona_radiata':   forms.NullBooleanSelect(),
                 'reference':        forms.TextInput(attrs={'placeholder': 'Reference contains...', 'style': 'width: 100%;'}),
                 
                 'lsa':              forms.TextInput(attrs={'placeholder': 'LSA id of the portrait...', 'style': 'width: 100%;'}),
                 } 
        
        # Zie regel 1326 van forms.py in Passim
        
        #widgets={'emperor':     forms.TextInput(attrs={'placeholder': 'Name of the emperor...', 'style': 'width: 100%;', 'class': 'searching'})
         #        }

    def __init__(self, *args, **kwargs):
        # Start by executing the standard handling
        super(PortraitForm, self).__init__(*args, **kwargs)

        oErr = ErrHandle()
        try:
            # Set other parameters
            # Ok, hij doet de laatste steeds
            
            self.fields['name'].required = False
            #self.fields['emperor'].required = False
            self.fields['disputed'].required = False
            self.fields['recarvedboo'].required = False
            self.fields['statue'].required = False
            self.fields['corona_laurea'].required = False
            self.fields['corona_civica'].required = False
            self.fields['corona_radiata'].required = False
            self.fields['lsa'].required = False
        
           
            
            # Get the instance
            if 'instance' in kwargs:
                instance = kwargs['instance']
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




