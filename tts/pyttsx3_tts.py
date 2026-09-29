import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 150)

def speak(text):

    print("\nAssistant Speaking...\n")

    engine.say(text)

    engine.runAndWait()