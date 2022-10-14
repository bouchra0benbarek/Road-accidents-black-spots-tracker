# -*- coding: utf-8 -*-



from contextlib import nullcontext
from datetime import date
from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from pickle import TRUE
from pyexpat import model
from sys import flags
from time import time
from turtle import title
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import os


# Create your models here.
class caneva(models.Model):
    id_caneva = models.BigIntegerField(primary_key=True, null=False)
    title = models.TextField()
    year = models.IntegerField(default=2022)
    trimestre = models.TextField()
    wilaya = models.TextField()
    total_acc = models.IntegerField(default=0)
    total_dead = models.IntegerField(default=0)
    total_injured = models.IntegerField(default=0)
    total_PN = models.IntegerField(default=0)


class wilaya(models.Model):
    id_wilaya = models.BigIntegerField(primary_key=True, null=False)
    name_wilaya = models.TextField()
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)
    def getName(self):
        return self.name_wilaya

    
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('images/', filename) 

class BlackSpot(models.Model):
    point_noir = models.CharField(max_length=400, null=False)
    commune = models.CharField(max_length=400, null=False)
    localisation = models.CharField(max_length=600, null=False)
    valeur_pk = models.CharField(max_length=400, null=False)
    gps = models.FloatField()
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)
    nb_accidents = models.IntegerField()
    nb_blesses = models.IntegerField()
    nb_tues = models.IntegerField()
    causes = models.TextField()
    mesures = models.TextField()
    observations = models.TextField()
    images = models.ImageField( upload_to = filepath ,null=True, blank=True)

    caneva_id = models.ForeignKey(caneva, on_delete=models.CASCADE, null=False)
    



class report(models.Model):
    id_report = models.BigIntegerField(primary_key = TRUE, null = False)
    report_title = models.TextField()





