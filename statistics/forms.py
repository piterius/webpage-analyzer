from django import forms


class URLForm(forms.Form):
    url = forms.URLField(label='Please enter URL to check', max_length=100)
