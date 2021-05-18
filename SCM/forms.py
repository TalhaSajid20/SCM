from django import forms
from .models import SCM1


class SCMModelForm(forms.ModelForm):
    class Meta:
        model = SCM1
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
        )



class SCMform(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)