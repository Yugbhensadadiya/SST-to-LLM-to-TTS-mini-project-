import collections
import os
import time
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd


def record_audio(
    filename="audio/input.wav",
    sample_rate=16000,
    block_duration=0.05,  # 50ms block size
    silence_duration=1.3,  # wait ~1.3 seconds of silence after user finishes speaking
    max_duration=18.0,  # maximum overall recording limit
    initial_timeout=4.5,  # timeout if user doesn't start speaking
):
    block_size = int(sample_rate * block_duration)
    # Pre-speech buffer (0.4s) to capture the start of words
    pre_speech_blocks = collections.deque(maxlen=int(0.4 / block_duration))
    recorded_blocks = []

    print("\nListening... Speak your query.")

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype="int16", blocksize=block_size) as stream:
        # Measure ambient noise level dynamically (0.25 sec)
        calibration_blocks = max(1, int(0.25 / block_duration))
        noise_levels = []
        for _ in range(calibration_blocks):
            data, _ = stream.read(block_size)
            rms = float(np.sqrt(np.mean(data.astype(np.float32) ** 2)))
            noise_levels.append(rms)
            pre_speech_blocks.append(data.copy())

        avg_noise = float(np.mean(noise_levels)) if noise_levels else 150.0

        # Hysteresis thresholds:
        # Speech start: needs clear audio above noise floor
        start_threshold = max(avg_noise * 1.5, avg_noise + 200.0, 350.0)
        # Silence/stop: allows quieter speech without prematurely cutting off
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
                # Speech detection
                if rms > start_threshold:
                    has_spoken = True
                    print("  [Speaking detected...]")
                    recorded_blocks.extend(pre_speech_blocks)
                    silence_start = None
                elif elapsed > initial_timeout:
                    # User did not speak within initial timeout
                    recorded_blocks.extend(pre_speech_blocks)
                    break
            else:
                recorded_blocks.append(data.copy())

                if rms < stop_threshold:
                    # Silence detected after speech
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start >= silence_duration:
                        # User stopped speaking and silence persisted
                        print("  [Finished speaking, processing...]")
                        break
                else:
                    # User continued or resumed speaking within the pause window
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