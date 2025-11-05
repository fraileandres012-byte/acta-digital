import streamlit as st
import hashlib

# ---- funciones ----
def get_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# ---- interfaz ----
st.title("Acta digital - hashes")

st.header("1. Generar hash")
texto_generar = st.text_input("Escribe el texto para generar su hash:")

if st.button("Generar hash"):
    if texto_generar.strip():
        h = get_hash(texto_generar)
        st.success("Hash generado (SHA-256):")
        st.code(h)
    else:
        st.warning("Escribe un texto primero.")

st.header("2. Verificar hash")
texto_verificar = st.text_input("Texto original a verificar:", key="verificar_texto")
hash_usuario = st.text_input("Hash que debería tener el texto:", key="verificar_hash")

if st.button("Verificar"):
    if texto_verificar.strip() and hash_usuario.strip():
        hash_calculado = get_hash(texto_verificar)
        if hash_calculado == hash_usuario.strip():
            st.success("✅ Coincide: el hash pertenece a este texto.")
        else:
            st.error("❌ No coincide: el hash NO pertenece a este texto.")
            st.write("Hash calculado por la app:")
            st.code(hash_calculado)
    else:
        st.warning("Rellena el texto y el hash a verificar.")
