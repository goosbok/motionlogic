from django.db import models

class Restaurants(models.Model):
    name_corp = models.CharField(max_length=50, db_index= True)
    name_in_corp_sys = models.CharField(max_length=250, default='None')
    city = models.CharField(max_length=50, db_index= True)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.name_corp + self.name_in_corp_sys
