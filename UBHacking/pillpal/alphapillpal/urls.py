from django.conf.urls import url

from . import views

urlpatterns = [
    # Login page
    url(r'^$', views.accounts.login_page, name='login'),
    # Home page
    url(r'^home/$', views.accounts.home, name='home'),
    # Logout page
    url(r'^logout/$', views.accounts.logout_page, name='logout'),

    # Create Account
    url(r'^create/$', views.accounts.create_account, name='create'),

    # Doctor can view list of patients to select
    url(r'^patients/$', views.doctor.patient_view, name='patientview'),
    # Doctor can view a selected patient's info
    url(r'^patients/details/$', views.doctor.patient_details,
        name='patientdetails'),

    # Two urls- one for doctor and one for patient adding medication...for now addMedication is general (for patient)
    url(r'^addMedicationDoc/$', views.medications.addMedicationDoc, name='addMedicationDoc'),
    url(r'^addMedication/$', views.medications.addMedicationPat, name='addMedicationPat'),
    # Remove medication
    url(r'^removeMedication/$', views.medications.removeMedication, name='removeMedication'),
    # Edit existing medications
    url(r'^editMedication/$', views.medications.editMedication, name='editMedication'),
    # View existing medications
    url(r'^home-patient/$', views.medications.viewMedication, name='home-patient')
]