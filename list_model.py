from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

models = client.models.list()

print("Available Models:\n")

for model in models.data:
    print(model.id)