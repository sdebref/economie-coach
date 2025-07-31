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
            all_text += page.extract_text() + "\n"
    return all_text

st.set_page_config(page_title="Economie Coach voor Téné", layout="wide")
st.title("📘 AI Studiecoach Economie – Derde Middelbaar")

st.sidebar.header("📂 Upload werkboek")
uploaded_file = st.sidebar.file_uploader("Upload hier een PDF van een thema", type="pdf")

if uploaded_file:
    with st.spinner("PDF wordt ingelezen..."):
        volledige_tekst = extract_text_from_pdf(uploaded_file)

    thema_lijst = ["Thema 1: Consument & Producent", "Thema 2: Werking van een onderneming",
                   "Thema 3: Boekhoudkundig beheer", "Thema 4: Personeelsbeheer", "Thema 5: Logistiek & Transport"]

    st.sidebar.markdown("### 📚 Kies een thema")
    gekozen_thema = st.sidebar.selectbox("Kies een thema om oefeningen te maken:", thema_lijst)

    st.header(f"📝 Oefeningen bij {gekozen_thema}")
    vragen = genereer_vragen(volledige_tekst)

    score = 0
    for idx, (vraag, opties, juist_idx) in enumerate(vragen):
        st.subheader(f"Vraag {idx+1}")
        keuze = st.radio(vraag, opties, key=f"vraag_{idx}")
        if st.button(f"Controleer vraag {idx+1}", key=f"knop_{idx}"):
            if opties.index(keuze) == juist_idx:
                st.success("✅ Juist!")
                score += 1
            else:
                st.error(f"❌ Fout. Correct antwoord: {opties[juist_idx]}")

    st.markdown("---")
    st.markdown(f"### 🎯 Eindscore: {score} op {len(vragen)}")
else:
    st.info("👉 Upload een werkboek-PDF in de zijbalk om te beginnen.")