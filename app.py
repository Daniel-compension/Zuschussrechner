import streamlit as st

st.set_page_config(page_title="Compension Zuschussrechner", layout="centered")

st.title("💼 Compension Zuschussrechner")

# Eingabe der BBG
bbg = st.number_input("Beitragsbemessungsgrenze (jährlich in €)", value=96600)

# Eingabe des Gesamtbeitrags
gesamtbeitrag = st.number_input("Gesamtbeitrag", value=0.0, step=10.0, format="%.2f")

# AG-Zuschuss Auswahl
ag_zuschuss_optionen = ["15%", "20%", "30%", "Individuell"]
ag_zuschuss_wahl = st.selectbox("AG-Zuschuss", ag_zuschuss_optionen, index=1)

if ag_zuschuss_wahl == "Individuell":
    ag_zuschuss_prozent = st.number_input("Individueller AG-Zuschuss in %", value=20.0)
else:
    ag_zuschuss_prozent = float(ag_zuschuss_wahl.strip('%'))

# AVWL Auswahl
avwl_optionen = ["0,00 €", "13,29 €", "26,59 €", "40 €", "Sonstige"]
avwl_wahl = st.selectbox("AVWL", avwl_optionen, index=2)

if avwl_wahl == "Sonstige":
    avwl = st.number_input("Individueller AVWL in €", value=0.0)
else:
    avwl = float(avwl_wahl.replace("€", "").replace(",", ".").strip())

# Optionen
zuschuss_auf_avwl = st.checkbox("AG-Zuschuss auf AVWL rechnen", value=False)
begrenzen = st.checkbox("Zuschuss auf 4% BBG begrenzen", value=False)

# Ergebnis anzeigen
if st.button("Berechnen"):
    ag_zuschuss_prozent_decimal = ag_zuschuss_prozent / 100

    if begrenzen:
        max_bemessung = min(gesamtbeitrag, round((bbg * 0.04) / 12, 2))
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
    st.write(f"**AG-Zuschuss:** {ag_zuschuss_euro:.2f} €")
    st.write(f"**Entgeltumwandlung:** {entgeltumwandlung:.2f} €")
    st.write(f"**AVWL:** {avwl:.2f} €")
    st.write(f"**AG-Zuschuss (%):** {ag_zuschuss_prozent:.2f}%")
