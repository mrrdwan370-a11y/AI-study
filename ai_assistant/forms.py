from django import forms


class ChatForm(forms.Form):

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Ask AI anything about your studies..."
            }
        )
    )