import streamlit as st
import whisper
import tempfile
import os
from pydub import AudioSegment
import torch
from TTS.api import TTS

st.title("🗣️ Traductor y Clonador de Voz (Español → Inglés)")
st.info("Sube un audio en español (.wav, .mp3, .ogg). El sistema lo transcribirá, traducirá y usará tu voz clonada para reproducirlo en inglés.")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

@st.cache_resource
def load_tts_model():
    return TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=torch.cuda.is_available())

model = load_model()
tts = load_tts_model()

# Guardar archivo temporal y convertir a .wav si es necesario
def save_and_convert_audio(uploaded_file):
    original_ext = os.path.splitext(uploaded_file.name)[-1].lower()
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=original_ext)
    temp_input.write(uploaded_file.read())
    temp_input.close()

    if original_ext != ".wav":
        audio = AudioSegment.from_file(temp_input.name)
        wav_path = temp_input.name.replace(original_ext, ".wav")
        audio.export(wav_path, format="wav")
    else:
        wav_path = temp_input.name

    return wav_path

# Subida
uploaded_file = st.file_uploader("🎤 Sube un archivo de audio", type=["wav", "mp3", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file)
    wav_path = save_and_convert_audio(uploaded_file)

    with st.spinner("Transcribiendo y traduciendo..."):
        result = model.transcribe(wav_path, task="translate")
        translated_text = result["text"]
        st.success("✅ Traducción lista")
        st.text_area("📝 Texto traducido al inglés", translated_text, height=200)

    st.subheader("🧬 Reproducción con tu propia voz (clonada)")
    speaker_wav = wav_path
    output_path = wav_path.replace(".wav", "_output.wav")

    tts.tts_to_file(text=translated_text, speaker_wav=speaker_wav, language="en", file_path=output_path)
    st.audio(output_path, format="audio/wav")

    os.remove(wav_path)