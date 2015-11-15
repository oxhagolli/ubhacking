from django.db import models
from django.contrib.auth.models import User

import json

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
        return str1

    def get_days(self):
        jsonDec = json.JSONDecoder()
        lst = jsonDec.decode(self.days)

        str1 = ""
        for index, item in enumerate(lst):
            str1 += str(item)
            if item != len(lst)-1:
                str1 += ", "
        return str1