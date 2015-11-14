from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.accounts.login_page, name='login'),
]