from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def ask_groq(text, language):

    if language == "gu":
        lang_instruction = "Answer in Gujarati."

    elif language == "hi":
        lang_instruction = "Answer in Hindi."

    else:
        lang_instruction = "Answer in English."

    prompt = f"""
You are a helpful university AI assistant.

{lang_instruction}

User Question:
{text}

Give a concise and helpful answer.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=300
    )

    return response.choices[0].message.content