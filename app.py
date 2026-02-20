import streamlit as st

st.title("PV Dimensionierungshilfe")

pv_leistung = st.slider("PV-Peakleistung (kWp)", 0, 30, 10)
batterie = st.slider("Batteriekapazität (kWh)", 0, 20, 10)
jahresverbrauch = st.number_input("Jahresstrombedarf (kWh/a)", 1000, 10000, 4500)

st.metric("PV-Leistung", f"{pv_leistung} kWp")
st.metric("Batterie", f"{batterie} kWh")
st.metric("Jahresverbrauch", f"{jahresverbrauch} kWh/a")
st.metric("test", f"{jahresverbrauch} kWh/a")