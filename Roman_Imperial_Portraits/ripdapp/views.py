from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def index(request):
    now = datetime.now()

    return render(
        request,
        "ripdapp/index.html",  # Relative path from the 'templates' folder to the template file
        # "index.html", # Use this code for VS 2017 15.7 and earlier
        {
            'title' : "Roman Imperial Portraits Database",
            'message' : "Roman Imperial Portraits Database",
            'content' : " on " + now.strftime("%A, %d %B, %Y at %X"),
            'message2': "This website is made by Thijs Hermsen"
            #'content': "<strong>Roman Imperial Portraits Database</strong> on " + now.strftime("%A, %d %B, %Y at %X")
        }
    )
    #html_content = "<html><head><title>Roman Imperial Portraits Database</title></head><body>"
    #html_content += "<strong>Roman Imperial Portraits Database</strong> on " + now.strftime("%A, %d %B, %Y at %X")
    #html_content += "</body></html>"

    #return HttpResponse(html_content)

def about(request):
    return render(
        request,
        "ripdapp/about.html",
        {
            'title' : "About Roman Imperial Portraits Database",
            'content' : "Example app page for Django. This app was developed for the project....",
            'content2': "Second Example app page for Django. This app was developed for the project...."
        }
    )


def welcome(request):
    return render(
        request,
        "ripdapp/welcome.html",
        {
            'title' : "Welcome Roman Imperial Portraits Database",
            'content' : "This is the welcome page of the RIPD ",
            'year':datetime.now().year
        }
    )

def browse(request):
    return render(
        request,
        "ripdapp/browse.html",
        {
            'title' : "Browse Roman Imperial Portraits Database",
            'content' : "This is the browse page of the RIPD "            
        }
    )

def advsearch(request):
    return render(
        request,
        "ripdapp/advsearch.html",
        {
            'title' : "Advanced search Roman Imperial Portraits Database",
            'content' : "This is the advanced search page of the RIPD "            
        }
    )

def reflinks(request):
    return render(
        request,
        "ripdapp/reflinks.html",
        {
            'title' : "References and links Roman Imperial Portraits Database",
            'content' : "This is the references and links page of the RIPD "            
        }
    )