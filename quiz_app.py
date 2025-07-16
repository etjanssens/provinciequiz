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

# Initialiseer state
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state:
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.feedback = ""
    st.session_state.antwoordveld = ""

plaats = st.session_state.vraag["woonplaats"]
provincie_juist = st.session_state.vraag["provincie"].strip().lower()

st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

antwoord = st.text_input("Typ hier de provincie:", value=st.session_state.antwoordveld, key="antwoordveld").strip().lower()

# Controle: alleen als invoer een volledige provincienaam is
alle_provincies = [p.lower() for p in df["provincie"].unique()]
if antwoord in alle_provincies:
    if antwoord == provincie_juist:
        st.session_state.score["goed"] += 1
        st.session_state.score["totaal"] += 1
        st.success("✅ Goed geraden!")
    else:
        st.session_state.score["totaal"] += 1
        st.error(f"❌ Fout! Het juiste antwoord is: **{st.session_state.vraag['provincie']}**")

    percentage = (st.session_state.score["goed"] / st.session_state.score["totaal"]) * 100
    st.info(f"🎯 Je hebt {st.session_state.score['goed']} van {st.session_state.score['totaal']} goed ({percentage:.1f}%)")

    # Nieuwe vraag klaarzetten
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.antwoordveld = ""
    st.stop()  # Zorgt voor refresh met nieuwe vraag

# Opnieuw beginnen knop
if st.button("🔁 Opnieuw beginnen"):
    st.session_state.score = {"goed": 0, "totaal": 0}
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.antwoordveld = ""
    st.rerun()