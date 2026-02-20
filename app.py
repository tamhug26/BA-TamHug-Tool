import streamlit as st

st.title("PV Dimensionierungshilfe")


#inputs:
pv_Peakleistung = st.slider("PV-Peakleistung (kWp)", 0, 30, 10)
Dachneigung = st.number_input("Dachneigung (°))", 0, 180, 360)
#Dachausrichtung = 
#Standort=
batteriekapazität = st.slider("Batteriekapazität (kWh)", 0, 20, 10)
maxLadeleistungBatterie = st.slider("max. Ladeleistung der Batterie (kW)", 0, 20, 10)
maxEntladeleistungBatterie = st.slider("max. Entladeleistung der Batterie (kW)", 0, 20, 10)
minSoC = st.number_input("Min. SoC (%))", 0, 20, 50)
maxSoC = st.number_input("Max. SoC (%))", 60, 80, 100)
# regel einbauen minSoC muss < sein als maxSoC
Einspeisegrenze = st.number_input("Eispeisegrenze (kW))", 60, 80, 100)
Bezugsgrenze = st.number_input("Bezugsgrenze (kW))", 60, 80, 100)
Jahresheizwärmebedarf = st.number_input("Jahresheizwärmebedarf (kWh/a)", 1000, 10000, 4500)
jahresverbrauch = st.number_input("Jahresstrombedarf (kWh/a)", 1000, 10000, 4500)

JahresarbeitszahlJAZ = st.number_input("Jahresarbeitszahl JAZ (-)", 1000, 10000, 4500)
#CO2Emissionen = 
WärmeStrombedarf = Jahresheizwärmebedarf / JahresarbeitszahlJAZ

st.metric("WärmeStrombedarf", f"{WärmeStrombedarf} kWp")
st.metric("Batterie", f"{batteriekapazität} kWh")
st.metric("Jahresverbrauch", f"{jahresverbrauch} kWh/a")
