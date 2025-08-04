import streamlit as st
import openai
import pdfplumber
from pathlib import Path

@st.cache_data
def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"
    return all_text

def genereer_gpt_vragen(tekst, aantal=3):
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
Je bent een onderwijshulp voor een 14-jarige leerling met dyslexie. Op basis van onderstaande economische tekst uit het derde middelbaar, genereer je {aantal} meerkeuzevragen met telkens 4 antwoordopties. Geef telkens ook het juiste antwoord aan. De stijl moet duidelijk, kort en Nederlandstalig zijn.

TEKST:
"""
{tekst[:3000]}
"""

Formatteer je output als een JSON-lijst met:
- "vraag"
- "opties" (lijst van 4 antwoordmogelijkheden)
- "correcte_index" (getal van 0–3)
"""

try:
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
    )
    raw_output = response.choices[0].message.content
    return eval(raw_output)
except Exception as e:
    st.error(f"Fout bij ophalen van GPT-vragen: {e}")
    return []

st.set_page_config(page_title="Economie Coach voor Téné", layout="wide")
st.title("📘 AI Studiecoach Economie – Derde Middelbaar")

# Themabestand mapping
pdf_map = {
    "Thema 1: Consument & Producent": "data/Lift 3 DA T1.pdf",
    "Thema 2: Werking van een onderneming": "data/Lift 3 DA T2.pdf",
    "Thema 3: Boekhoudkundig beheer": "data/Lift 3 DA T3.pdf",
    "Thema 4: Personeelsbeheer": "data/Lift 3 DA T4.pdf",
    "Thema 5: Logistiek & Transport": "data/Lift 3 DA T5.pdf"
}

st.sidebar.header("📚 Kies een thema")
gekozen_thema = st.sidebar.selectbox("Kies een thema:", list(pdf_map.keys()))

pdf_path = Path(pdf_map[gekozen_thema])
volledige_tekst = extract_text_from_pdf(pdf_path)

if st.button("🎲 Genereer GPT-oefenvragen"):
    st.session_state.vragen = genereer_gpt_vragen(volledige_tekst)
    st.session_state.antwoorden = [None] * len(st.session_state.vragen)
    st.session_state.gecontroleerd = [False] * len(st.session_state.vragen)

if "vragen" in st.session_state:
    st.header("📝 Oefenvragen")
    score = 0
    for idx, vraag in enumerate(st.session_state.vragen):
        st.subheader(f"Vraag {idx+1}")
        opties = vraag["opties"]
        juist_idx = vraag["correcte_index"]
        st.session_state.antwoorden[idx] = st.radio(
            vraag["vraag"],
            opties,
            index=None,
            key=f"vraag_{idx}"
        )
        if st.button(f"Controleer vraag {idx+1}", key=f"knop_{idx}"):
            st.session_state.gecontroleerd[idx] = True
        if st.session_state.gecontroleerd[idx]:
            keuze = st.session_state.antwoorden[idx]
            if keuze is None:
                st.warning("⚠️ Kies een antwoord.")
            elif opties.index(keuze) == juist_idx:
                st.success("✅ Juist!")
                score += 1
            else:
                st.error(f"❌ Fout. Correct antwoord: {opties[juist_idx]}")
    st.markdown("---")
    st.markdown(f"### 🎯 Eindscore: {score} op {len(st.session_state.vragen)}")
else:
    st.info("👉 Kies een thema en klik op 'Genereer GPT-oefenvragen'.")
