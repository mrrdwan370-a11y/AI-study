from django.shortcuts import render
from ai_assistant.services import ask_ai
from django.contrib import messages
from django.urls import reverse
from tasks.models import Task
from resources.models import Resource
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from notes.models import Note
from django.db.models import Q
from django.shortcuts import  get_object_or_404, redirect, render

from .forms import NoteForm, CategoryForm, TagForm
from .models import Note, Category, Tag
from dashboard.models import Activity


@login_required
def notes_list(request):
    notes = Note.objects.filter( user=request.user ).select_related( "category").prefetch_related("tags")
    search = request.GET.get( "search",  "" )
    category_id = request.GET.get( "category",  ""  )
    favorite = request.GET.get( "favorite", "" )
    if search:
        notes = notes.filter( Q(title__icontains=search) |  Q(content__icontains=search) |  Q(tags__name__icontains=search) ).distinct()
    if category_id:
        notes = notes.filter( category_id=category_id )
    if favorite == "1":
        notes = notes.filter( is_favorite=True  )
    paginator = Paginator( notes,  6 )
    page_number = request.GET.get( "page" )
    page_obj = paginator.get_page( page_number )
    categories = Category.objects.filter( user=request.user )
    context = {
        "page_obj": page_obj,
        "categories": categories,
        "search": search,
        "selected_category": category_id,
        "favorite": favorite,
    }
    return render( request, "notes/notes_list.html",context )

@login_required
def note_detail(request, pk):
    note = get_object_or_404( Note, pk=pk, user=request.user)
    return render(
        request, "notes/note_detail.html", { "note": note } )

@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(  request.POST,  request.FILES, user=request.user )
        if form.is_valid():
            note = form.save(  commit=False )
            note.user = request.user
            note.save()
            form.save_m2m()
            Activity.objects.create(  user=request.user,  action="Note Created", description=f"Created note: {note.title}" )
            messages.success( request, "Note created successfully!")
            return redirect( "notes_list"  )
    else:
        form = NoteForm( user=request.user )
    return render(
        request,
        "notes/note_form.html",
        { "form": form, "page_title": "Create Note", "button_text": "Create Note", }  )

@login_required
def note_update(request, pk):
    note = get_object_or_404( Note, pk=pk, user=request.user )
    if request.method == "POST":
        form = NoteForm( request.POST, request.FILES, instance=note, user=request.user )
        if form.is_valid():
            note = form.save()
            Activity.objects.create(  user=request.user,  action="Note Updated", description=f"Updated note: {note.title}"  )
            messages.success( request, "Note updated successfully!" )
            return redirect( "note_detail", pk=note.pk )
    else:
        form = NoteForm( instance=note, user=request.user  )
    return render(  request, "notes/note_form.html",
        {
            "form": form,
            "page_title": "Edit Note",
            "button_text": "Save Changes",
            "note": note,
        }
    )

@login_required
def note_delete(request, pk):
    note = get_object_or_404( Note, pk=pk,  user=request.user )
    if request.method == "POST":
        title = note.title
        note.delete()
        Activity.objects.create( user=request.user,  action="Note Deleted", description=f"Deleted note: {title}" )
        messages.success( request, "Note deleted successfully!" )
        return redirect( "notes_list" )
    return render(  request,  "notes/note_confirm_delete.html", { "note": note } )

@login_required
def note_toggle_favorite(request, pk):
    note = get_object_or_404(  Note, pk=pk, user=request.user )
    if request.method == "POST":
        note.is_favorite = not note.is_favorite
        note.save()
    return redirect( "notes_list" )

@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm( request.POST )
        if form.is_valid():
            category = form.save( commit=False  )
            category.user = request.user
            category.save()
            messages.success(  request, "Category created successfully!" )
            return redirect( "notes_list"  )
    else:
        form = CategoryForm()
    return render(  request, "notes/category_form.html", { "form": form } )

@login_required
def tag_create(request):
    if request.method == "POST":
        form = TagForm(  request.POST  )
        if form.is_valid():
            tag = form.save(  commit=False  )
            tag.user = request.user
            tag.save()
            messages.success(  request, "Tag created successfully!" )
            return redirect("notes_list"  )

    else:
        form = TagForm()
    return render(  request,  "notes/tag_form.html",  { "form": form }  )

@login_required
def global_live_search(request):
    query = request.GET.get("q", "").strip()
    results = []
    if not query:  return JsonResponse({  "results": [] })
    notes = Note.objects.filter( user=request.user ).filter(  Q(title__icontains=query) |
          Q(content__icontains=query) | Q(tags__name__icontains=query) ).distinct()[:10]
    for note in notes:
        results.append({ "type": "Note", "title": note.title, "content": note.content[:120],
             "category": (
                note.category.name
                if note.category
                else ""
            ), "url": f"/notes/{note.pk}/", })

    tasks = Task.objects.filter(  user=request.user  ).filter(  Q(title__icontains=query) | Q(description__icontains=query) )[:10]
    for task in tasks:
        results.append({ "id": task.id, "title": task.title,  "content": task.description[:120], 
            "category": task.get_priority_display(), "type": "Task",
            "url": reverse("task_detail", args=[task.id] ),  })
    resources = Resource.objects.filter( user=request.user  ).filter( Q(title__icontains=query) |  Q(description__icontains=query) |  Q(resource_type__icontains=query) )[:10]
    for resource in resources:
        results.append({ "type": "Resource", "title": resource.title, "content": resource.description[:120],
            "category": resource.get_resource_type_display(),
            "url": f"/resources/{resource.pk}/",  })
    return JsonResponse({ "results": results[:20] })

@login_required
def summarize_note(request, pk):
    note = get_object_or_404( Note, pk=pk, user=request.user )
    if request.method != "POST": return redirect("note_detail", pk=pk)
    prompt = f"""
You are an AI Study Assistant.

Summarize the following study note clearly.

Requirements:
- Keep the important information.
- Use simple language.
- Organize the answer with bullet points.
- Do not add information that is not in the note.

Note title:
{note.title}

Note content:
{note.content}
"""
    try:
        ai_response = ask_ai([
            {
                "role": "system",
                "content": (
                    "You are a helpful educational "
                    "assistant for students."  )  },
            { "role": "user",   "content": prompt  } ])
        request.session["ai_summary"] = ai_response
        request.session.modified = True
        messages.success(  request, "Note summarized successfully!"  )
    except Exception as e:
        print("AI ERROR:", e)
        messages.error( request, f"AI Error: {e}"  )
    return redirect( "note_detail",  pk=pk )