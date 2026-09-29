import re
import pyttsx3

try:
    import pythoncom
except ImportError:
    pythoncom = None


def clean_text_for_tts(text: str) -> str:
    # Remove markdown formatting like **, ##, bullet points, pipes
    cleaned = re.sub(r'[*#_`~>|]', '', text)
    cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def speak(text):
    if not text or not text.strip():
        return

    clean_text = clean_text_for_tts(text)
    if not clean_text:
        return

    print("\nAssistant Speaking...\n")
    try:
        if pythoncom:
            pythoncom.CoInitialize()

        # Initialize fresh engine instance per call to prevent SAPI5 event loop death in loops
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(clean_text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print(f"TTS Error: {e}")