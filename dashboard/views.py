from django.contrib.auth.decorators import login_required
from django.db.models import Count 
from django.shortcuts import render
from tasks.models import Task
from notes.models import Note
from resources.models import Resource
from .models import Activity

@login_required
def dashboard_view(request):
    user = request.user
    total_tasks = Task.objects.filter( user=user).count()
    completed_tasks = Task.objects.filter( user=user,status="COMPLETED").count()
    pending_tasks = Task.objects.filter( user=user, status="PENDING" ).count()
    total_notes = Note.objects.filter( user=user).count()
    total_resources = Resource.objects.filter( user=user ).count()
    recent_activities = Activity.objects.filter( user=user)[:6]
    upcoming_tasks = Task.objects.filter(  user=user ).exclude( status="COMPLETED").order_by("due_date")[:5]
    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_notes": total_notes,
        "total_resources": total_resources,
        "recent_activities": recent_activities,
        "upcoming_tasks": upcoming_tasks,
    }
    return render( request, "dashboard/dashboard.html", context )