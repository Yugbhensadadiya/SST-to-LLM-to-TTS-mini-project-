import re
import pyttsx3

try:
    import pythoncom
except ImportError:
    pythoncom = None


def clean_text_for_tts(text: str) -> str:
    cleaned = re.sub(r'[*#_`~>|]', '', text)
    cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()


def speak(text):
    if not text:
        return

    clean_text = clean_text_for_tts(text)
    if not clean_text:
        return

    print("\nAssistant Speaking...\n")
    try:
        if pythoncom:
            pythoncom.CoInitialize()

        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(clean_text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS Error: {e}")