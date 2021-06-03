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

    # =========== Portrait-specific ===========================

    class Meta:
        ATTRS_FOR_FORMS = {'class': 'form-control'};

        model = Portrait
        fields = ['name']
        widgets={'name':        forms.TextInput(attrs={'placeholder': 'English name...', 'style': 'width: 100%;', 'class': 'searching'})
                 }

    def __init__(self, *args, **kwargs):
        # Start by executing the standard handling
        super(PortraitForm, self).__init__(*args, **kwargs)

        oErr = ErrHandle()
        try:
            # Set other parameters
            self.fields['name'].required = False
            
            # Get the instance
            if 'instance' in kwargs:
                instance = kwargs['instance']
                if instance != None:
                    pass
        except:
            msg = oErr.get_error_message()
            oErr.DoError("PortraitForm")

        # Return the response
        return None




