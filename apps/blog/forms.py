from django import forms
from .models import Category, Comment
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article
from .validators import *



class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title_anglaise', 'title_francaise')
    
    def clean(self): 
        cleaned_data = super().clean()
        CategoryValidator(self) 
        return self.cleaned_data



class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content_francaise"].required = False
        self.fields["content_anglaise"].required = False
        self.fields["title_francaise"].widget.attrs.update({"class": "form-control"})
        self.fields["title_anglaise"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["image_francaise"].widget.attrs.update({"class": "form-control-file"})
        self.fields["image_anglaise"].widget.attrs.update({"class": "form-control-file"})
        self.fields["slug_francaise"].widget.attrs.update({"class": "form-control"})
        self.fields["slug_anglaise"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_title_a"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_title_f"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_description_a"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_description_f"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Article
        fields = ['title_francaise', 'title_anglaise', 'category','content_francaise', 'content_anglaise', 'image_francaise', 'image_anglaise', 'slug_francaise', 'slug_anglaise', 'meta_title_a','meta_title_f','meta_description_a','meta_description_f']
        widgets = {
            "content_francaise": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
            "content_anglaise": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
        }



class ArticleUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content_francaise"].required = False
        self.fields["content_anglaise"].required = False
        self.fields["title_francaise"].widget.attrs.update({"class": "form-control"})
        self.fields["title_anglaise"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["image_francaise"].widget.attrs.update({"class": "form-control-file"})
        self.fields["image_anglaise"].widget.attrs.update({"class": "form-control-file"})
        self.fields["slug_francaise"].widget.attrs.update({"class": "form-control"})
        self.fields["slug_anglaise"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_title_a"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_title_f"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_description_a"].widget.attrs.update({"class": "form-control"})
        self.fields["meta_description_f"].widget.attrs.update({"class": "form-control"})


    class Meta:
        model = Article
        fields = ['title_francaise', 'title_anglaise', 'category','content_francaise', 'content_anglaise', 'image_francaise', 'image_anglaise', 'slug_francaise', 'slug_anglaise', 'meta_title_a','meta_title_f','meta_description_a','meta_description_f']
        widgets = {
            "content_francaise": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
            "content_anglaise": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
        }