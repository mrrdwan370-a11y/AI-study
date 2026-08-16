from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .models import ChatSession, ChatMessage
from .forms import ChatForm
from .services import ask_ai


@login_required
def ai_chat(request):

    session_id = request.GET.get("session")

    if session_id:

        session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

    else:

        session = ChatSession.objects.create(
            user=request.user,
            title="New AI Chat"
        )

    if request.method == "POST":

        form = ChatForm(
            request.POST
        )

        if form.is_valid():

            user_message = form.cleaned_data["message"]

            ChatMessage.objects.create(
                session=session,
                role="user",
                content=user_message
            )

            previous_messages = (
                ChatMessage.objects
                .filter(session=session)
                .order_by("created_at")
            )

            messages = [

                {
                    "role": "system",
                    "content": (
                        "You are AI Study Hub Assistant. "
                        "Help students understand programming, "
                        "Django, Python, databases and study topics. "
                        "Give clear and educational answers."
                    )
                }

            ]

            for message in previous_messages:

                messages.append({
                    "role": message.role,
                    "content": message.content
                })

            try:

                ai_response = ask_ai(
                    messages
                )

            # except Exception:

            #     ai_response = (
            #         "Sorry, I couldn't connect to the AI service. "
            #         "Please try again later."
            #     )
            except Exception as e:
                 print("AI ERROR:", e)
                 ai_response = f"AI Error: {e}"

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=ai_response
            )

            if session.title == "New AI Chat":

                session.title = user_message[:50]

                session.save()

            return redirect(
                f"/ai/?session={session.id}"
            )

    else:

        form = ChatForm()

    sessions = ChatSession.objects.filter(
        user=request.user
    ).order_by("-updated_at")

    messages = ChatMessage.objects.filter(
        session=session
    )

    return render(
        request,
        "ai_assistant/chat.html",
        {
            "session": session,
            "sessions": sessions,
            "messages": messages,
            "form": form,
        }
    )