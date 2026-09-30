import sys
import time
from recorder.recorder import record_audio
from stt.whisper_stt import transcribe_audio
from llm.groq_service import ask_groq
from tts.pyttsx3_tts import speak
from utils.language_router import get_language_name
from utils.memory import ConversationMemory
from config.settings import MAX_CONVERSATION_HISTORY

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "stop", "close"}


def main():
    print("\n" + "=" * 45)
    print("      University Voice Assistant (Continuous)      ")
    print("=" * 45)
    print("Tip: Say 'exit', 'quit', or 'bye' (or press Ctrl+C) to stop.\n")

    memory = ConversationMemory(max_turns=MAX_CONVERSATION_HISTORY)

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

            cleaned_input = text.lower().strip().rstrip(".!?")
            if cleaned_input in EXIT_KEYWORDS:
                farewell = "Goodbye! Have a great day."
                print(f"\nAssistant:\n{farewell}")
                speak(farewell)
                break

            answer = ask_groq(
                text=text,
                language=language,
                history=memory.get_messages(),
            )

            print("\nAssistant:")
            print(answer)

            speak(answer)

            memory.add_turn(text, answer)

            time.sleep(0.5)
            print("\n" + "-" * 45)

    except KeyboardInterrupt:
        print("\n\nSession ended by user. Goodbye!")


if __name__ == "__main__":
    main()