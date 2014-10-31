from django import forms
from manage_worksheets.models import Tag

class SubmissionForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(
            attrs={'class': 'form-control'}),
            max_length=200,
            label="Adresse (URL)"
            )

    tags = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
            queryset=Tag.objects.all(),
            label="Schlagworte",
            required=False           # choosing tags is not mandatory
            )

class ChooseTagsForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
            queryset=Tag.objects.all(),
            label="Schlagworte",
            required=False
            )
    def __init__(self, *args, **kwargs):
        worksheet = kwargs.pop('worksheet', None)
        #del kwargs['worksheet']
        super(ChooseTagsForm, self).__init__(*args, **kwargs)
        if worksheet:
            self.initial['tags'] = [t.pk for t in worksheet.tags.all()]

