import streamlit as st
import pandas as pd

#Tabellen bzw Dataframes
Standort = {
    "Adelboden" : -10,
    "Aigle" : -6,
    "Altdorf" : -6,
    "Basel-Binningen" : -7,
    "Bern-Liebefeld" : -7,
    "Buchs-Aarau" : -7,
    "Chur" : -7,
    "Davos" : -13,
    "Disentis" : -10,
    "Engelberg" : -11,
    "Genève-Cointrin" : -4,
    "Glarus" : -8,
    "Grand-St-Bernard" : -15,
    "Güttingen" : -7,
    "Interlaken" : -7,
    "La Chaux-de-Fonds" : -10,
    "La Frétaz" : -10,
    "Locarno-Monti" : -1,
    "Lugano" : -1,
    "Luzern" : -6,
    "Magadino" : -3,
    "Montana" : -10,
    "Neuchâtel" : -5,
    "Payerne" : -7,
    "Piotta" : -7,
    "Pully" : -4,
    "Robbia" : -8,
    "Rünenberg" : -8,
    "Samedan" : -18,
    "San Bernardino" : -11,
    "St. Gallen" : -9,
    "Schaffhausen" : -8,
    "Scuol" : -12,
    "Sion" : -6,
    "Ulrichen" : -16,
    "Vaduz" : -8,
    "Wynau" : -7,
    "Zermatt" : -11,
    "Zürich-Kloten" : -8,
    "Zürich-MeteoSchweiz" : -8
}

df_Bautyp_Heizwaermebedarf = pd.DataFrame({
    "Bautyp" : list(range(1901, 2016)) + ["Minergie", "Minergie-P"],
    "Heizwaermebedarf" : (
    [140]*20 +
    [150]*30 +
    [160]*15 +
    [170]*13 +
    [162]*3 +
    [130]*2 +
    [110]*6 +
    [90]*13 +
    [70]*7 +
    [50]*6 +
    [40] +
    [30]
    )
})

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

st.header("Dimensionierungstool")

EBFm2 = st.number_input("Energiebezugsfläche bzw m2", 50, 5000, 200)
Standort = st.selectbox(
    "Standort wählen",
    list(Standort.keys())
) 

st.subheader("Heizwärmebedarf ermittlung")
# aus Baujahr Heizwärmebedarf kWh/m2
m2 = st.number_input("Fläche des EFH [m2]", 50, 5000, 200)
bau_typ = st.selectbox(
    "Gebäudestandard",
    ["Baujahr", "Minergie", "Minergie-P"]
)
if bau_typ == "Baujahr":
    Baujahr = st.number_input("Baujahr", 1900, 2015, 1990)
    treffer = df_Bautyp_Heizwaermebedarf.loc[df_Bautyp_Heizwaermebedarf["Bautyp"] == Baujahr, "Heizwaermebedarf"]
    if not treffer.empty:
        Heizwaermebedarf = treffer.iloc[0] * m2
        saniert = st.radio(
            "Wurde das Gebäude saniert?",
            ["Nein", "Ja"],
            horizontal=True
        )
        reduktion = 0.0
        if saniert == "Ja":
            Sanierungstyp = st.multiselect(
                "Sanierungtyp",
                ["Dämmung Dach", "neue Fenster", "Dämmung Fassade"],
            )
            reduktionen = {
                "Dämmung Dach": 0.15,
                "neue Fenster": 0.15,
                "Dämmung Fassade": 0.25
            }
            reduktion = sum(reduktionen[typ] for typ in Sanierungstyp)
        Heizwaermebedarf_total = Heizwaermebedarf * (1 - reduktion)
        Heizwaermebedarf_input = st.number_input(
            "Heizwärmebedarf kWh/a",
            value=int(Heizwaermebedarf_total)
        )
        ergebnis = Heizwaermebedarf_input
    else:
        st.error("Dieses Baujahr wurde in der Tabelle nicht gefunden.")
elif bau_typ == "Minergie":
    treffer = df_Bautyp_Heizwaermebedarf.loc[df_Bautyp_Heizwaermebedarf["Bautyp"] == bau_typ, "Heizwaermebedarf"]
    if not treffer.empty:
        Heizwaermebedarf = treffer.iloc[0] * m2
        Heizwaermebedarf_input = st.number_input(
            "Heizwärmebedarf kWh/m2",
            value=int(Heizwaermebedarf)
        )
        ergebnis = Heizwaermebedarf_input
    else:
        st.error("Dieses Baujahr wurde in der Tabelle nicht gefunden.")
elif bau_typ == "Minergie-P":
    treffer = df_Bautyp_Heizwaermebedarf.loc[df_Bautyp_Heizwaermebedarf["Bautyp"] == bau_typ, "Heizwaermebedarf"]
    if not treffer.empty:
        Heizwaermebedarf = treffer.iloc[0] * m2
        Heizwaermebedarf_input = st.number_input(
            "Heizwärmebedarf kWh/m2",
            value=int(Heizwaermebedarf)
        )
        ergebnis = Heizwaermebedarf_input
    else:
        st.error("Dieses Baujahr wurde in der Tabelle nicht gefunden.")

st.subheader("Heizsystem")

heizsystem = st.segmented_control(
    "Heizsystem wählen", ["Fossil", "Wärmepumpe"],
    default="Fossil"
)
if heizsystem == "Fossil":
    fossil_typ = st.radio(
        "Fossiles Heizsystem",
        ["Gas", "Öl", "Pellets"],
        horizontal=True
    )
    if fossil_typ == "Gas":
        gas = Heizwaermebedarf / 10
        Gasverbrauch_input = st.number_input(
            "Gasverbrauch m³/a",
            value=int(gas)
        )
        ergebnis = Gasverbrauch_input
        st.write("Emissionen UBP/a: ")
        st.write("Emissionen kgCO2/a: ")
    elif fossil_typ == "Öl":
        oel = Heizwaermebedarf / 10
        Oelverbrauch_input = st.number_input(
            "Ölverbrauch L/a",
            value=int(oel)
        )
        ergebnis = Oelverbrauch_input
        st.write("Emissionen UBP/a: ")
        st.write("Emissionen kgCO2/a: ")
    elif fossil_typ == "Pellets":
        pellets = Heizwaermebedarf / 5
        Pelletsverbrauch_input = st.number_input(
            "Pelletsverbrauch kg/a",
            value=int(pellets)
        )
        ergebnis = Pelletsverbrauch_input
        st.write("Emissionen UBP/a: ")
        st.write("Emissionen kgCO2/a: ")
    # noch emmisionen draus rechnen
    # .1f = 1 Nachkommastelle zb st.write(f"Gasverbrauch: {gas:.1f} m³/a")
    # variablen direkt in text als f-String (formatted string).
elif heizsystem == "Wärmepumpe":
    wp_typ = st.radio(
        "Wärmepumpenart",
        [
            "Luft/Wasser Wärmepumpe",
            "Sole/Wasser Wärmepumpe",
            "Wasser/Wasser Wärmepumpe"
        ],
        horizontal=True
    )
    if wp_typ == "Luft/Wasser Wärmepumpe":
        jaz = st.number_input("JAZ", min_value=0.1, max_value=10.0, value=2.5, step=0.1)
    elif wp_typ == "Sole/Wasser Wärmepumpe":
        jaz = st.number_input("JAZ", min_value=0.1, max_value=10.0, value=4.5, step=0.1)
    else:
        jaz = st.number_input("JAZ", min_value=0.1, max_value=10.0, value=4.0, step=0.1)
    stromverbrauch = Heizwaermebedarf / jaz
    st.write(f"Stromverbrauch: {stromverbrauch:.1f} kWh/a")


st.write("------------------------------")

st.subheader("Photovoltaikanlage")
pv_Peakleistung = st.number_input("PV-Peakleistung (kWp)", 0, 30, 10)
Dachneigung = st.number_input("Dachneigung (°)", 0, 360, 180)
#Dachausrichtung = 

st.write("------------------------------")
st.subheader("Batterie")
batteriekapazität = st.slider("Batteriekapazität (kWh)", 0, 20, 10)
maxLadeleistungBatterie = st.slider("max. Ladeleistung der Batterie (kW)", 0, 20, 10)
maxEntladeleistungBatterie = st.slider("max. Entladeleistung der Batterie (kW)", 0, 20, 10)
minSoC = st.number_input("Min. SoC (%)", 0, 50, 20)
maxSoC = st.number_input("Max. SoC (%)", 60, 100, 80)

st.write("------------------------------")
st.subheader("EVU")
EVU_name = st.selectbox(
    "EVU wählen",
    list(EVU.keys())
)
CO2Emmisionen = EVU[EVU_name]
st.write("CO2 Emmisionen:", CO2Emmisionen, "kg CO2e/MWh")

st.write("------------------------------")
st.subheader("Ein- und Ausspeisen")
# regel einbauen minSoC muss < sein als maxSoC
Einspeisegrenze = st.number_input("Einspeisegrenze (%)", 60, 100, 70)
EinspeisegrenzekW = (Einspeisegrenze/100)* pv_Peakleistung
st.metric("Einspeisegrenze kW:", EinspeisegrenzekW, "kW")
Bezugsgrenze = st.number_input("Bezugsgrenze (kW)", 60, 100, 80)

jahresstromverbrauch = st.number_input("Jahresstrombedarf total(kWh/a)", 1000, 10000, 4500)



