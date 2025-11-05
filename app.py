import streamlit as st
import hashlib
import time
import json

st.title("Acta digital")

contenido = st.text_area("Escribe el acta:")

if st.button("Guardar acta"):
    ts = time.time()
    acta = {
        "contenido": contenido,
        "timestamp": ts
    }
    acta_json = json.dumps(acta, sort_keys=True)
    acta_hash = hashlib.sha256(acta_json.encode()).hexdigest()

    st.success("Acta guardada")
    st.write("Hash del acta:", acta_hash)
