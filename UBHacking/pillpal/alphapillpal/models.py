from django.db import models
from django.contrib.auth.models import User

#will store user's medications. can have more than one
class Medication(models.Model):
    patient = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    time = models.TimeField()
    days = models.TextField(null=True) #JSON-serialized (text) version of list; will hold days of week