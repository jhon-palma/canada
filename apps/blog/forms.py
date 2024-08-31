from django import forms
from .models import Category, Comment
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','category','content','image')
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="post"
            )
        }

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title_anglaise', 'title_francaise')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'champs_tem',
                'placeholder':'*Commentaires',
                'id': 'comment', 
            }),
        }

class ArticleForm(forms.ModelForm):
      """Form for comments to the article."""

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["content"].required = False

      class Meta:
          model = Article
          fields = ('title','category','content','image')
          widgets = {
              "content": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              )
          }