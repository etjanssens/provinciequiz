import streamlit as st
import pandas as pd
import time

# Pagina setup
st.set_page_config(page_title="Raad de provincie", page_icon="🐼")
st.markdown("""
    <style>
    /* Achtergrond met lucht en weilandgevoel */
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
    .stProgress > div > div > div {
        background-color: #01A747;
    }
    .stSidebar {
        background-color: #f7f7f7;
    }
    </style>
""", unsafe_allow_html=True)

# Logo bovenaan
st.markdown(
    '<img src="https://groenlinkspvda.nl/wp-content/uploads/2023/09/GL-PvdA-logo-1.svg" width="220">',
    unsafe_allow_html=True
)

# Titel en subtitel
st.title("🧠 Raad de provincie bij de plaats!")
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

# Session state
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state:
    st.session_state.vraag = df.sample(1).iloc[0]
if "keuze" not in st.session_state:
    st.session_state.keuze = ""
if "klaar_voor_volgende" not in st.session_state:
    st.session_state.klaar_voor_volgende = False

# Score bovenaan
goed = st.session_state.score["goed"]
totaal = st.session_state.score["totaal"]
percentage = (goed / totaal * 100) if totaal > 0 else 0
st.info(f"🎯 Je hebt {goed} van {totaal} goed ({percentage:.1f}%)")

# Nieuwe vraag bij doorloop
if st.session_state.klaar_voor_volgende:
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.keuze = ""
    st.session_state.klaar_voor_volgende = False
    st.rerun()

# Vraag tonen
plaats = st.session_state.vraag["woonplaats"]
juiste_provincie = st.session_state.vraag["provincie"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Dropdown
antwoord = st.selectbox("Kies de provincie:", [""] + alle_provincies, index=0, key="keuze")

# Verwerken
if antwoord and not st.session_state.klaar_voor_volgende:
    st.session_state.score["totaal"] += 1
    if antwoord == juiste_provincie:
        st.session_state.score["goed"] += 1
        st.success("✅ Goed geraden!")
    else:
        st.error(f"❌ Fout! Het juiste antwoord is: **{juiste_provincie}**")

    # Voortgangsbalk (korter)
    st.session_state.klaar_voor_volgende = True
    with st.empty():
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.012)  # 1.2 seconde animatie
            bar.progress(i + 1)
    st.rerun()

# Resetknop
with st.sidebar:
    if st.button("🔁 Opnieuw beginnen"):
        st.session_state.score = {"goed": 0, "totaal": 0}
        st.session_state.vraag = df.sample(1).iloc[0]
        st.session_state.keuze = ""
        st.session_state.klaar_voor_volgende = False
        st.rerun()