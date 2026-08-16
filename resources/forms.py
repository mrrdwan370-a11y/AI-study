from django import forms
from .models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:

        model = Resource

        fields = [
            "title",
            "description",
            "link",
            "resource_type",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Resource title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe this resource..."
                }
            ),

            "link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com"
                }
            ),

            "resource_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }