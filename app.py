import streamlit as st
import hashlib
import time
import json
import os
import secrets

# ================== CONFIG ==================
DOC_FILE = "blockchain.jsonl"   # un registro por línea
VOTES_FILE = "votes.jsonl"      # votos guardados línea a línea

# ================== UTILIDADES BÁSICAS ==================
def get_hash(text: str) -> str:
    """Devuelve el hash SHA-256 del texto."""
    return hashlib.sha256(text.encode()).hexdigest()

def save_record(record: dict):
    """Guarda un registro de documento en el archivo."""
    with open(DOC_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_records():
    """Carga todos los registros de documentos."""
    if not os.path.exists(DOC_FILE):
        return []
    records = []
    with open(DOC_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records

# ================== VERIFICAR SI YA ESTÁ REGISTRADO ==================
def verify(content: str) -> bool:
    """
    Comprueba si el contenido ya fue registrado antes.
    Calcula su hash y lo busca en el archivo local.
    """
    h = get_hash(content)
    if not os.path.exists(DOC_FILE):
        return False
    with open(DOC_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("hash") == h:
                return True
    return False

# ================== VOTOS ==================
def save_vote(doc_hash: str, vote: str):
    """Guarda un voto (sí/no) para un hash de documento."""
    with open(VOTES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"hash": doc_hash, "vote": vote}, ensure_ascii=False) + "\n")

def count_votes():
    """Cuenta los votos sí/no."""
    yes, no = 0, 0
    if not os.path.exists(VOTES_FILE):
        return yes, no
    with open(VOTES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            v = json.loads(line)
            if v.get("vote") == "Sí":
                yes += 1
            else:
                no += 1
    return yes, no

# ================== INTERFAZ ==================
st.title("Registro de Documentos Digitales (demo)")

tabs = st.tabs([
    "📥 Registrar",
    "🔍 Verificar documento",
    "🔐 Claves",
    "🗳️ Votación de validez",
    "📜 Historial"
])

# ---------- TAB 1: REGISTRAR ----------
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
            content_hash = get_hash(content)
            record = {
                "owner": owner.strip(),
                "hash": content_hash,
                "content_preview": content[:80],
                "time": time.time()
            }
            save_record(record)
            st.success("Documento registrado con éxito ✅")
            st.write("Hash del documento:")
            st.code(content_hash)

# ---------- TAB 2: VERIFICAR DOCUMENTO ----------
with tabs[1]:
    st.subheader("1) Verificar si el contenido coincide con un hash dado")
    texto_verificar = st.text_area("Pega aquí el contenido que quieres verificar")
    hash_usuario = st.text_input("Hash que debería tener este contenido")

    if st.button("Verificar coincidencia texto-hash"):
        if not texto_verificar.strip() or not hash_usuario.strip():
            st.warning("Rellena tanto el contenido como el hash.")
        else:
            hash_calculado = get_hash(texto_verificar)
            if hash_calculado == hash_usuario.strip():
                st.success("✅ El contenido coincide con el hash proporcionado.")
            else:
                st.error("❌ El contenido NO coincide con el hash proporcionado.")
                st.write("Hash calculado para el contenido que enviaste:")
                st.code(hash_calculado)

    st.subheader("2) Verificar si este documento ya estaba registrado")
    texto_buscar = st.text_area("Pega el contenido del documento a comprobar", key="texto_buscar")

    if st.button("Verificar si ya existe"):
        if not texto_buscar.strip():
            st.warning("Escribe el contenido primero.")
        else:
            exists = verify(texto_buscar)
            if exists:
                st.success("✅ Este documento (su hash) YA está registrado.")
            else:
                st.info("ℹ️ Este documento NO aparece en el registro local.")

# ---------- TAB 3: CLAVES ----------
with tabs[2]:
    st.subheader("Generación de claves (demo)")
    st.write("Aquí simulamos un par de claves: la privada **no** debes compartirla; la pública sí.")

    if st.button("Generar nuevas claves"):
        private_key = secrets.token_hex(16)  # 128 bits en hex
        public_key = get_hash(private_key)
        st.write("Tu **clave pública** (para identificarte):")
        st.code(public_key)
        st.write("Tu **clave privada** (guárdala, sirve para firmar):")
        st.code(private_key)
        st.info("La clave pública identifica, la privada da poder para firmar.")

    st.markdown(
        "> Nota: esto es una demo simplificada, no un sistema de claves real como los de producción."
    )

# ---------- TAB 4: VOTACIÓN ----------
with tabs[3]:
    st.header("Votación de validez")
    st.write("Simula una DAO donde cada usuario puede emitir su voto sobre un documento.")

    doc_hash = st.text_input("Hash del documento a votar")
    vote = st.radio("¿Es válido?", ["Sí", "No"])

    if st.button("Votar"):
        if not doc_hash.strip():
            st.warning("Debes indicar el hash del documento.")
        else:
            save_vote(doc_hash.strip(), vote)
            st.success("Voto registrado 🗳️")

    if st.button("Ver resultado"):
        y, n = count_votes()
        st.write(f"Sí: {y} | No: {n}")
        st.markdown(
            "> Comentario: el código ejecuta la decisión (registra el voto y muestra el conteo), "
            "pero **no analiza si la decisión es justa** ni quién debería tener más peso."
        )

# ---------- TAB 5: HISTORIAL ----------
with tabs[4]:
    st.subheader("Historial de documentos registrados")
    records = load_records()
    if not records:
        st.info("Aún no hay documentos registrados.")
    else:
        records = sorted(records, key=lambda r: r.get("time", 0), reverse=True)
        for i, r in enumerate(records, start=1):
            st.markdown(f"### Registro {i}")
            st.write(f"**Propietario:** {r.get('owner', '—')}")
            st.write("**Hash:**")
            st.code(r.get("hash", ""))
            ts = r.get("time", 0)
            if ts:
                fecha = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                st.write(f"**Fecha de registro:** {fecha}")
            if r.get("content_preview"):
                st.write(f"**Contenido (preview):** {r['content_preview']}...")
            st.write("---")
