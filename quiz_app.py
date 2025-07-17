import streamlit as st
import pandas as pd
import random
import time

# Pagina setup
st.set_page_config(page_title="Raad de provincie", page_icon="🧠")

# 🌿 Huisstijl (inclusief GL-PvdA kleuren en achtergrond)
st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #e6f7f1 0%, #ffffff 30%, #d4f5d2 100%);
        background-attachment: fixed;
    }
    .stApp {
        background: transparent;
    }
    h1, .stTitle {
        color: #01A747;
        font-weight: bold;
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

# Titel
st.title("🐼 Raad de provincie bij de plaats!")
st.markdown("**Van Emiel Janssens, voor het campagneteam ❤️**")

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

# Init session state
if "vragenlijst" not in st.session_state:
    st.session_state.vragenlijst = random.sample(df.to_dict(orient="records"), 15)
    st.session_state.huidige_index = 0
    st.session_state.goed_geraden = 0
    st.session_state.keuze = ""
    st.session_state.feedback_toon = False
    st.session_state.klaar_voor_volgende = False

# Eindscherm
if st.session_state.huidige_index >= len(st.session_state.vragenlijst):
    score = st.session_state.goed_geraden
    totaal = len(st.session_state.vragenlijst)
    percentage = (score / totaal) * 100

    st.success(f"🎉 Je hebt {score} van de {totaal} goed ({percentage:.1f}%)!")

    # Kopieerbare tekst
    deeltekst = f"Ik had {score} van de {totaal} goed in de GroenLinks-PvdA Provinciequiz! 🇳🇱🧠 #provinciequiz"

    st.markdown("### Deel jouw score:")
    st.code(deeltekst, language="markdown")
    st.markdown("""
        <button onclick="navigator.clipboard.writeText(`%s`)" style="background-color:#01A747;color:white;padding:0.5em 1em;border:none;border-radius:6px;font-weight:bold;">
            📋 Kopieer naar klembord
        </button>
        <br><br>
    """ % deeltekst, unsafe_allow_html=True)

    if st.button("🔁 Probeer opnieuw"):
        for key in ["vragenlijst", "huidige_index", "goed_geraden", "keuze", "feedback_toon", "klaar_voor_volgende"]:
            del st.session_state[key]
        st.rerun()

    st.stop()

# Vraag
vraag = st.session_state.vragenlijst[st.session_state.huidige_index]
plaats = vraag["woonplaats"]
juiste_provincie = vraag["provincie"]

# Voortgang
vraagnummer = st.session_state.huidige_index + 1
st.markdown(f"🔄 **Vraag {vraagnummer} van 15**")
st.markdown(f"📍 In welke provincie ligt de plaats _{plaats}_?")

# Antwoordkeuze
antwoord = st.selectbox("Kies de provincie:", [""] + alle_provincies, index=0, key="keuze")

# Verwerking
if antwoord and not st.session_state.feedback_toon:
    st.session_state.feedback_toon = True
    if antwoord == juiste_provincie:
        st.success("✅ Goed geraden!")
        st.session_state.goed_geraden += 1
    else:
        st.error(f"❌ Fout! Het juiste antwoord is: **{juiste_provincie}**")

    # Animatie/vertraging met voortgang
    with st.empty():
        bar = st.progress(0)
        for i in range(80):
            time.sleep(0.012)  # 1s
            bar.progress(i + 1)

    # Naar volgende
    st.session_state.huidige_index += 1
    st.session_state.keuze = ""
    st.session_state.feedback_toon = False
    st.rerun()

# Resetknop in de sidebar
with st.sidebar:
    if st.button("🔁 Opnieuw beginnen"):
        for key in ["vragenlijst", "huidige_index", "goed_geraden", "keuze", "feedback_toon", "klaar_voor_volgende"]:
            del st.session_state[key]
        st.rerun()