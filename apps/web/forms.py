#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import *
from django.core.exceptions import ValidationError
from ..labels import *
from .choices import *
from .models import *


class MetadataForm(ModelForm):
    class Meta:
        model = MetaDataWeb
        fields = ['origin', 'm_title_a', 'm_title_f', 'm_description_a', 'm_description_f']

    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs) 

        for key in self.fields.keys():
            field = self.fields[key]
            field.widget.attrs['class'] = 'form-control'
                