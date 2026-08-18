import time
from django.conf import settings
from google import genai
from google.genai import types

client = genai.Client( api_key=settings.GEMINI_API_KEY)

def ask_ai(messages,max_retries=3):
    system_instruction = (
        "You are AI Study Hub Assistant. "
        "Help students understand programming, Django, Python, "
        "databases, artificial intelligence and study topics. "
        "Give clear, educational and easy-to-understand answers. "
        "When explaining code, provide examples."
    )
    conversation = []
    for message in messages:
        role = message.get("role")
        if role == "system":
            continue
        if role == "assistant":
            role = "model"
        conversation.append( types.Content( role=role, parts=[ types.Part(  text=message.get("content", "") ) ] ) )

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content( model="gemini-3.5-flash",contents=conversation,
                config=types.GenerateContentConfig( system_instruction=system_instruction,  max_output_tokens=1000, temperature=0.7, ) )
            return response.text
        except Exception as e:
            error_message = str(e)
            print("================================")
            print("GEMINI AI ERROR:")
            print(error_message)
            print("================================")
            if "503" in error_message:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                    continue
            raise