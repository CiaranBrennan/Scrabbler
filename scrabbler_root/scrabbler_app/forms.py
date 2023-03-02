from django import forms
from django.forms import ModelForm
from .models import Match

class DateInput(forms.DateInput):
    input_type = 'date'

class EditForm(forms.Form):
    forename  = forms.CharField  (label="Forename", max_length=30, required=False)
    surname   = forms.CharField  (label="Surname", max_length=30, required=False)
    email     = forms.EmailField (label="Email", required=False)

class CreateForm(forms.Form):
    forename   = forms.CharField  (label="Forename", max_length=30)
    surname    = forms.CharField  (label="Surname", max_length=30)
    email      = forms.EmailField (label="Email")
    dateJoined = forms.DateField  (label="Date joined")

class MatchPlayerForm(forms.Form):
    #Define initial fields
    forename = forms.CharField    (label="Forename", max_length=30, required=True)
    surname  = forms.CharField    (label="Surname", max_length=30, required=True)
    score    = forms.IntegerField (label="Score", required=True)


class MatchModelForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["datePlayed", "comments"]
        widgets = {
            'datePlayed': DateInput()
        }