from django import forms
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.forms import formset_factory
from .models import Match, MatchScore

class EditForm(forms.Form):
    forename  = forms.CharField  (label="Forename", max_length=30, required=False)
    surname   = forms.CharField  (label="Surname", max_length=30, required=False)
    email     = forms.EmailField (label="Email", required=False)

class CreateForm(forms.Form):
    forename   = forms.CharField  (label="Forename", max_length=30)
    surname    = forms.CharField  (label="Surname", max_length=30)
    email      = forms.EmailField (label="Email")
    dateJoined = forms.DateField  (label="Date joined")

# class AddMatchForm(forms.Form):
#     #Define initial fields
#     forename = forms.CharField (label="Forename", max_length=30, required=True)
#     surname = forms.CharField (label="Surname", max_length=30, required=True)
#     score = forms.IntegerField (label="Score", required=True)

#     def get_player_fields(self):
#         for field_name in self.fields:
#             if field_name.startswith(‘interest_’):
#                 yield self[field_name]

class AddMatchForm(forms.Form):
    #Define initial fields
    forename = forms.CharField (label="Forename", max_length=30, required=True)
    surname = forms.CharField (label="Surname", max_length=30, required=True)
    score = forms.IntegerField (label="Score", required=True)

AddMatchFormSet = formset_factory(AddMatchForm, extra=0, min_num=2, max_num=4, can_delete=True)