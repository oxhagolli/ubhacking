import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    Http404, HttpResponseBadRequest, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext as _

from ..models import *
from .. import utils

def addMedicationDoc(request):
    #if they haven't submitted yet
    if request.method != "POST":
        # Just the base page
        return utils.render(request, "alphapillpal/addMedication.html")
    #otherwise, user submitted an edited version
    try:
        patient = User.objects.get(pk=request.POST.get("patient"))
    except User.DoesNotExist:
        return HttpResponseBadRequest("Invalid patient")
    #add normally

#add new medication
def addMedication(request):
    #if they haven't submitted yet
    if request.method != "POST":
        # Just the base page
        return utils.render(request, "alphapillpal/addMedication.html")
    #otherwise, user submitted an edited version
    name = request.POST.get("name", "").strip()
    time = request.POST.get("time", "")
    days = [] #list of days that medication needs to be taken
    for day in days:
        #ORENS DO PLS
        return

    daysJson = json.dumps(days)

    #created new medication for patient
    request.user.medication_set.create(patient=request.user, name=name, time=time, days=daysJson)

    return HttpResponseRedirect(reverse("alphapillpal/home-"))



#remove existing medication
def removeMedication(request):
    return

#edit existing medication
def editMedication(request):
    return


#view medications
def viewMedication(request):
    return utils.render(request, "alphapillpal/viewMedication.html")