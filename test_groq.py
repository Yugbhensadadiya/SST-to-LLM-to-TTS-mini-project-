from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "give me you introduction in one sentance"
        }
    ],
    temperature=0.3,
)

print(response.choices[0].message.content)