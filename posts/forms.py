from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'email', 'body']
        widgets = {
            'author': forms.TextInput(attrs={
                'id': 'author',
                'placeholder': 'Name *',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'placeholder': 'Your@email.com',
            }),
            'body': forms.Textarea(attrs={
                'id': 'comment',
                'placeholder': 'Your Comment',
                'rows': 5,
                'required': True,
            }),
        }
