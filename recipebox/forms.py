from django import forms
from recipebox.models import Author


class NewRecipeAddForm(forms.Form):
    title = forms.CharField(max_length=100)
    authors = [(a.id, a.name) for a in Author.objects.all()]
    author = forms.ChoiceField(choices=authors)
    description = forms.CharField(max_length=300)
    time = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
