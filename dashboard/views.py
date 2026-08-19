from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tasks.models import Task
from notes.models import Note
from resources.models import Resource
from .models import Activity


@login_required
def dashboard_view(request):

    user = request.user

    # ==========================================
    # TASK STATISTICS
    # ==========================================

    total_tasks = Task.objects.filter(
        user=user
    ).count()

    completed_tasks = Task.objects.filter(
        user=user,
        status="COMPLETED"
    ).count()

    pending_tasks = Task.objects.filter(
        user=user,
        status="PENDING"
    ).count()

    in_progress_tasks = Task.objects.filter(
        user=user,
        status="IN_PROGRESS"
    ).count()


    # ==========================================
    # TASK PRIORITY
    # ==========================================

    high_priority_tasks = Task.objects.filter(
        user=user,
        priority="HIGH"
    ).count()

    medium_priority_tasks = Task.objects.filter(
        user=user,
        priority="MEDIUM"
    ).count()

    low_priority_tasks = Task.objects.filter(
        user=user,
        priority="LOW"
    ).count()


    # ==========================================
    # NOTES & RESOURCES
    # ==========================================

    total_notes = Note.objects.filter(
        user=user
    ).count()

    total_resources = Resource.objects.filter(
        user=user
    ).count()


    # ==========================================
    # RECENT ACTIVITY
    # ==========================================

    recent_activities = Activity.objects.filter(
        user=user
    ).order_by("-created_at")[:6]


    # ==========================================
    # UPCOMING TASKS
    # ==========================================

    upcoming_tasks = Task.objects.filter(
        user=user
    ).exclude(
        status="COMPLETED"
    ).order_by("due_date")[:5]


    # ==========================================
    # DASHBOARD CONTEXT
    # ==========================================

    context = {

        # ------------------------------
        # Statistics
        # ------------------------------

        "total_tasks": total_tasks,

        "completed_tasks": completed_tasks,

        "pending_tasks": pending_tasks,

        "in_progress_tasks": in_progress_tasks,

        "total_notes": total_notes,

        "total_resources": total_resources,


        # ------------------------------
        # Priority
        # ------------------------------

        "high_priority_tasks": high_priority_tasks,

        "medium_priority_tasks": medium_priority_tasks,

        "low_priority_tasks": low_priority_tasks,


        # ------------------------------
        # Activity
        # ------------------------------

        "recent_activities": recent_activities,

        "upcoming_tasks": upcoming_tasks,
    }


    return render(
        request,
        "dashboard/dashboard.html",
        context
    )