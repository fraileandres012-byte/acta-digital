import streamlit as st
import hashlib
import time
import json

# 1. Función para calcular el hash
def get_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

st.title("Acta digital - generador de hash")

# 2. Campo de texto
texto = st.text_area("Escribe el contenido del acta o el texto a firmar:")


