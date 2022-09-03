from django.forms import ModelForm, Textarea
from .models import Post, Comment
from django_ckeditor_5.widgets import CKEditor5Widget


class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Post
        fields = ['category', 'title', 'content']
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            "content": "",
        }
        widgets = {
                'content': Textarea(attrs={'cols': 40, 'rows': 4}),
            }