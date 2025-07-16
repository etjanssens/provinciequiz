import streamlit as st
import pandas as pd

st.set_page_config(page_title="Raad de provincie", page_icon="🧠")

st.title("🧠 Raad de provincie bij de plaats!")

@st.cache_data
def load_data():
    df = pd.read_csv("woonplaatsen.csv")
    if "woonplaats" not in df.columns or "provincie" not in df.columns:
        st.error("CSV mist kolommen 'woonplaats' en/of 'provincie'.")
        st.stop()
    return df[["woonplaats", "provincie"]].dropna().drop_duplicates()

df = load_data()

# Init state
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state:
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.antwoord = ""
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Vraag
plaats = st.session_state.vraag["woonplaats"]
provincie_juist = st.session_state.vraag["provincie"].strip().lower()
alle_provincies = [p.lower() for p in df["provincie"].unique()]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Antwoordveld
antwoord = st.text_input("Typ hier de provincie:", value=st.session_state.antwoord, key="antwoordveld").strip().lower()
st.session_state.antwoord = antwoord

# Automatische controle als volledige provincienaam
if not st.session_state.show_feedback and antwoord in alle_provincies:
    st.session_state.score["totaal"] += 1
    if antwoord == provincie_juist:
        st.session_state.score["goed"] += 1
        st.session_state.feedback = "✅ Goed geraden!"
    else:
        st.session_state.feedback = f"❌ Fout! Het juiste antwoord is: **{st.session_state.vraag['provincie']}**"
    st.session_state.show_feedback = True
    st.rerun()

# Feedback tonen
if st.session_state.show_feedback:
    if st.session_state.feedback.startswith("✅"):
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

    goed = st.session_state.score["goed"]
    totaal = st.session_state.score["totaal"]
    percentage = (goed / totaal) * 100
    st.info(f"🎯 Je hebt {goed} van {totaal} goed ({percentage:.1f}%)")

    # Volgende vraag-knop
    if st.button("Volgende vraag"):
        st.session_state.vraag = df.sample(1).iloc[0]
        st.session_state.antwoord = ""
        st.session_state.feedback = ""
        st.session_state.show_feedback = False
        st.rerun()

# Reset-knop
with st.sidebar:
    if st.button("🔁 Opnieuw beginnen"):
        st.session_state.score = {"goed": 0, "totaal": 0}
        st.session_state.vraag = df.sample(1).iloc[0]
        st.session_state.antwoord = ""
        st.session_state.feedback = ""
        st.session_state.show_feedback = False
        st.rerun()