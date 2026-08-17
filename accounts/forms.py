# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import (
#     UserCreationForm,
#     AuthenticationForm,
#     PasswordChangeForm,
# )
# from .models import Profile


# class RegisterForm(UserCreationForm):

#     email = forms.EmailField(
#         required=True
#     )

#     first_name = forms.CharField(
#         max_length=50,
#         required=True
#     )

#     last_name = forms.CharField(
#         max_length=50,
#         required=True
#     )

#     class Meta:
#         model = User

#         fields = [
#             "first_name",
#             "last_name",
#             "username",
#             "email",
#             "password1",
#             "password2",
#         ]

#     def clean_email(self):
#         email = self.cleaned_data["email"]

#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError(
#                 "This email is already registered."
#             )

#         return email

# from django import forms
# from django.contrib.auth.models import User


# from django import forms
# from django.contrib.auth.models import User
# from .models import Profile


# class ProfileForm(forms.ModelForm):

#     class Meta:
#         model = User

#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#         ]

#         widgets = {
#             "first_name": forms.TextInput(attrs={
#                 "class": "form-control",
#                 "placeholder": "First Name"
#             }),

#             "last_name": forms.TextInput(attrs={
#                 "class": "form-control",
#                 "placeholder": "Last Name"
#             }),

#             "email": forms.EmailInput(attrs={
#                 "class": "form-control",
#                 "placeholder": "Email Address"
#             }),
#         }


# class ProfileImageForm(forms.ModelForm):

#     class Meta:
#         model = Profile

#         fields = ["avatar"]

#         widgets = {
#             "profile_image": forms.FileInput(attrs={
#                 "class": "form-control",
#                 "accept": "image/*"
#             })
#         }

# class ChangePasswordForm(forms.Form):

#     old_password = forms.CharField(
#         label="Current Password",
#         widget=forms.PasswordInput(attrs={
#             "class": "form-control",
#             "placeholder": "Current password"
#         })
#     )

#     new_password = forms.CharField(
#         label="New Password",
#         widget=forms.PasswordInput(attrs={
#             "class": "form-control",
#             "placeholder": "New password"
#         })
#     )

#     confirm_password = forms.CharField(
#         label="Confirm New Password",
#         widget=forms.PasswordInput(attrs={
#             "class": "form-control",
#             "placeholder": "Confirm new password"
#         })
#     )

#     def clean(self):

#         cleaned_data = super().clean()

#         new_password = cleaned_data.get("new_password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if new_password and confirm_password:

#             if new_password != confirm_password:
#                 raise forms.ValidationError(
#                     "New passwords do not match."
#                 )

#         return cleaned_data

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


# ==========================================
# Register Form
# ==========================================

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    first_name = forms.CharField(
        max_length=50,
        required=True
    )

    last_name = forms.CharField(
        max_length=50,
        required=True
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email


# ==========================================
# Profile Information Form
# ==========================================

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First Name"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last Name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address"
            }),
        }


# ==========================================
# Profile Image Form
# ==========================================

class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "avatar"
        ]

        widgets = {
            "avatar": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            })
        }


# ==========================================
# Change Password Form
# ==========================================

class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Current password"
        })
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "New password"
        })
    )

    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm new password"
        })
    )

    def clean(self):

        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:

            if new_password != confirm_password:
                raise forms.ValidationError(
                    "New passwords do not match."
                )

        return cleaned_data