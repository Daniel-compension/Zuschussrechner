import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image

CONFIG_FILE = "config.json"

def load_or_create_config():
    current_year = str(datetime.now().year)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            if current_year in config:
                return config[current_year]
    return None

def save_config(value):
    current_year = str(datetime.now().year)
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    config[current_year] = value
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Seiteneinstellungen
st.set_page_config(page_title="Zuschussrechner", page_icon="💼", layout="centered")

# Logo anzeigen
logo_path = "COMPENSION 2025 - transparenter Hintergrund.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, use_container_width=True)

# Laden der BBG
bbg_aktuell = load_or_create_config()

# Wenn keine BBG gespeichert ist, zuerst abfragen
if bbg_aktuell is None:
    st.markdown("### 🛠️ Beitragsbemessungsgrenze erfassen")
    neue_bbg = st.number_input("Beitragsbemessungsgrenze (jährlich in €)", min_value=10000.0, step=100.0, format="%.2f", value=96600.00)
    if st.button("✅ Speichern"):
        save_config(neue_bbg)
        st.experimental_rerun()
    st.stop()

# Monatliche BBG berechnen
monatliche_bbg = round((bbg_aktuell * 0.04) / 12, 2)

st.markdown("## 💼 Zuschussrechner")
st.write(f"Aktuelle BBG: **{bbg_aktuell:,.2f} € jährlich**, Zuschussgrenze: **{monatliche_bbg:.2f} € monatlich**")

# Eingabefelder
gesamtbeitrag = st.number_input("Gesamtbeitrag (AG + AN + AVWL)", min_value=0.0, step=1.0, format="%.2f")

zuschuss_option = st.selectbox("AG-Zuschuss", ["15%", "20%", "30%", "Individuell"])
if zuschuss_option == "Individuell":
    zuschuss_prozent = st.number_input("Individueller Zuschuss in %", min_value=0.0, max_value=100.0, step=0.5)
else:
    zuschuss_prozent = float(zuschuss_option.replace("%", ""))

avwl_option = st.selectbox("AVWL", ["0,00 €", "13,29 €", "26,59 €", "40 €", "Sonstige"])
if avwl_option == "Sonstige":
    avwl = st.number_input("Sonstige AVWL (€)", min_value=0.0, step=0.5, format="%.2f")
else:
    avwl = float(avwl_option.replace("€", "").replace(",", ".").strip())

zuschuss_auf_avwl = st.checkbox("AG-Zuschuss auf AVWL rechnen")
begrenzen = st.checkbox("Zuschuss auf 4% BBG begrenzen")

if st.button("🧮 Berechnen"):
    beitrag = gesamtbeitrag
    ag_zuschuss_euro = 0
    entgeltumwandlung = 0

    prozentsatz = zuschuss_prozent / 100

    if begrenzen:
        max_bemessung = min(beitrag, monatliche_bbg)
        x = max_bemessung / (1 + prozentsatz)
        ag_zuschuss_euro = x * prozentsatz
        entgeltumwandlung = beitrag - ag_zuschuss_euro - avwl
    elif zuschuss_auf_avwl:
        x = beitrag / (1 + prozentsatz)
        ag_zuschuss_euro = x * prozentsatz
        entgeltumwandlung = beitrag - ag_zuschuss_euro - avwl
    else:
        bemessung = beitrag - avwl
        x = bemessung / (1 + prozentsatz)
        ag_zuschuss_euro = x * prozentsatz
        entgeltumwandlung = beitrag - ag_zuschuss_euro - avwl

    st.success("✅ Ergebnis")
    st.write(f"**AG-Zuschuss:** {ag_zuschuss_euro:.2f} €")
    st.write(f"**Entgeltumwandlung:** {entgeltumwandlung:.2f} €")
    st.write(f"**AVWL:** {avwl:.2f} €")
