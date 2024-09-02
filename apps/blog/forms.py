from django import forms
from .models import Category, Comment
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article

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
          self.fields["content_francaise"].required = False
          self.fields["content_anglaise"].required = False

      class Meta:
          model = Article
          fields = ('title_francaise','category','content_francaise', 'content_anglaise', 'image')
          widgets = {
              "content_francaise": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              ),
              "content_anglaise": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              ),
          }