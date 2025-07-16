
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

# Initialiseer sessiestatus
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state:
    st.session_state.vraag = df.sample(1).iloc[0]
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "show_new_question" not in st.session_state:
    st.session_state.show_new_question = False

# Nieuwe vraag na beantwoording
if st.session_state.show_new_question:
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.feedback = None
    st.session_state.show_new_question = False

plaats = st.session_state.vraag["Regio's"]
provincie = st.session_state.vraag["Provincie Naam (Naam)"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Formulier
with st.form("quiz"):
    antwoord = st.text_input("Typ hier je antwoord:")
    submitted = st.form_submit_button("Indienen")

# Beoordeling
if submitted:
    st.session_state.score["totaal"] += 1
    if antwoord.strip().lower() == provincie.lower():
        st.session_state.score["goed"] += 1
        st.session_state.feedback = ("✅ Goed geraden!", "success")
    else:
        st.session_state.feedback = (f"❌ Fout! Het juiste antwoord is: **{provincie}**", "error")
    st.session_state.show_new_question = True

# Feedback tonen
if st.session_state.feedback:
    msg, status = st.session_state.feedback
    if status == "success":
        st.success(msg)
    else:
        st.error(msg)

    percentage = (st.session_state.score["goed"] / st.session_state.score["totaal"]) * 100
    st.info(f"🎯 Je hebt {st.session_state.score['goed']} van {st.session_state.score['totaal']} goed ({percentage:.1f}%)")

    # Automatische refresh via JS-truc
    st.markdown("""
        <script>
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        </script>
    """, unsafe_allow_html=True)
