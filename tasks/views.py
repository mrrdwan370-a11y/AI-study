from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import TaskForm
from .models import Task
from dashboard.models import Activity


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        user=request.user
    )

    search = request.GET.get(
        "search",
        ""
    )

    status = request.GET.get(
        "status",
        ""
    )

    priority = request.GET.get(
        "priority",
        ""
    )

    if search:

        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if status:
        tasks = tasks.filter(
            status=status
        )

    if priority:
        tasks = tasks.filter(
            priority=priority
        )

    paginator = Paginator(
        tasks,
        8
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {
        "page_obj": page_obj,
        "search": search,
        "selected_status": status,
        "selected_priority": priority,
        "status_choices": Task.STATUS_CHOICES,
        "priority_choices": Task.PRIORITY_CHOICES,
    }

    return render(
        request,
        "tasks/task_list.html",
        context
    )


@login_required
def task_create(request):

    if request.method == "POST":

        form = TaskForm(
            request.POST
        )

        if form.is_valid():

            task = form.save(
                commit=False
            )

            task.user = request.user

            task.save()

            Activity.objects.create(
                user=request.user,
                action="Task Created",
                description=f"Created task: {task.title}"
            )

            messages.success(
                request,
                "Task created successfully!"
            )

            return redirect(
                "tasks_list"
            )

    else:

        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "page_title": "Create Task",
            "button_text": "Create Task",
        }
    )


@login_required
def task_update(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            task = form.save()

            Activity.objects.create(
                user=request.user,
                action="Task Updated",
                description=f"Updated task: {task.title}"
            )

            messages.success(
                request,
                "Task updated successfully!"
            )

            return redirect(
                "tasks_list"
            )

    else:

        form = TaskForm(
            instance=task
        )

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "page_title": "Edit Task",
            "button_text": "Save Changes",
            "task": task,
        }
    )


@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        title = task.title

        task.delete()

        Activity.objects.create(
            user=request.user,
            action="Task Deleted",
            description=f"Deleted task: {title}"
        )

        messages.success(
            request,
            "Task deleted successfully!"
        )

        return redirect(
            "tasks_list"
        )

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task": task
        }
    )


@login_required
def task_complete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        if task.status == "COMPLETED":

            task.status = "PENDING"

            message = "Task marked as pending."

        else:

            task.status = "COMPLETED"

            message = "Task completed successfully!"

        task.save()

        Activity.objects.create(
            user=request.user,
            action="Task Status Updated",
            description=f"{task.title}: {task.get_status_display()}"
        )

        messages.success(
            request,
            message
        )

    return redirect(
        "tasks_list"
    )