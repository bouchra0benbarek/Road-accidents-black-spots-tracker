from dataclasses import field, fields
from importlib.metadata import files
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import BlackSpot

class BlackSpotForm(ModelForm):
    class Meta:
        model = BlackSpot
        fields = '__all__'