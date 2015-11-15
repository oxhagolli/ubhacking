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

#pick a patient!
@utils.requires_user(["Doctors", "Nurses"])
def patient_view(request):
    #displays list of patients to pick
    return utils.render(request, "alphapillpal/patient-view.html", {
        "patients": User.objects.filter(groups__name="Patients")
    })


@utils.requires_user(["Doctors"])
#view patient details
def patient_details(request):
    #if patient does not exist
    try:
        patient = User.objects.get(pk=request.GET.get("patient"))
    except User.DoesNotExist:
        return HttpResponseBadRequest("Invalid patient")
    #display patient's details with option to edit
    return utils.render(request, "portal/patient-detail.html", {
        "patient": patient})