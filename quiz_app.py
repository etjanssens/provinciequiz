
import streamlit as st
import pandas as pd
import random
import time

st.title("🧠 Raad de provincie bij de plaats!")

@st.cache_data
def load_data():
    df = pd.read_csv("woonplaatsen.csv")
    df = df[["Regio's", "Provincie Naam (Naam)"]].dropna()
    df = df.sample(frac=1).reset_index(drop=True)  # shuffle bij laden
    return df

df = load_data()

# Score bijhouden
if "totaal" not in st.session_state:
    st.session_state.totaal = 0
if "goed" not in st.session_state:
    st.session_state.goed = 0

# Vraag bijhouden
if "current_row_index" not in st.session_state:
    st.session_state.current_row_index = 0

# Selecteer rij op index
index = st.session_state.current_row_index
rij = df.iloc[index]
plaats = rij["Regio's"]
provincie_juist = rij["Provincie Naam (Naam)"]

# Toon vraag
st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

antwoord = st.text_input("Typ hier je antwoord:")

# Verwerk antwoord
if antwoord:
    st.session_state.totaal += 1
    if antwoord.strip().lower() == provincie_juist.lower():
        st.session_state.goed += 1
        st.success("✅ Goed geraden!")
    else:
        st.error(f"❌ Fout! Het juiste antwoord is: **{provincie_juist}**")

    # Toon score
    percentage = (st.session_state.goed / st.session_state.totaal) * 100
    st.info(f"🎯 Je hebt {st.session_state.goed} van {st.session_state.totaal} goed ({percentage:.1f}%)")

    # Wacht 1 seconde en laad volgende vraag
    time.sleep(1)
    st.session_state.current_row_index = (st.session_state.current_row_index + 1) % len(df)
    st.experimental_rerun()
