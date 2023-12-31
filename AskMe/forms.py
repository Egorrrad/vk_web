from django import forms
from django.contrib.auth.models import User


class QuestionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "col-9 pole_for_question"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "col-9 pole_for_question"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "col-9 pole_for_question"}))


class AddAnswerForm(forms.Form):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={"class": "col-9 pole_for_question", "placeholder": "Enter your answer here"}))


class SettingsForm(forms.Form):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={"class": "col-9 pole_for_log"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "col-9 pole_for_log"}))
    first_name = forms.CharField(label="NickName", widget=forms.TextInput(attrs={"class": "col-9 pole_for_log"}))

    image = forms.ImageField(required=False, label="Upload avatar", widget=forms.FileInput(attrs={"class": "col-9"}))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={"class": "col-9 pole_for_log"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "col-9 pole_for_log"}))
    first_name = forms.CharField(label="NickName", widget=forms.TextInput(attrs={"class": "col-9 pole_for_log"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "col-9 pole_for_log"}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={"class": "col-9 pole_for_log"}))

    image = forms.ImageField(required=False, label="Upload avatar", widget=forms.FileInput(attrs={"class": "col-9"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={"class": "col-9 pole_for_log"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "col-9 pole_for_log"}))
