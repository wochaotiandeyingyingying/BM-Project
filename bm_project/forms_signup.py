from django import forms
from django.contrib.auth import get_user_model

import re


def lowercase_email(email):
    """
    Normalize the address by lowercasing the domain part of the email
    address.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = '@'.join([email_name.lower(), domain_part.lower()])
    return email

class SignupForm(forms.ModelForm):
    username = forms.CharField(
        label='用户名', required=True,
        error_messages={'required': 'Please fill in your username', 'max_length': 'Can only enter up to 15 characters', 'min_length': 'Enter at least 3 characters'}, max_length=15,
        min_length=3, widget=forms.TextInput(attrs={'class':'form-control','placeholder': '3~15 letters/numbers/Chinese characters'}))
    email = forms.EmailField(error_messages={'required': 'Please fill in your email', 'invalid': 'Email format is incorrect'},
                             label='邮箱', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fill in the correct email to activate your account'}))
    password = forms.CharField(
        error_messages={'required': 'Please enter your password', 'max_length': 'Can only enter up to 20 characters', 'min_length': 'Enter at least 6 characters'},
        label='密码', required=True, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'The length is within 6~20 characters'}))
    confirm_password = forms.CharField(
        error_messages={'required': 'Please fill in your password', 'max_length': 'Can only enter up to 20 characters', 'min_length': 'Enter at least 6 characters'},
        label='确认密码', required=True, max_length=20, min_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'The length is within 6~20 characters'}))

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password",)

    def clean_email(self):
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        lower_email = lowercase_email(email)
        try:
            UserModel._default_manager.get(email=lower_email)
        except UserModel.DoesNotExist:
            return lower_email
        raise forms.ValidationError("有人已经注册了这个email地址")

    def clean_confirm_password(self):
        # cleaned_data=super(SignupForm,self).clean()
        password = self.cleaned_data.get("password", False)
        confirm_password = self.cleaned_data["confirm_password"]
        if not (password == confirm_password):
            raise forms.ValidationError("确认密码和密码不一致")
        return confirm_password

    def clean_username(self):
        UserModel = get_user_model()
        username = self.cleaned_data["username"]
        # 过滤用户名敏感词的注册用户
        n = re.sub('[^\u4e00-\u9fa5a-zA-Z]', '', username)

        mgc = ['admin']

        if n in mgc:
            raise forms.ValidationError("换一个试试^-^")

        try:
            UserModel._default_manager.get(username=username)

        except UserModel.DoesNotExist:
            return username
        raise forms.ValidationError("有人已经注册了这个用户名")
