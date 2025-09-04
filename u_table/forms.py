from . import models
from django import forms

class InfoForm(forms.ModelForm):
    class Meta:
        model = models.InfoTable
        fields='__all__'
class UpdatedInfoForm(forms.ModelForm):
    class Meta:
        model = models.UpdatedInfoTable
        fields = '__all__'

