
import streamlit as st
from whisper_utils import transcribe_audio
from xtts_utils import generate_xtts_audio
import openai
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Voice Translator", page_icon="🗣️")
st.title("🗣️ Traductor de Voz con Clonación Personalizada")

st.info("Graba tu voz en español y traduce al inglés manteniendo tu identidad vocal.")

uploaded_file = st.file_uploader("📥 Sube tu voz en español (formato WAV)", type=["wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    st.audio(audio_path, format="audio/wav")

    if st.button("✅ Procesar"):
        with st.spinner("Transcribiendo con Whisper..."):
            texto_es = transcribe_audio(audio_path)
            st.success("Transcripción en español:")
            st.write(texto_es)

        with st.spinner("Traduciendo con GPT..."):
            prompt = f"Traduce al inglés esta frase manteniendo el sentido: {texto_es}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            texto_en = response.choices[0].message.content.strip()
            st.success("Traducción al inglés:")
            st.write(texto_en)

        with st.spinner("Generando voz clonada en inglés..."):
            audio_output_path = generate_xtts_audio(texto_en, audio_path)
            st.success("✅ Audio generado con tu voz en inglés")
            st.audio(audio_output_path, format="audio/wav")
