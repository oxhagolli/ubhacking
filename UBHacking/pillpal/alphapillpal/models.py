from django.db import models
from django.contrib.auth.models import User

import json
from django.core.validators import RegexValidator


#will store phone number(s) of people
class PhoneModel(models.Model):
    patient = models.ForeignKey(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True) # validators should be a list


#will store user's medications. can have more than one
class Medication(models.Model):
    patient = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    time = models.TextField(null=True) #JSON-serialized. values of times of the day (list of timefields)
    days = models.TextField(null=True) #JSON-serialized (text) version of list; will hold days of week

    def get_times(self):
        jsonDec = json.JSONDecoder()
        lst = jsonDec.decode(self.time)

        str1 = ""
        for index, item in enumerate(lst):
            str1 += str(item)
            if item != len(lst)-1:
                str1 += ", "
        return str1[:len(str1)-2]

    def get_days(self):
        jsonDec = json.JSONDecoder()
        lst = jsonDec.decode(self.days)

        str1 = ""
        for index, item in enumerate(lst):
            str1 += str(item)
            if item != len(lst)-1:
                str1 += ", "
        return str1[:len(str1)-2]
