from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")