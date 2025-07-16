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

# Initieer sessiestatus
for key, default in {
    "totaal": 0,
    "goed": 0,
    "current_row_index": 0,
    "feedback": "",
    "input_disabled": False,
    "antwoord": "",
    "trigger_next": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Huidige vraag
index = st.session_state.current_row_index
rij = df.iloc[index]
plaats = rij["Regio's"]
provincie_juist = rij["Provincie Naam (Naam)"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Invoerveld + knop
with st.form("quiz_form"):
    antwoord = st.text_input("Typ hier je antwoord:", value="" if st.session_state["trigger_next"] else st.session_state["antwoord"], disabled=st.session_state.input_disabled)
    submitted = st.form_submit_button("Indienen")

# Als formulier werd ingediend
if submitted and not st.session_state.input_disabled:
    st.session_state.totaal += 1
    st.session_state.antwoord = antwoord
    if antwoord.strip().lower() == provincie_juist.lower():
        st.session_state.goed += 1
        st.session_state.feedback = "✅ Goed geraden!"
    else:
        st.session_state.feedback = f"❌ Fout! Het juiste antwoord is: **{provincie_juist}**"
    st.session_state.input_disabled = True
    st.session_state.trigger_next = True

# Feedback tonen buiten het formulier
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

    # Score
    percentage = (st.session_state.goed / st.session_state.totaal) * 100
    st.info(f"🎯 Je hebt {st.session_state.goed} van {st.session_state.totaal} goed ({percentage:.1f}%)")

    # Start timer en prepare volgende vraag — maar NIET in dezelfde render
    time.sleep(1)
    st.session_state.current_row_index = (st.session_state.current_row_index + 1) % len(df)
    st.session_state.feedback = ""
    st.session_state.input_disabled = False
    st.session_state.antwoord = ""
    st.session_state.trigger_next = False
    st.experimental_rerun()