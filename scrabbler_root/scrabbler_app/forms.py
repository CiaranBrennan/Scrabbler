from django import forms
from django.forms import ModelForm
from .models import Match, Player

class DateInput(forms.DateInput):
    input_type = 'date'

class EditPlayerForm(forms.Form):
    forename  = forms.CharField  (label="Forename", max_length=30, required=False)
    surname   = forms.CharField  (label="Surname", max_length=30, required=False)

class CreatePlayerForm(forms.Form):
    forename   = forms.CharField  (label="Forename", required=True, max_length=30)
    surname    = forms.CharField  (label="Surname", required=True, max_length=30)

class MatchPlayerForm(forms.Form):
    #Define initial fields
    name     = forms.ModelChoiceField(label="Player", required=True, queryset=Player.objects.all().order_by("surname"))
    score    = forms.IntegerField (label="Score", required=True)


class MatchModelForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["datePlayed", "comments"]
        widgets = {
            'datePlayed': DateInput()
        }