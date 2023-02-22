from django import forms

class EditForm(forms.Form):
    forename  = forms.CharField  (label="Forename", max_length=30, required=False)
    surname   = forms.CharField  (label="Surname", max_length=30, required=False)
    email     = forms.EmailField (label="Email", required=False)

class CreateForm(forms.Form):
    forename   = forms.CharField  (label="Forename", max_length=30)
    surname    = forms.CharField  (label="Surname", max_length=30)
    email      = forms.EmailField (label="Email")
    dateJoined = forms.DateField  (label="Date joined")

class AddMatchForm(forms.Form):
    fname1 = forms.CharField (label="Forename", max_length=30, required=True)
    sname1 = forms.CharField (label="Surname", max_length=30, required=True)
    score1 = forms.IntegerField (label="Score", required=True)
    fname2 = forms.CharField (label="Forename", max_length=30, required=True)
    sname2 = forms.CharField (label="Surname", max_length=30, required=True)
    score2 = forms.IntegerField (label="Score", required=True)
