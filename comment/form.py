from django import forms
from ckeditor.widgets import CKEditorWidget


class CommentText(forms.Form):
    comment_text = forms.CharField(label="",widget=CKEditorWidget())