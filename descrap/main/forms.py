from django import forms
from .models import Document
class docform(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name','image')