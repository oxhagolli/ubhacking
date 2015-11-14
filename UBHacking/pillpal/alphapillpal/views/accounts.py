from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    Http404, HttpResponseBadRequest, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password

from .. import utils


def login_page(request):
    vars = {}
    user = None
    #if the user is trying to log in
    if request.method =="POST":
        #check if they left username or password blank
        if not request.POST.get("username", None) or \
            not request.POST.get("password", None):
            vars["errorMessage"] = "Missing username or password."
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username = username, password = password)
            #if the username or password was incorrect
            if user == None:
                vars["errorMessage"] = "Username and/or password is incorrect."
            elif not user.is_active:
                vars["errorMessage"] = "Account is disabled"
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
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")
    firstName = request.POST.get("firstName" "").strip()
    lastName = request.POST.get("lastName", "").strip()

    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password1,
                                    first_name=firstName,
                                    last_name=lastName)
    user.groups = Group.objects.filter(name="Patients")
    user.save()

    #login as new user
    user = authenticate(username=username, password=password1)
    login(request, user)
    return HttpResponseRedirect(reverse("alphapillpal:home"))