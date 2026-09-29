def get_language_name(code):

    mapping = {
        "en": "English",
        "hi": "Hindi",
        "gu": "Gujarati"
    }

    return mapping.get(code, "Unknown")