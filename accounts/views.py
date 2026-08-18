from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import  RegisterForm, ProfileForm, ProfileImageForm, ChangePasswordForm
from .models import Profile
from tasks.models import Task
from notes.models import Note
from resources.models import Resource

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create( user=user)
            login(request, user)
            messages.success( request, "Account created successfully!" )
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render( request,"accounts/register.html", { "form": form } )

@login_required
def profile(request):
    user = request.user
    profile_obj, created = Profile.objects.get_or_create( user=user )
    total_tasks = Task.objects.filter( user=user ).count()
    total_notes = Note.objects.filter( user=user ).count()
    total_resources = Resource.objects.filter( user=user ).count()
    context = {
        "profile_user": user,
        "profile": profile_obj,
        "total_tasks": total_tasks,
        "total_notes": total_notes,
        "total_resources": total_resources,
    }
    return render( request, "accounts/profile.html", context )

@login_required
def profile_edit(request):
    profile_obj, created = Profile.objects.get_or_create( user=request.user )
    if request.method == "POST":
        form = ProfileForm(  request.POST, instance=request.user )
        image_form = ProfileImageForm(  request.POST, request.FILES, instance=profile_obj )
        if form.is_valid() and image_form.is_valid():
            form.save()
            image_form.save()
            messages.success(  request,  "Profile updated successfully!" )
            return redirect("profile")
    else:
        form = ProfileForm( instance=request.user )
        image_form = ProfileImageForm( instance=profile_obj )
    return render( request, "accounts/profile_edit.html",
        {
            "form": form,
            "image_form": image_form,
            "profile": profile_obj,
        } )

@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm( request.POST )
        if form.is_valid():
            old_password = form.cleaned_data[ "old_password" ]
            new_password = form.cleaned_data[  "new_password" ]
            if not request.user.check_password( old_password ):
                form.add_error( "old_password",  "Current password is incorrect." )
            else:
                request.user.set_password( new_password )
                request.user.save()
                update_session_auth_hash( request, request.user )
                messages.success( request, "Password changed successfully!" )
                return redirect("profile")
    else:
        form = ChangePasswordForm()
    return render(  request, "accounts/change_password.html",  {  "form": form  } )