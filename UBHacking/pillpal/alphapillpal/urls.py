from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.accounts.login_page, name='login'),
    # home URL
    url(r'^home/$', views.accounts.home, name='home'),
    # Logout URL
    url(r'^logout/$', views.accounts.logout_page, name='logout'),

    # Create Account
    url(r'^create/$', views.accounts.create_account, name='create')

    # add two urls- one for doctor and one for patient adding medication
]