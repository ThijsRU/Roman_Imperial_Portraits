"""
Definition of views for the RIPD app.
"""

from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from datetime import datetime

from ripdapp.models import *

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

    return render(request,'ripdapp/nlogin.html', context)

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
    return render(request, 'ripdapp/signup.html', {'form': form})




def update_from_excel(request):
    """Check if contents can be updated from the MEDIA excel file"""

    # Can only be done by a super-user
    if request.user.is_superuser:
        pass
    
    # What we return is simply the home page
    return reverse('home')

