from django import forms
from manage_worksheets.models import Tag

class SubmissionForm(forms.Form):
    url = forms.URLField(max_length=200, label="URL:", attrs={'class': 'form-control'})
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all(), attrs={'class': 'list-inline list-unstyled form-control'})

class ChooseTagsForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all(), attrs={'class': 'list-inline list-unstyled form-control'})
    worksheet_id = forms.CharField(widget=forms.HiddenInput, attrs={'class': 'form-control'})
