
import streamlit as st
import pandas as pd
import random
import time

st.title("🧠 Raad de provincie bij de plaats!")

@st.cache_data
def load_data():
    df = pd.read_csv("woonplaatsen.csv")
    df = df[["Regio's", "Provincie Naam (Naam)"]].dropna()
    df = df.sample(frac=1).reset_index(drop=True)
    return df

df = load_data()

# Score bijhouden
if "totaal" not in st.session_state:
    st.session_state.totaal = 0
if "goed" not in st.session_state:
    st.session_state.goed = 0
if "current_row_index" not in st.session_state:
    st.session_state.current_row_index = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = False

# Huidige vraag ophalen
index = st.session_state.current_row_index
rij = df.iloc[index]
plaats = rij["Regio's"]
provincie_juist = rij["Provincie Naam (Naam)"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Input en knop
with st.form("quiz_form"):
    antwoord = st.text_input("Typ hier je antwoord:", disabled=st.session_state.input_disabled)
    submitted = st.form_submit_button("Indienen")

# Verwerk antwoord
if submitted and not st.session_state.input_disabled:
    st.session_state.totaal += 1
    if antwoord.strip().lower() == provincie_juist.lower():
        st.session_state.goed += 1
        st.session_state.feedback = "✅ Goed geraden!"
    else:
        st.session_state.feedback = f"❌ Fout! Het juiste antwoord is: **{provincie_juist}**"

    # Blokkeer verdere input tijdelijk
    st.session_state.input_disabled = True

    # Toon feedback en score
    st.success(st.session_state.feedback) if "✅" in st.session_state.feedback else st.error(st.session_state.feedback)
    percentage = (st.session_state.goed / st.session_state.totaal) * 100
    st.info(f"🎯 Je hebt {st.session_state.goed} van {st.session_state.totaal} goed ({percentage:.1f}%)")

    # Start timer voor nieuwe vraag
    time.sleep(1)

    # Zet volgende vraag klaar
    st.session_state.current_row_index = (st.session_state.current_row_index + 1) % len(df)
    st.session_state.feedback = ""
    st.session_state.input_disabled = False
    st.experimental_rerun()
