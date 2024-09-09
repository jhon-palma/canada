from django import forms
from .models import Category, Comment
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title_anglaise', 'title_francaise')

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

    class Meta:
        model = Article
        fields = ('title_francaise', 'title_anglaise', 'category','content_francaise', 'content_anglaise', 'image_francaise', 'image_anglaise')
        widgets = {
            "content_francaise": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
            "content_anglaise": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
        }