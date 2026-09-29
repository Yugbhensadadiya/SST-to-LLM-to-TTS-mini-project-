import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(
    filename="audio/input.wav",
    duration=5,
    sample_rate=16000
):
    print("Speak now...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(filename, sample_rate, recording)

    print("Recording saved:", filename)

    return filename