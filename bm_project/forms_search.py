from django import forms
from django.contrib.auth import get_user_model

class SearchForm(forms.Form):
    materialid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入mp-id'}))
