from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm, ChangePasswordForm

from tasks.models import Task
from notes.models import Note
from resources.models import Resource
from .forms import RegisterForm


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )

@login_required
def profile(request):

    user = request.user

    total_tasks = Task.objects.filter(
        user=user
    ).count()

    total_notes = Note.objects.filter(
        user=user
    ).count()

    total_resources = Resource.objects.filter(
        user=user
    ).count()

    context = {
        "profile_user": user,
        "total_tasks": total_tasks,
        "total_notes": total_notes,
        "total_resources": total_resources,
    }

    return render(
        request,
        "accounts/profile.html",
        context
    )


@login_required
def profile_edit(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully!"
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/profile_edit.html",
        {
            "form": form
        }
    )


@login_required
def change_password(request):

    if request.method == "POST":

        form = ChangePasswordForm(
            request.POST
        )

        if form.is_valid():

            old_password = form.cleaned_data[
                "old_password"
            ]

            new_password = form.cleaned_data[
                "new_password"
            ]

            if not request.user.check_password(
                old_password
            ):

                form.add_error(
                    "old_password",
                    "Current password is incorrect."
                )

            else:

                request.user.set_password(
                    new_password
                )

                request.user.save()

                update_session_auth_hash(
                    request,
                    request.user
                )

                messages.success(
                    request,
                    "Password changed successfully!"
                )

                return redirect("profile")

    else:

        form = ChangePasswordForm()

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form
        }
    )