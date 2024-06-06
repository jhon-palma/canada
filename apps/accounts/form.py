#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, Form
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectMultiple

from django.contrib.auth.models import User
from ..users.models import *



class UpdateUsersForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['cellphone','telephone','password']

    def __init__(self, request, *args, **kwargs):
        super(UpdateUsersForm, self).__init__(*args, **kwargs)
        required = ['password']
        
        for key in self.fields.keys():
            field = self.fields[key]
            field.widget.attrs['class'] = 'form-control'
            if key in required:
                field.widget.attrs['required'] = True
                
