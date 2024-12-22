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
        fields = ['origin', 'meta_title_a', 'meta_title_f', 'meta_description_a', 'meta_description_f']

    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs) 

        for key in self.fields.keys():
            field = self.fields[key]
            field.widget.attrs['class'] = 'form-control'
                