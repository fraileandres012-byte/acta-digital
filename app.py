import streamlit as st
import hashlib

def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

st.title("Generador de hash")

texto = st.text_input("Escribe el texto original:")

if st.button("Calcular hash"):
    if texto.strip():
        hash_result = get_hash(texto)
        st.success("Hash generado:")
        st.code(hash_result)
    else:
        st.warning("Escribe algo primero.")
