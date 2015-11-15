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
    patient = request.user #THIS IS WRONG
    name = request.POST.get("name", "").strip()
    time = request.POST.get("time", "")
    days = [] #list of days that medication needs to be taken
    for day in days:
        #ORENS DO PLS
        return

    daysJson = json.dumps(days)

    #created new medication for patient
    request.user.medication_set.create(patient=request.user, name=name, time=time, days=daysJson)

    return HttpResponseRedirect(reverse("alphapillpal:patient-details") +
                                        "?patient=" + str(patient.id))


#add new medication
def addMedication(request):
    #if they haven't submitted yet
    if request.method != "POST":
        # Just the base page
        return utils.render(request, "alphapillpal/addMedication.html")
    #otherwise, user submitted an edited version
    name = request.POST.get("name", "").strip()
    time = request.POST.get("time", "")
    times = json.dumps([time]) #change this in the future when we have more times - look down!
    chosenDays = []
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"] #list of days that medication needs to be taken
    #put chosen strings in new list
    for day in days:
        if request.POST.get(day) is not None:
            chosenDays.append(request.POST.get(day))
    # Turn the list into JSON string
    daysJson = json.dumps(chosenDays)

    #created new medication for patient
    request.user.medication_set.create(patient=request.user, name=name, time=times, days=daysJson)
    return HttpResponseRedirect(reverse("alphapillpal:home"))


#remove existing medication
def removeMedication(request):
    #getting patient
    patient = request.POST.get("patient", "")
    #getting medicine we want to remove and removes it
    patient.medication_set.get(pk=request.POST.get("medicine")).delete()



#edit existing medication
def editMedication(request):
    #if they haven't submitted yet
    if request.method != "POST":
        # Just the base page
        return utils.render(request, "alphapillpal/editMedication.html") #add auto-fill
    #otherwise, user submitted an edited version
    #getting patient
    patient = request.POST.get("patient", "")
    name = request.POST.get("name", "").strip()
    time = request.POST.get("time", "")
    days = [] #list of days that medication needs to be taken
    for day in days:
        #ORENS DO PLS
        return

    daysJson = json.dumps(days)

    #created new medication for patient
    medicine = patient.medication_set.get(pk=request.POST.get("medicine", ""))
    medicine.patient = patient
    medicine.name = name
    medicine.time = time
    medicine.days = daysJson

    medicine.save()

    return HttpResponseRedirect(reverse("alphapillpal:home"))


#view medications
def viewMedication(request):
    return utils.render(request, "alphapillpal/home-patient.html")