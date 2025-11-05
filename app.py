import streamlit as st
import hashlib

def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

st.title("Acta digital - prueba de hash")

texto = st.text_input("Escribe algo:")

if texto:
    hash_texto = get_hash(texto)
    st.write("Hash SHA-256:")
    st.code(hash_texto)
