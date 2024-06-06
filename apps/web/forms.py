#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import *
from django.core.exceptions import ValidationError

from ..parametrization.forms import *
from ..vars import *
from ..functions import *
from ..labels import *
from .list import *
from .choices import *
from .models import *



class WebPQRForm(ModelForm):
    class Meta:
        model = WebPQR
        fields = ['type_request','first_name','last_name','email','telephone','indicative','cellphone','detail']
        
    def __init__(self, *args, **kwargs):
        super(WebPQRForm, self).__init__(*args, **kwargs)
        
        for key in self.fields.keys():
            field = self.fields[key]
            field.widget.attrs['class'] = 'form-control __bor'

            if key == 'indicative':
                field.widget.attrs['title'] = 'Selecciona una Opción'
                field.widget.attrs['class'] = 'form-control  __bor selectpicker'
                field.widget.attrs['data-live-search'] = 'true'
                field.widget.attrs['data-size'] = '5'
            
            if key in web_numbers:
                field.widget.attrs['onkeypress'] = 'OnlyNumbers(event)'
                field.widget.attrs['class'] = 'form-control __bor'

    def clean(self): 
        return self.cleaned_data

