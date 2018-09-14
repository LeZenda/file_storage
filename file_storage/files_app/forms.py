from django import forms
from files_app.models import Document


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        exclude = ('user',)
        # fields = '__all__'
