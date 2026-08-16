# from django.conf import settings
# from openai import OpenAI

# client = OpenAI(
#     api_key=settings.OPENAI_API_KEY
# )


# def ask_ai(messages):

#     response = client.chat.completions.create(

#         model="gpt-4o-mini",

#         messages=messages,

#         temperature=0.7,

#     )

#     return response.choices[0].message.content
from django.conf import settings
from google import genai
from google.genai import types


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def ask_ai(messages):

    system_instruction = (
        "You are AI Study Hub Assistant. "
        "Help students understand programming, Django, Python, "
        "databases, artificial intelligence and study topics. "
        "Give clear, educational and easy-to-understand answers. "
        "When explaining code, provide examples."
    )

    conversation = []

    for message in messages:

        if message["role"] == "system":
            continue

        role = message["role"]

        if role == "assistant":
            role = "model"

        conversation.append({
            "role": role,
            "parts": [
                {
                    "text": message["content"]
                }
            ]
        })

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=1000,
        )
    )

    return response.text