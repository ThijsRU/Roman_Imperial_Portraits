"""
Views that are needed to show a map
"""

from django.views.generic.detail import DetailView
from django.urls import reverse

from django.views.generic.list import ListView, View
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.db import connection
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse

import fnmatch
import sys

class ErrHandle:
    """Error handling"""

    # ======================= CLASS INITIALIZER ========================================
    def __init__(self):
        # Initialize a local error stack
        self.loc_errStack = []

    # ----------------------------------------------------------------------------------
    # Name :    Status
    # Goal :    Just give a status message
    # History:
    # 6/apr/2016    ERK Created
    # ----------------------------------------------------------------------------------
    def Status(self, msg):
        # Just print the message
        print(msg, file=sys.stderr)

    # ----------------------------------------------------------------------------------
    # Name :    DoError
    # Goal :    Process an error
    # History:
    # 6/apr/2016    ERK Created
    # ----------------------------------------------------------------------------------
    def DoError(self, msg, bExit = False):
        # Append the error message to the stack we have
        self.loc_errStack.append(msg)
        # Print the error message for the user
        print("Error: "+msg+"\nSystem:", file=sys.stderr)
        # Get the error message
        sSysMsg = self.get_error_message()
        print(sSysMsg, file=sys.stderr)
        # Add the system error to the stack too
        self.loc_errStack.append(sSysMsg)
        # Is this a fatal error that requires exiting?
        if (bExit):
            sys.exit(2)
        # Otherwise: return the string that has been made
        return "<br>".join(self.loc_errStack)


    def get_error_message(self):
        arInfo = sys.exc_info()
        if len(arInfo) == 3:
            sMsg = str(arInfo[1])
            if arInfo[2] != None:
                sMsg += " at line " + str(arInfo[2].tb_lineno)
            return sMsg
        else:
            return ""

def adapt_search(val):
    # First trim
    val = val.strip()    
    # Adapt for the use of '#'
    if '#' in val:
        val = r'(^|(.*\b))' + val.replace('#', r'((\b.*)|$)')
    else:
        val = '^' + fnmatch.translate(val) + '$'
    return val



class MapView(DetailView):
    """Show the 'trefwoorden' belonging to this lemma, after applying a filter"""

    model = None
    modEntry = None
    frmSearch = None
    entry_list = []
    order_by = ""
    labelfield = ""
    use_object = True
    filterQ = None
    label = ""
    qs = None
    prefix = ""

    def get(self, request, *args, **kwargs):
        # No errors, just return to the homepage
        return reverse('home')

    def initialize(self):
        # This is where the user may himself call [add_entry] to fill the [entry_list]
        self.entry_list = []
        
    def add_entry(self, key, type="str", query="", form="", fkfield=""):
        self.entry_list.append(dict(key=key, form=form, type=type, query=query, fkfield=fkfield))

    def get_object(self, queryset = None):
        if self.use_object:
            response = super(MapView, self).get_object(queryset)
        else:
            response = None
        return response

    def get_popup(self, entry):
        return "(no popup specified)"
    
    def post(self, request, *args, **kwargs):
        # Formulate a response
        data = {'status': 'error', 'msg': 'unknown'}

        def query_add(lstQ, val, path, type, fkfield = None):
            if type == "str" and val != "" and val != None:
                comparison = "iexact"
                if '*' in val or '[' in val or '?' in val or '#' in val:
                    val = adapt_search(val)
                    comparison = "iregex"
                lstQ.append(Q(**{"{}__{}".format(path, comparison): val}))
            elif type == "int" and val != "" and val != None:
                if val.isdigit():
                    iVal = int(val)
                    if iVal>0:
                        lstQ.append(Q(**{"{}".format(path): iVal}))
            elif type == "fk" and val != "" and val != None and fkfield != None:
                val = getattr(val, fkfield)
                lstQ.append(Q(**{"{}__{}".format(path, fkfield): val}))

        oErr = ErrHandle()
        try:
            # First initialize
            self.initialize() 

            # Get the object from what we receive
            obj = self.get_object()

            # Get the search parameters, if any
            if self.prefix == "":
                search_form = self.frmSearch(request.POST)
            else:
                search_form = self.frmSearch(request.POST, prefix=self.prefix)
            # It should always be valid, but this gives [cleaned_data]
            if search_form.is_valid():
                # Get the data
                cleaned_data = search_form.cleaned_data

                # Build a filter to get all entries, based on the cleaned data
                lstQ = []

                # Possibly add one filter
                if self.filterQ != None:
                    lstQ.append(self.filterQ)

                # Start with the main object's id
                if self.use_object:
                    # Note: this is for detail views probably
                    lstQ.append(Q(**{"{}__id".format(self.model._meta.model_name.lower()): obj.id}))

                # Derive the variables from the cleaned_data according to entry_list
                value_list = []
                for oItem in self.entry_list:
                    sValue = oItem['query']
                    if oItem['form'] != "":
                        form_value = cleaned_data.get(oItem['form'], "")
                        # Add to the query
                        if 'fkfield' in oItem and oItem['fkfield'] != "":
                            query_add(lstQ, form_value, oItem['query'], oItem['type'], fkfield=oItem['fkfield'])
                            sValue = "{}__{}".format(oItem['query'], oItem['fkfield'])
                        else:
                            query_add(lstQ, form_value, oItem['query'], oItem['type'])
                    else:
                        if 'fkfield' in oItem and oItem['fkfield'] != "":
                            sValue = "{}__{}".format(oItem['query'], oItem['fkfield'])
                    oItem['value_key'] = sValue
                    # ALl items: get their values into [value_list]
                    value_list.append(sValue)

                # Action depends on where the query comes from
                if self.qs == None:
                    # Get features of all the ENtry elements satisfying the condition
                    total = self.modEntry.objects.filter(*lstQ).count()
                    # Retrieve all the necessary entries
                    lst_entry = self.modEntry.objects.filter(*lstQ).order_by(*self.order_by).values(*value_list)
                else:
                    # We already have a query...
                    total = self.qs.count()
                    # Retrieve all the necessary entries
                    lst_entry = self.qs.order_by(*self.order_by).values(*value_list)

                # Create a new list that uses the 'key's from entry_list
                lst_back = []
                for item in lst_entry:
                    oEntry = {}
                    for oItem in self.entry_list:
                        oEntry[oItem['key']] = item[oItem['value_key']]

                    # Check if the points are okay
                    bSkip = False
                    if "point_x" in oEntry and "point_y" in oEntry:
                        try:
                           point_x = float(oEntry['point_x'])
                           point_y = float(oEntry['point_y'])
                        except:
                            bSkip = True

                    if not bSkip:
                        # Combine point_x, point_y if needed
                        if not "point" in oEntry and "point_x" in oEntry and "point_y" in oEntry:
                            oEntry['point'] = "{}, {}".format(oEntry['point_x'], oEntry['point_y'])
                        oEntry['pop_up'] = self.get_popup(oEntry)
                        lst_back.append(oEntry)

                # Possibly perform grouping 
                lst_back = self.group_entries(lst_back)

                # Add the data
                data['entries'] = lst_back
                if self.use_object:
                    data['label'] = getattr(obj, self.labelfield)    
                else:
                    data['label'] = self.label

                # Set the status to okay
                data['status'] = 'ok'

        except:
            data['msg'] = oErr.get_error_message()
            oErr.DoError("MapView/post")

        return JsonResponse(data) 

    def group_entries(self, lst_this):
        """Allow changing the list of entries"""

        return lst_this

