from collections import deque
import os
import time
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd


def record_audio(
    filename="audio/input.wav",
    sample_rate=16000,
    block_duration=0.05,
    silence_duration=1.3,
    max_duration=18.0,
    initial_timeout=4.5,
):
    block_size = int(sample_rate * block_duration)
    pre_speech_blocks = deque(maxlen=int(0.4 / block_duration))
    recorded_blocks = []

    print("\nListening... Speak your query.")

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype="int16", blocksize=block_size) as stream:
        calibration_blocks = max(1, int(0.25 / block_duration))
        noise_levels = []
        for _ in range(calibration_blocks):
            data, _ = stream.read(block_size)
            rms = float(np.sqrt(np.mean(data.astype(np.float32) ** 2)))
            noise_levels.append(rms)
            pre_speech_blocks.append(data.copy())

        avg_noise = float(np.mean(noise_levels)) if noise_levels else 150.0

        start_threshold = max(avg_noise * 1.5, avg_noise + 200.0, 350.0)
        stop_threshold = max(avg_noise * 1.2, avg_noise + 100.0, 250.0)

        has_spoken = False
        silence_start = None
        start_time = time.time()

        while True:
            data, _ = stream.read(block_size)
            rms = float(np.sqrt(np.mean(data.astype(np.float32) ** 2)))
            elapsed = time.time() - start_time

            if not has_spoken:
                pre_speech_blocks.append(data.copy())
                if rms > start_threshold:
                    has_spoken = True
                    print("  [Speaking detected...]")
                    recorded_blocks.extend(pre_speech_blocks)
                elif elapsed > initial_timeout:
                    recorded_blocks.extend(pre_speech_blocks)
                    break
            else:
                recorded_blocks.append(data.copy())

                if rms < stop_threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start >= silence_duration:
                        print("  [Finished speaking, processing...]")
                        break
                else:
                    silence_start = None

            if elapsed > max_duration:
                print("  [Maximum duration reached, processing...]")
                break

    if recorded_blocks:
        audio_data = np.concatenate(recorded_blocks, axis=0)
    else:
        audio_data = np.zeros((sample_rate, 1), dtype="int16")

    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    write(filename, sample_rate, audio_data)
    return filename