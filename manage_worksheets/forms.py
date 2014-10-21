from django import forms
from manage_worksheets.models import Tag

class SubmissionForm(forms.Form):
    url = forms.URLField(max_length=200, label="URL:")
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all())

class ChooseTagsForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all())
    worksheet_id = forms.CharField(widget=forms.HiddenInput)
