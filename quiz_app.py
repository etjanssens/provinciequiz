import streamlit as st
import pandas as pd
import random
import time

# Pagina setup
st.set_page_config(page_title="Raad de provincie", page_icon="🧠")

# 🌿 Huisstijl en achtergrond
st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #e6f7f1 0%, #ffffff 30%, #d4f5d2 100%);
        background-attachment: fixed;
    }
    .stApp {
        background: transparent;
    }

    /* Algemene tekstkleur */
    html, body, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #003a1b !important;
    }

    h1, .stTitle {
        color: #01A747 !important;
        font-weight: bold;
    }

    .stMarkdown strong {
        color: #003a1b !important;
    }

    .stButton>button {
        background-color: #01A747;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #028a3a;
    }

    .stSelectbox label {
        font-weight: bold;
        color: #01A747;
    }

    .stSidebar {
        background-color: #f7f7f7;
    }
    </style>
""", unsafe_allow_html=True)

# Logo
st.markdown(
    '<img src="https://groenlinkspvda.nl/wp-content/uploads/2023/09/GL-PvdA-logo-1.svg" width="220">',
    unsafe_allow_html=True
)

# Titel en subtitel
st.title("🧠 Raad de provincie bij de plaats!")
st.markdown("**Van Emiel Janssens, voor Faye Bovelander ❤️**")

# Data inladen
@st.cache_data
def load_data():
    df = pd.read_csv("woonplaatsen.csv")
    if "woonplaats" not in df.columns or "provincie" not in df.columns:
        st.error("CSV mist kolommen 'woonplaats' en/of 'provincie'.")
        st.stop()
    return df[["woonplaats", "provincie"]].dropna().drop_duplicates()

df = load_data()
alle_provincies = sorted(df["provincie"].unique())

# Session state initialiseren
if "vragenlijst" not in st.session_state:
    st.session_state.vragenlijst = random.sample(df.to_dict(orient="records"), 10)
    st.session_state.huidige_index = 0
    st.session_state.goed_geraden = 0
    st.session_state.feedback_toon = False

# EINDSCHERM
if st.session_state.huidige_index >= len(st.session_state.vragenlijst):
    score = st.session_state.goed_geraden
    totaal = len(st.session_state.vragenlijst)
    percentage = (score / totaal) * 100

    # Feedback per score
    feedback_zinnen = {
        0: "🪙 Muntje in de randstedelijke arrogantiepot!",
        1: "🧭 Je weet net genoeg om verdwaald te raken in je eigen provincie.",
        2: "🚫 Je hebt duidelijk een blinde vlek buiten je eigen postcode.",
        3: "🛵 Jij komt niet vaak buiten de ring, maar áls je er komt, geniet je des te meer.",
        4: "🌫️ Je hebt ooit wel eens van Groningen gehoord, maar daar blijft het bij.",
        5: "🚆 Misschien een NS-kortingskaart overwegen om eens wat van ons mooie land te ontdekken?",
        6: "🚶 Niet slecht! Jij komt weleens ergens. Letterlijk.",
        7: "🚗 Jij kent best veel in Nederland. Heb je een auto ofzo?",
        8: "🗺️ Jij bent het menselijk alternatief voor de ANWB-routeplanner.",
        9: "📡 Jij bent het type dat het weerbericht per provincie volgt.",
        10: "🧠 Jij hebt deze quiz gehackt. Of je bent gewoon heel slim!",
    }

    oordeel = feedback_zinnen.get(score, "")
    st.success(f"🎉 Je hebt {score} van de {totaal} goed ({percentage:.1f}%)! {oordeel}")

    deeltekst = f"Ik had {score} van de {totaal} goed in de GroenLinks-PvdA Provinciequiz! 🇳🇱🧠 #provinciequiz"

    st.markdown("### Deel jouw score:")
    st.code(deeltekst, language="markdown")
    st.markdown("📋 Selecteer en kopieer de tekst hierboven om te delen op WhatsApp, socials of mail.")

    if st.button("🔁 Probeer opnieuw"):
        for key in ["vragenlijst", "huidige_index", "goed_geraden", "feedback_toon"]:
            del st.session_state[key]
        st.rerun()

    st.stop()

# Vraag laden
vraag = st.session_state.vragenlijst[st.session_state.huidige_index]
plaats = vraag["woonplaats"]
juiste_provincie = vraag["provincie"]
vraagnummer = st.session_state.huidige_index + 1
totaal = len(st.session_state.vragenlijst)
antwoord_key = f"keuze_{vraagnummer}"

# Voortgang
st.markdown(f"🔄 **Vraag {vraagnummer} van {totaal}**")
st.markdown(f"📍 In welke provincie ligt de plaats _{plaats}_?")

# Keuzemenu
antwoord = st.selectbox(
    "Kies de provincie:",
    [""] + alle_provincies,
    index=0,
    key=antwoord_key
)

# Verwerking
if antwoord and not st.session_state.feedback_toon:
    st.session_state.feedback_toon = True
    if antwoord == juiste_provincie:
        st.success("✅ Goed geraden!")
        st.session_state.goed_geraden += 1
    else:
        st.error(f"❌ Fout! Het juiste antwoord is: **{juiste_provincie}**")

    # Animatie
    with st.empty():
        bar = st.progress(0)
        for i in range(80):  # ±1s
            time.sleep(0.012)
            bar.progress(i + 1)

    # Volgende vraag
    st.session_state.huidige_index += 1
    st.session_state.feedback_toon = False
    st.rerun()

# Resetknop in sidebar
with st.sidebar:
    if st.button("🔁 Opnieuw beginnen"):
        for key in ["vragenlijst", "huidige_index", "goed_geraden", "feedback_toon"]:
            del st.session_state[key]
        st.rerun()