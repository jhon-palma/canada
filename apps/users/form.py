from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Form
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectMultiple

from apps.accounts.models import CustomUser
from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'is_active']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'order', 'type_user', 'membre','occupation', 'occupation_anglaise', 'facebook', 'instagram', 'linkedin', 'twitter']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2','first_name', 'last_name')
    
    # def save(self, commit=True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     user.username = self.cleaned_data["email"] 
    #     if commit:
    #         user.save()
    #     return user