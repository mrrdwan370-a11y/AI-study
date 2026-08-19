from django import forms
from .models import Note, Category, Tag

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [ "title", "content", "category", "tags", "image", "is_favorite", ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter note title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 10,
                "placeholder": "Write your note..."
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "tags": forms.SelectMultiple(attrs={
                "class": "form-select",
                "size": 5
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "is_favorite": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user )
            self.fields["tags"].queryset = Tag.objects.filter(user=user )
            
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [ "name", "description", ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Category name"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Category description"
            }),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Tag name"
            }),
        }