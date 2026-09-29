import os
import shutil
import sys
import ctranslate2
from faster_whisper import WhisperModel

# Ensure ffmpeg binary is accessible in PATH
if not shutil.which("ffmpeg"):
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = os.path.dirname(ffmpeg_exe)
        target_exe = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        if not os.path.exists(target_exe):
            shutil.copyfile(ffmpeg_exe, target_exe)
        os.environ["PATH"] = ffmpeg_dir + os.path.pathsep + os.environ.get("PATH", "")
    except Exception:
        pass

# Ensure model is stored in virtual environment directory instead of global cache
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_DIR = sys.prefix if hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix else os.path.join(PROJECT_ROOT, ".venv")
MODEL_DIR = os.path.join(VENV_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

model = WhisperModel("small", device=device, compute_type=compute_type, download_root=MODEL_DIR)

def transcribe_audio(audio_path):
    segments, info = model.transcribe(audio_path, task="transcribe")
    text = "".join(segment.text for segment in segments).strip()
    language = info.language

    return text, language
