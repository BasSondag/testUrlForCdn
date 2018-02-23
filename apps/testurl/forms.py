from django import forms

class AddUrlForm(forms.Form):
    Add_URL = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
