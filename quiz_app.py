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

df = load_data()
alle_provincies = sorted(df["provincie"].unique())

# Initialiseer sessiestate
if "score" not in st.session_state:
    st.session_state.score = {"goed": 0, "totaal": 0}
if "vraag" not in st.session_state:
    st.session_state.vraag = df.sample(1).iloc[0]
if "keuze" not in st.session_state:
    st.session_state.keuze = ""
if "klaar_voor_volgende" not in st.session_state:
    st.session_state.klaar_voor_volgende = False

# Score altijd tonen
goed = st.session_state.score["goed"]
totaal = st.session_state.score["totaal"]
percentage = (goed / totaal * 100) if totaal > 0 else 0
st.info(f"🎯 Je hebt {goed} van {totaal} goed ({percentage:.1f}%)")

# Volgende vraag klaarzetten als vorige was beantwoord
if st.session_state.klaar_voor_volgende:
    st.session_state.vraag = df.sample(1).iloc[0]
    st.session_state.keuze = ""
    st.session_state.klaar_voor_volgende = False
    st.rerun()

# Toon vraag
plaats = st.session_state.vraag["woonplaats"]
juiste_provincie = st.session_state.vraag["provincie"]
st.markdown(f"📍 **In welke provincie ligt de plaats _{plaats}_?**")

# Forceer focus op de selectbox via JavaScript
st.components.v1.html("""
<script>
    const select = window.parent.document.querySelector('select');
    if (select) { select.focus(); }
</script>
""", height=0)

# Dropdown (geheugenvriendelijk)
index = 0
if st.session_state.keuze in alle_provincies:
    index = alle_provincies.index(st.session_state.keuze) + 1

antwoord = st.selectbox(
    "Kies de provincie:",
    [""] + alle_provincies,
    index=index,
    key="keuze"
)

# Antwoordverwerking
if antwoord and not st.session_state.klaar_voor_volgende:
    st.session_state.score["totaal"] += 1
    if antwoord == juiste_provincie:
        st.session_state.score["goed"] += 1
        st.success("✅ Goed geraden!")
    else:
        st.error(f"❌ Fout! Het juiste antwoord is: **{juiste_provincie}**")

    st.session_state.klaar_voor_volgende = True
    time.sleep(2)
    st.rerun()

# Opnieuw beginnen
with st.sidebar:
    if st.button("🔁 Opnieuw beginnen"):
        st.session_state.score = {"goed": 0, "totaal": 0}
        st.session_state.vraag = df.sample(1).iloc[0]
        st.session_state.keuze = ""
        st.session_state.klaar_voor_volgende = False
        st.rerun()