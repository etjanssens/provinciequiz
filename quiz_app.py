import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Raad de provincie", page_icon="🧠")

st.title("🧠 Raad de provincie bij de plaats!")

@st.cache_data
def load_data():
    df = pd.read_csv("woonplaatsen.csv")
    if "woonplaats" not in df.columns or "provincie" not in df.columns:
        st.error("CSV mist kolommen 'woonplaats' en/of 'provincie'.")
        st.stop()
    return df[["woonplaats", "provincie"]].dropna().drop_duplicates()

# ❗ EERST laden, daarna pas gebruiken
df = load_data()
alle_provincies = sorted(df["provincie"].unique())

# Initialiseer sessiestatus
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state:
    st.session_state.vraag = df.sample(1).iloc[0]
if "laatste_antwoord" not in st.session_state:
    st.session_state.laatste_antwoord = ""

# Vraag tonen
plaats = st.session_state.vraag["woonplaats"]
juiste_provincie = st.session_state.vraag["provincie"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Dropdown met provincies
antwoord = st.selectbox("Kies de provincie:", [""] + alle_provincies, index=0)

# Check zodra iets nieuws gekozen is
if antwoord and antwoord != st.session_state.laatste_antwoord:
    st.session_state.score["totaal"] += 1
    st.session_state.laatste_antwoord = antwoord

    if antwoord == juiste_provincie:
        st.session_state.score["goed"] += 1
        st.success("✅ Goed geraden!")
    else:
        st.error(f"❌ Fout! Het juiste antwoord is: **{juiste_provincie}**")

    goed = st.session_state.score["goed"]
    totaal = st.session_state.score["totaal"]
    percentage = (goed / totaal) * 100
    st.info(f"🎯 Je hebt {goed} van {totaal} goed ({percentage:.1f}%)")

    time.sleep(2)
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.laatste_antwoord = ""
    st.rerun()

# Resetknop
with st.sidebar:
    if st.button("🔁 Opnieuw beginnen"):
        st.session_state.score = {"goed": 0, "totaal": 0}
        st.session_state.vraag = df.sample(1).iloc[0]
        st.session_state.laatste_antwoord = ""
        st.rerun()