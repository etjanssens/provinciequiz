import streamlit as st
import pandas as pd

st.title("🧠 Raad de provincie bij de plaats!")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("woonplaatsen.csv")
        if "woonplaats" in df.columns and "provincie" in df.columns:
            return df[["woonplaats", "provincie"]].dropna().drop_duplicates()
        else:
            st.error("❌ Bestand gevonden, maar kolommen 'woonplaats' en/of 'provincie' ontbreken.")
            st.stop()
    except FileNotFoundError:
        st.error("📁 Bestand 'woonplaatsen.csv' niet gevonden. Zorg dat het in dezelfde map staat als dit script.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Fout bij het laden van de data: {e}")
        st.stop()

df = load_data()

# Initialiseer score en vraag
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state or st.session_state.get("nieuwe_vraag", True):
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.feedback = ""
    st.session_state.nieuwe_vraag = False
    st.session_state.antwoordveld = ""  # Reset invoerveld

plaats = st.session_state.vraag["woonplaats"]
provincie_juist = st.session_state.vraag["provincie"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Invoerveld buiten formulier — automatisch controleren
antwoord = st.text_input("Typ hier de provincie:", key="antwoordveld").strip().lower()
juiste_antwoord = provincie_juist.strip().lower()

# Automatisch controleren als gebruiker iets typt
if antwoord:
    if antwoord == juiste_antwoord:
        st.session_state.score["goed"] += 1
        st.session_state.score["totaal"] += 1
        st.session_state.feedback = "✅ Goed geraden!"
        st.session_state.nieuwe_vraag = True
        st.rerun()
    elif len(antwoord) >= len(juiste_antwoord):
        st.session_state.score["totaal"] += 1
        st.session_state.feedback = f"❌ Fout! Het juiste antwoord is: **{provincie_juist}**"
        st.session_state.nieuwe_vraag = True
        st.rerun()

# Toon feedback + score
if st.session_state.feedback:
    if st.session_state.feedback.startswith("✅"):
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

    percentage = (st.session_state.score["goed"] / st.session_state.score["totaal"]) * 100
    st.info(f"🎯 Je hebt {st.session_state.score['goed']} van {st.session_state.score['totaal']} goed ({percentage:.1f}%)")