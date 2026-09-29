LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "mr": "Marathi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "pa": "Punjabi",
    "ur": "Urdu",
}

def get_language_name(code):
    if not code:
        return "Unknown"
    return LANGUAGE_NAMES.get(code.lower(), code.upper())