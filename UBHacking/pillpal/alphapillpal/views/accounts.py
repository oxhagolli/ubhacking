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


def login_page(request):
    vars = {}
    user = None
    #if the user is trying to log in
    if request.method =="POST":
        #check if they left username or password blank
        if not request.POST.get("email", None) or \
            not request.POST.get("password", None):
            vars["error_message"] = _("Missing email or password")
        else:
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(username = email, password = password)
            #if the username or password was incorrect
            if user == None:
                vars["error_message"] = _("Email and/or password is incorrect")
            elif not user.is_active:
                vars["error_message"] = _("Account is disabled")
                user = None
    if user == None:
        #if the user is already logged in
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("alphapillpal:home"))
        else:
            return utils.render(request, "alphapillpal/login.html", vars)
    else:
        login(request, user)
        #redirect to user's homepage
        return HttpResponseRedirect(reverse("alphapillpal:home"))


#logout user
def logout_page(request):
    logout(request)
    # Redirect back to the login page
    return HttpResponseRedirect(reverse("alphapillpal:login"))


#user's home page
def home(request):
    for group_name, item_name, group in utils.USER_GROUPS:
        if utils.user_in_group(request.user, group_name):
            return utils.render(request, "alphapillpal/home-%s.html" %
                                item_name.lower())

    # If none of these, let's check if they're an administrator
    if request.user.is_superuser or request.user.is_staff:
        return utils.render(request, "alphapillpal/home-administrator.html")




#create new account
def create_account(request):
    # If there is a user logged in, log them out and then redirect to ourselves
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect(reverse("alphapillpal:create"))

    #if they haven't submitted yet
    if request.method != "POST":
        # Just the base page
        return utils.render(request, "alphapillpal/create.html")

    #otherwise, they submitted to create new account
    email = request.POST.get("email", "").strip()
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")
    firstName = request.POST.get("firstName" "").strip()
    lastName = request.POST.get("lastName", "").strip()

    def err(msg):
        return utils.render(request, "portal/create.html", {
            "username": email,
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "error_message": msg
        })
    #check username first
    if not email:
        return err(_("Missing email"))
    if User.objects.filter(username=email).exists():
        return err(_("Email already taken"))

    #check email next
    if not email:
        return err(_("Missing email"))

    if not firstName or not lastName:
        return err(_("Missing name"))

    #check password next
    if not password1 or not password2:
        return err(_("Missing password"))
    if password1 != password2:
        return err(_("Passwords don't match"))


    user = User.objects.create_user(username=email,
                                    email=email,
                                    password=password1,
                                    first_name=firstName,
                                    last_name=lastName)
    if user is None:
        return err(_("Couldn't create user"))
    user.groups = Group.objects.filter(name="Patients")
    user.save()

    #login as new user
    user = authenticate(username=email, password=password1)
    login(request, user)
    return HttpResponseRedirect(reverse("alphapillpal:home"))