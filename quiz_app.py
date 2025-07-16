
import streamlit as st
import pandas as pd
import random

st.title("🧠 Raad de provincie bij de plaats!")

@st.cache_data
def load_data():
    df = pd.read_csv("woonplaatsen.csv")
    df = df[["Regio's", "Provincie Naam (Naam)"]].dropna()
    return df

df = load_data()

if "current_row" not in st.session_state:
    st.session_state.current_row = df.sample(1).iloc[0]

plaats = st.session_state.current_row["Regio's"]
provincie_juist = st.session_state.current_row["Provincie Naam (Naam)"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

antwoord = st.text_input("Typ hier je antwoord:")

if antwoord:
    if antwoord.strip().lower() == provincie_juist.lower():
        st.success("✅ Goed geraden!")
    else:
        st.error(f"❌ Fout! Het juiste antwoord is: **{provincie_juist}**")

if st.button("🔁 Nieuwe vraag"):
    st.session_state.current_row = df.sample(1).iloc[0]
    st.experimental_rerun()
