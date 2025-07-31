import streamlit as st
import pdfplumber
import random

def genereer_vragen(tekst, aantal=3):
    voorbeeld_vragen = [
        ("Wat betekent het begrip 'toegevoegde waarde'?", ["De winst", "De extra waarde in een proces", "BTW", "De kostprijs"], 1),
        ("Welke sector hoort bij logistiek?", ["Ziekenhuizen", "Bouw", "Transport", "Reclame"], 2),
        ("Wat is het doel van marketing?", ["Productie verhogen", "Meer winst boeken", "Werknemers belonen", "De verkoop stimuleren"], 3)
    ]
    return random.sample(voorbeeld_vragen, min(aantal, len(voorbeeld_vragen)))

def extract_text_from_pdf(uploaded_file):
    all_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"
    return all_text

st.set_page_config(page_title="Economie Coach voor Téné", layout="wide")
st.title("📘 AI Studiecoach Economie – Derde Middelbaar")

# ⬅️ 1. Upload PDF en sla tekst op in session_state
st.sidebar.header("📂 Upload werkboek")
uploaded_file = st.sidebar.file_uploader("Upload een PDF van een thema", type="pdf")

if uploaded_file and "pdf_text" not in st.session_state:
    with st.spinner("PDF wordt ingelezen..."):
        st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)

if "pdf_text" in st.session_state:
    thema_lijst = ["Thema 1: Consument & Producent", "Thema 2: Werking van een onderneming",
                   "Thema 3: Boekhoudkundig beheer", "Thema 4: Personeelsbeheer", "Thema 5: Logistiek & Transport"]

    st.sidebar.markdown("### 📚 Kies een thema")
    gekozen_thema = st.sidebar.selectbox("Kies een thema om oefeningen te maken:", thema_lijst)

    # ⬅️ 2. Vragen pas genereren bij klik
    if st.button("🎲 Genereer oefenvragen"):
        st.session_state.vragen = genereer_vragen(st.session_state.pdf_text)
        st.session_state.antwoorden = [None] * len(st.session_state.vragen)
        st.session_state.gecontroleerd = [False] * len(st.session_state.vragen)

if "vragen" in st.session_state:
    st.header("📝 Oefenvragen")

    score = 0
    for idx, (vraag, opties, juist_idx) in enumerate(st.session_state.vragen):
        st.subheader(f"Vraag {idx+1}")
        st.session_state.antwoorden[idx] = st.radio(
            vraag,
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
    st.info("👉 Kies een thema en klik op 'Genereer oefenvragen'.")
