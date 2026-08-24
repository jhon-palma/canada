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
        # origin queda fuera a proposito: identifica la pagina a la que
        # pertenece la fila, no es contenido que se edite. Se enviaba en un
        # <select> oculto de update.html y bastaba con que llegase con otro
        # valor para reescribir la clave: asi 'sell' se quedo sin fila y
        # 'properties' con dos, y las dos paginas pasaron a dar 500.
        fields = ['m_title_a', 'm_title_f', 'm_description_a', 'm_description_f']

    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs) 

        for key in self.fields.keys():
            field = self.fields[key]
            field.widget.attrs['class'] = 'form-control'
                