from django import forms


def CategoryValidator(instance):
    category_eng = instance.cleaned_data.get('title_anglaise')
    category_fr = instance.cleaned_data.get('title_francaise')
    if category_eng == category_fr:
        errors = {
            'title_anglaise': 'Los títulos no pueden ser iguales'
        }
        raise forms.ValidationError(errors)
