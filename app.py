import streamlit as st
from PIL import Image

# Seiteneinstellungen
st.set_page_config(
    page_title="Zuschussrechner | COMPENSION",
    page_icon="💼",
    layout="centered"
)

# Logo anzeigen
logo = Image.open("COMPENSION 2025 - transparenter Hintergrund.png")
st.image(logo, use_column_width=True)

# Titel & Beschreibung
st.markdown("## 💼 Compension Zuschussrechner")
st.markdown("Berechnet den Arbeitgeberzuschuss und den Entgeltumwandlungsbetrag basierend auf der aktuellen Beitragsbemessungsgrenze.")
st.markdown("---")

# Eingaben
st.subheader("📥 Eingaben")

bbg = st.number_input("Beitragsbemessungsgrenze (jährlich in €)", value=96600.00, step=100.0, format="%.2f")
gesamtbeitrag = st.number_input("Gesamtbeitrag (€)", value=0.0, step=10.0, format="%.2f")

col1, col2 = st.columns(2)
with col1:
    ag_zuschuss_wahl = st.selectbox("AG-Zuschuss", ["15%", "20%", "30%", "Individuell"], index=1)
with col2:
    avwl_wahl = st.selectbox("AVWL", ["0,00 €", "13,29 €", "26,59 €", "40 €", "Sonstige"], index=2)

if ag_zuschuss_wahl == "Individuell":
    ag_zuschuss_prozent = st.number_input("Individueller AG-Zuschuss (%)", value=20.0)
else:
    ag_zuschuss_prozent = float(ag_zuschuss_wahl.strip('%'))

if avwl_wahl == "Sonstige":
    avwl = st.number_input("Individueller AVWL (€)", value=0.0)
else:
    avwl = float(avwl_wahl.replace("€", "").replace(",", ".").strip())

zuschuss_auf_avwl = st.checkbox("AG-Zuschuss auf AVWL rechnen")
begrenzen = st.checkbox("Zuschuss auf 4% BBG begrenzen")

st.markdown("---")
if st.button("🧮 Berechnen"):
    ag_zuschuss_prozent_decimal = ag_zuschuss_prozent / 100
    bbg_monatlich = round((bbg * 0.04) / 12, 2)

    if begrenzen:
        max_bemessung = min(gesamtbeitrag, bbg_monatlich)
        x = max_bemessung / (1 + ag_zuschuss_prozent_decimal)
        ag_zuschuss_euro = x * ag_zuschuss_prozent_decimal
        entgeltumwandlung = gesamtbeitrag - ag_zuschuss_euro - avwl
    elif zuschuss_auf_avwl:
        x = gesamtbeitrag / (1 + ag_zuschuss_prozent_decimal)
        ag_zuschuss_euro = x * ag_zuschuss_prozent_decimal
        entgeltumwandlung = gesamtbeitrag - ag_zuschuss_euro - avwl
    else:
        bemessung = gesamtbeitrag - avwl
        x = bemessung / (1 + ag_zuschuss_prozent_decimal)
        ag_zuschuss_euro = x * ag_zuschuss_prozent_decimal
        entgeltumwandlung = gesamtbeitrag - ag_zuschuss_euro - avwl

    st.success("✅ Ergebnis")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("AG-Zuschuss (€)", f"{ag_zuschuss_euro:.2f}")
        st.metric("AVWL (€)", f"{avwl:.2f}")
    with col2:
        st.metric("Entgeltumwandlung (€)", f"{entgeltumwandlung:.2f}")
        st.metric("AG-Zuschuss (%)", f"{ag_zuschuss_prozent:.2f}%")
