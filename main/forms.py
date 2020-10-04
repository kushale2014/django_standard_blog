from django import forms
from .models import Article
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('img', 'name', 'text')
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'


class AuthUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
