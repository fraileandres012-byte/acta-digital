import streamlit as st
import hashlib
import time
import json
import os

# ----- configuración -----
DATA_FILE = "blockchain.jsonl"  # un registro por línea

# ----- funciones auxiliares -----
def get_hash(text: str) -> str:
    """Devuelve el hash SHA-256 del texto."""
    return hashlib.sha256(text.encode()).hexdigest()

def save_record(record: dict):
    """Guarda un registro en el archivo como una línea JSON."""
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_records():
    """Carga todos los registros del archivo. Devuelve una lista de dicts."""
    if not os.path.exists(DATA_FILE):
        return []
    records = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    # si alguna línea está corrupta, la saltamos
                    pass
    return records

# ----- interfaz -----
st.title("Registro de Documentos Digitales")

tabs = st.tabs(["📥 Registrar", "🔍 Verificar", "📜 Historial"])

# ================== TAB 1: REGISTRAR ==================
with tabs[0]:
    st.subheader("Registrar nuevo documento")

    owner = st.text_input("Propietario / Autor")
    content = st.text_area("Contenido del documento")

    if st.button("Registrar documento"):
        if not owner.strip():
            st.error("Debes indicar el propietario.")
        elif not content.strip():
            st.error("El contenido no puede estar vacío.")
        else:
            # calculamos el hash del contenido
            content_hash = get_hash(content)

            record = {
                "owner": owner.strip(),
                "hash": content_hash,
                "content_preview": content[:80],  # opcional: una vista previa
                "time": time.time()
            }

            save_record(record)
            st.success("Documento registrado con éxito ✅")
            st.write("Hash del documento:")
            st.code(content_hash)

# ================== TAB 2: VERIFICAR ==================
with tabs[1]:
    st.subheader("Verificar documento")

    texto_verificar = st.text_area("Pega aquí el contenido que quieres verificar")
    hash_usuario = st.text_input("Pega aquí el hash que debería tener el documento")

    if st.button("Verificar documento"):
        if not texto_verificar.strip() or not hash_usuario.strip():
            st.warning("Rellena tanto el contenido como el hash.")
        else:
            hash_calculado = get_hash(texto_verificar)
            if hash_calculado == hash_usuario.strip():
                st.success("✅ El contenido coincide con el hash proporcionado.")
            else:
                st.error("❌ El contenido NO coincide con el hash proporcionado.")
                st.write("Este sería el hash correcto para el contenido que has pegado:")
                st.code(hash_calculado)

# ================== TAB 3: HISTORIAL ==================
with tabs[2]:
    st.subheader("Historial de documentos registrados")
    records = load_records()

    if not records:
        st.info("Aún no hay documentos registrados.")
    else:
        # los mostramos del más reciente al más antiguo
        records = sorted(records, key=lambda r: r.get("time", 0), reverse=True)
        for i, r in enumerate(records, start=1):
            st.markdown(f"### Registro {i}")
            st.write(f"**Propietario:** {r.get('owner', '—')}")
            st.write(f"**Hash:**")
            st.code(r.get("hash", ""))
            # mostramos el timestamp de forma legible
            ts = r.get("time", 0)
            if ts:
                fecha = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                st.write(f"**Fecha de registro:** {fecha}")
            # vista previa opcional
            if r.get("content_preview"):
                st.write(f"**Contenido (preview):** {r['content_preview']}...")
            st.write("---")
