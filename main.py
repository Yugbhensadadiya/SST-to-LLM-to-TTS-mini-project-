from recorder.recorder import record_audio
from stt.whisper_stt import transcribe_audio
from llm.groq_service import ask_groq
from tts.pyttsx3_tts import speak
from utils.language_router import get_language_name



def main():

    print("\n===== University Voice Assistant =====\n")

    audio_path = record_audio()

    text, language = transcribe_audio(audio_path)

    print("\nDetected Language:")
    print(get_language_name(language))

    print("\nUser:")
    print(text)

    answer = ask_groq(
        text=text,
        language=language
    )

    print("\nAssistant:")
    print(answer)

    speak(answer)


if __name__ == "__main__":
    main()