import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):

    result = model.transcribe(audio_path)

    text = result["text"].strip()
    language = result["language"]

    return text, language