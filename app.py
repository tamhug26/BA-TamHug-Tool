import streamlit as st

st.title("PV Dimensionierungshilfe")
st.markdown("markdown")
st.caption("caption")
st.latex("latex")
st.write("write")
st.header("header")
st.subheader("subheader")
st.code("code")

left, middle, right = st.columns(3)
if left.button("Plain button", width="stretch"):
    left.markdown("You clicked the plain button.")
if middle.button("Emoji button", icon="😃", width="stretch"):
    middle.markdown("You clicked the emoji button.")
if right.button("Material button", icon=":material/mood:", width="stretch"):
    right.markdown("You clicked the Material button.")

st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

if st.button("Aloha", type="secondary"):
    st.write("Ciao")


if st.button("Aloha", type="tertiary"):
    st.write("Ciao")



#-----------------------------------
EVU = {
    "IWB": 12.88, #industrielle Werke Basel
    "EBL": 50.1, #Elektra Baselland
    "BKW": 84, #Bernische Kraftwerke AG Energie AG
    "Elektra Zeiningen": 59, #Elektra Zeiningen
    "CKW": 20, #Centralschweizerische Kraftwerke
    "EKZ": 48.3, #Elektrizitätswerke des Kantons Zürich"
    "EWZ": 15.9,
    "Axpo Holding AG": 62,
    "Alpiq AG": 13.4,
    "Repower AG": 131,
    "Romande Energie": 11.3,
    "Schweiz": 59
}

#inputs:
pv_Peakleistung = st.slider("PV-Peakleistung (kWp)", 0, 30, 10)
Dachneigung = st.number_input("Dachneigung (°)", 0, 360, 180)
#Dachausrichtung = 
EVU_name = st.selectbox(
    "EVU wählen",
    list(EVU.keys())
)
CO2Emmisionen = EVU[EVU_name]
st.write("CO2 Emmisionen:", CO2Emmisionen, "kg CO2e/MWh")

batteriekapazität = st.slider("Batteriekapazität (kWh)", 0, 20, 10)
maxLadeleistungBatterie = st.slider("max. Ladeleistung der Batterie (kW)", 0, 20, 10)
maxEntladeleistungBatterie = st.slider("max. Entladeleistung der Batterie (kW)", 0, 20, 10)
minSoC = st.number_input("Min. SoC (%)", 0, 50, 20)
maxSoC = st.number_input("Max. SoC (%)", 60, 100, 80)
# regel einbauen minSoC muss < sein als maxSoC
Einspeisegrenze = st.number_input("Einspeisegrenze (%)", 60, 100, 70)
EinspeisegrenzekW = (Einspeisegrenze/100)* pv_Peakleistung
st.write("Einspeisegrenze kW:", EinspeisegrenzekW, "kW")
Bezugsgrenze = st.number_input("Bezugsgrenze (kW)", 60, 100, 80)
Jahresheizwärmebedarf = st.number_input("Jahresheizwärmebedarf (kWh/a)", 1000, 10000, 4500)
jahresverbrauch = st.number_input("Jahresstrombedarf (kWh/a)", 1000, 10000, 4500)

JahresarbeitszahlJAZ = st.number_input("Jahresarbeitszahl JAZ (-)", 1000, 10000, 4500)
#CO2Emissionen = 

#Outputs:
WärmeStrombedarf = Jahresheizwärmebedarf / JahresarbeitszahlJAZ

st.metric("WärmeStrombedarf", f"{WärmeStrombedarf} kWp")
st.metric("Batterie", f"{batteriekapazität} kWh")
st.metric("Jahresverbrauch", f"{jahresverbrauch} kWh/a")
