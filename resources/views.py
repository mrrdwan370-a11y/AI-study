from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .models import Resource
from .forms import ResourceForm
from dashboard.models import Activity


@login_required
def resources_list(request):

    resources = Resource.objects.filter(
        user=request.user
    )

    search = request.GET.get(
        "search",
        ""
    )

    resource_type = request.GET.get(
        "type",
        ""
    )

    if search:

        resources = resources.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if resource_type:

        resources = resources.filter(
            resource_type=resource_type
        )

    resources = resources.order_by(
        "-created_at"
    )

    paginator = Paginator(
        resources,
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
        "selected_type": resource_type,
        "resource_types": Resource.RESOURCE_TYPES,
    }

    return render(
        request,
        "resources/resources_list.html",
        context
    )


@login_required
def resource_create(request):

    if request.method == "POST":

        form = ResourceForm(
            request.POST
        )

        if form.is_valid():

            resource = form.save(
                commit=False
            )

            resource.user = request.user

            resource.save()

            Activity.objects.create(
                user=request.user,
                action="Resource Created",
                description=f"Added resource: {resource.title}"
            )

            messages.success(
                request,
                "Resource added successfully!"
            )

            return redirect(
                "resources_list"
            )

    else:

        form = ResourceForm()

    return render(
        request,
        "resources/resource_form.html",
        {
            "form": form,
            "page_title": "Add Resource",
            "button_text": "Add Resource",
        }
    )


@login_required
def resource_detail(request, pk):

    resource = get_object_or_404(
        Resource,
        pk=pk,
        user=request.user
    )

    return render(
        request,
        "resources/resource_detail.html",
        {
            "resource": resource
        }
    )


@login_required
def resource_update(request, pk):

    resource = get_object_or_404(
        Resource,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = ResourceForm(
            request.POST,
            instance=resource
        )

        if form.is_valid():

            resource = form.save()

            Activity.objects.create(
                user=request.user,
                action="Resource Updated",
                description=f"Updated resource: {resource.title}"
            )

            messages.success(
                request,
                "Resource updated successfully!"
            )

            return redirect(
                "resource_detail",
                pk=resource.pk
            )

    else:

        form = ResourceForm(
            instance=resource
        )

    return render(
        request,
        "resources/resource_form.html",
        {
            "form": form,
            "page_title": "Edit Resource",
            "button_text": "Save Changes",
            "resource": resource,
        }
    )


@login_required
def resource_delete(request, pk):

    resource = get_object_or_404(
        Resource,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        title = resource.title

        resource.delete()

        Activity.objects.create(
            user=request.user,
            action="Resource Deleted",
            description=f"Deleted resource: {title}"
        )

        messages.success(
            request,
            "Resource deleted successfully!"
        )

        return redirect(
            "resources_list"
        )

    return render(
        request,
        "resources/resource_confirm_delete.html",
        {
            "resource": resource
        }
    )