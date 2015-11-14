from django.contrib.auth.models import Group
from django.shortcuts import render as django_render
from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    Http404, HttpResponseBadRequest, HttpResponse
from django.core.urlresolvers import reverse

# Groups for the Django authentication system
doctors, _d_created = Group.objects.get_or_create(name="Doctors")
patients, _p_created = Group.objects.get_or_create(name="Patients")

USER_GROUPS = [
    ("Doctors", "Doctor", doctors),
    ("Patients", "Patient", patients)
]


def user_in_group(user, group):
    return user.groups.filter(name=group).count() > 0


def render(request, template_name, vars=None, *args, **kwargs):
    if vars is None:
        vars = {}
    if request.user.is_authenticated() and "user" not in vars:
        vars["user"] = request.user
        vars["is_doctor"] = user_in_group(request.user, "Doctors")
        vars["is_nurse"] = user_in_group(request.user, "Nurses")
        vars["is_patient"] = user_in_group(request.user, "Patients")
    return django_render(request, template_name, vars, *args, **kwargs)


def requires_user(user_groups=None, redirect_on_fail=None):
    """
    Returns a function decorator that can be used on a view to check if a user
    is logged in and, if so, if the user is a certain type.

    :param user_groups: A list of the names of user groups that are allowed,
        including "Administrators" to represent administrators.
        If None, then defaults to any type of user.
    :param redirect_on_fail: Whether to redirect to the login page on a
        failure.
        * True: always redirect to the login page on a failure.
        * False: always throw a 403 Forbidden on a failure.
        * None: redirect to the login page if no user is logged in, or
          log the user out if user_groups was originally None, or
          otherwise throw a 404 Not Found.
    """
    any_group = False
    if user_groups is None:
        any_group = True
        user_groups = [group_name for group_name, _1, _2 in USER_GROUPS]

    def _call_handler(func):
        """
        Function decorator for a view that requires a user of a certain type
        to be logged in.
        """
        def _request_handler(request, *args, **kwargs):
            logged_in = request.user.is_authenticated()
            if logged_in:
                # User is logged in... but is that good enough?
                good_enough = False
                # First, check if the user is an administrator (and if that's OK)
                if (request.user.is_superuser or request.user.is_staff):
                    good_enough = True
                else:
                    # Check if the user is a part of any of the possible groups
                    for group in user_groups:
                        if user_in_group(request.user, group):
                            # Found one!
                            good_enough = True
                            break
                if good_enough:
                    # Woohoo! The user is A-OK
                    return func(request, *args, **kwargs)

            # Nope, the user failed :(

            if redirect_on_fail is True:
                return HttpResponseRedirect(reverse("portal:login"))
            if redirect_on_fail is False:
                return HttpResponseForbidden("<h1>Access Denied</h1>")

            # Alrighty... redirect_on_fail wasn't explicitly set, so we need to
            # figure something out.

            # If no user was logged in, redirect to the login page
            if not logged_in:
                return HttpResponseRedirect(reverse("portal:login"))
            # If we were accepting ANY group and the user STILL failed, log out
            if any_group:
                return HttpResponseRedirect(reverse("portal:logout"))
            # Last resort: throw a 404 at them
            raise Http404()
        return _request_handler
    return _call_handler
