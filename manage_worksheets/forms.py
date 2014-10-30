from django import forms
from manage_worksheets.models import Tag

class SubmissionForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), max_length=200, label="Adresse (URL)")
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': ''}), queryset=Tag.objects.all(), label="Schlagworte")
    
class ChooseTagsForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': ''}), queryset=Tag.objects.all(), label="Schlagworte")
    worksheet_id = forms.CharField(widget=forms.HiddenInput)