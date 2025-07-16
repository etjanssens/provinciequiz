
import streamlit as st
import pandas as pd
import random

st.title("🧠 Raad de provincie bij de plaats!")

@st.cache_data
def load_data():
    import os
    st.write("Bestanden in map:", os.listdir())  # Debug: wat ziet Streamlit?

    try:
        df = pd.read_csv("woonplaatsen.csv")
        st.write("Kolommen ingelezen:", df.columns.tolist())  # Debug: wat is er binnengekomen?

        if "woonplaats" in df.columns and "provincie" in df.columns:
            df = df[["woonplaats", "provincie"]].dropna().drop_duplicates()
            return df
        else:
            st.error("❌ Vereiste kolommen 'woonplaats' en/of 'provincie' ontbreken.")
            st.stop()
    except FileNotFoundError:
        st.error("📁 Bestand 'woonplaatsen.csv' niet gevonden. Staat het in je repo?")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Onverwachte fout bij laden CSV: {e}")
        st.stop()

df = load_data()

# Initialiseer score
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state or st.session_state.get("nieuwe_vraag", True):
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.feedback = ""
    st.session_state.nieuwe_vraag = False

plaats = st.session_state.vraag["woonplaats"]
provincie_juist = st.session_state.vraag["provincie"]

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Formulier
with st.form("quiz_form"):
    antwoord = st.text_input("Typ hier je antwoord:")
    submitted = st.form_submit_button("Indienen")

# Verwerk antwoord
if submitted:
    st.session_state.score["totaal"] += 1
    if antwoord.strip().lower() == provincie_juist.lower():
        st.session_state.score["goed"] += 1
        st.session_state.feedback = "✅ Goed geraden!"
    else:
        st.session_state.feedback = f"❌ Fout! Het juiste antwoord is: **{provincie_juist}**"
    st.session_state.nieuwe_vraag = True

# Toon feedback
if st.session_state.feedback:
    if st.session_state.feedback.startswith("✅"):
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)
    percentage = (st.session_state.score["goed"] / st.session_state.score["totaal"]) * 100
    st.info(f"🎯 Je hebt {st.session_state.score['goed']} van {st.session_state.score['totaal']} goed ({percentage:.1f}%)")

    # Automatische herlaad na 1 seconde
    st.markdown("""
        <script>
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        </script>
    """, unsafe_allow_html=True)
