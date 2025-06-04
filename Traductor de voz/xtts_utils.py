
import torch
from TTS.api import TTS
import os

# Cargar modelo XTTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=torch.cuda.is_available())

def generate_xtts_audio(text, reference_audio_path, output_path="audios/output.wav"):
    tts.tts_to_file(
        text=text,
        speaker_wav=reference_audio_path,
        language="en",
        file_path=output_path
    )
    return output_path
