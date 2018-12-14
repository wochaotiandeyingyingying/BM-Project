from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login

import re

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",widget=forms.TextInput(attrs={'class':'form-control','placeholder': '请输入用户名'}))

    password = forms.CharField(label="密码",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': '请输入密码'}))

    class Meta:
        model = get_user_model()
        fields = ("username", "password")

    # def clean(self):
    #     username=self.cleaned_data['username']
    #     password=self.cleaned_data['password']
    #     user=authenticate(username=username,password=password)
    #     if user is None:
    #         raise  forms.ValidationError('用户名或密码不正确')
    #     else:
    #         self.cleaned_data['user']=user
    #     return self.cleaned_data






