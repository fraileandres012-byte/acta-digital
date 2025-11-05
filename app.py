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

# 3. Botón para generar
if st.button("Generar hash"):
    if texto.strip():
        # calcular hash
        h = get_hash(texto)

        # opcional: crear un registro con timestamp
        registro = {
            "texto": texto,
            "timestamp": time.time(),
            "hash": h
        }

        st.success("Hash generado:")
        st.code(h)

        st.subheader("Registro generado (JSON)")
        st.code(json.dumps(registro, indent=2))
    else:
        st.warning("Escribe algo antes de generar el hash.")
