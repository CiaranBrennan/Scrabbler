from django import forms

class EditForm(forms.Form):
    firstName = forms.CharField (label="First name", max_length=30, required=False)
    surname   = forms.CharField (label="Surname", max_length=30, required=False)
    email     = forms.EmailField(label="Email", required=False)

class CreateForm(forms.Form):
    firstName  = forms.CharField (label="First name", max_length=30)
    surname    = forms.CharField (label="Surname", max_length=30)
    email      = forms.EmailField(label="Email")
    dateJoined = forms.DateField (label="Date joined")
