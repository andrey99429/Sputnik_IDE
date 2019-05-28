from django import forms

attrs = {'class': 'form-control', 'autocomplete': 'off'}


class Project_Form(forms.Form):
    name = forms.CharField(label='Название', max_length=50, widget=forms.TextInput(attrs=attrs))
