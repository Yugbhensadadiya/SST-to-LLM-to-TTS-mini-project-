import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from recorder.recorder import record_audio
from stt.whisper_stt import transcribe_audio
from llm.groq_service import ask_groq
from tts.pyttsx3_tts import speak
from utils.language_router import get_language_name

EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "stop", "close"}


def main():
    print("\n" + "=" * 45)
    print("      University Voice Assistant (Continuous)      ")
    print("=" * 45)
    print("Tip: Say 'exit', 'quit', or 'bye' (or press Ctrl+C) to stop.\n")

    conversation_history = []

    try:
        while True:
            audio_path = record_audio()

            print("Transcribing audio...")
            text, language = transcribe_audio(audio_path)

            if not text or not text.strip():
                print("\n(No speech detected. Listening again...)\n")
                continue

            print("\nDetected Language:")
            print(get_language_name(language))

            print("\nUser:")
            print(text)

            # Check if user said an exit command
            cleaned_input = text.lower().strip().rstrip(".!?")
            if cleaned_input in EXIT_KEYWORDS:
                farewell = "Goodbye! Have a great day."
                print(f"\nAssistant:\n{farewell}")
                speak(farewell)
                break

            answer = ask_groq(
                text=text,
                language=language,
                history=conversation_history
            )

            print("\nAssistant:")
            print(answer)

            speak(answer)

            # Keep conversation history for context in follow-up queries
            conversation_history.append({"role": "user", "content": text})
            conversation_history.append({"role": "assistant", "content": answer})

            # Small pause before listening again so speaker echo isn't picked up
            time.sleep(0.5)
            print("\n" + "-" * 45)

    except KeyboardInterrupt:
        print("\n\nSession ended by user. Goodbye!")


if __name__ == "__main__":
    main()