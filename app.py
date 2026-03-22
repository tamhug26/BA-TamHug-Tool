import streamlit as st
import pandas as pd
import numpy as np

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

#Zeitdimension mit Dataframe
def create_base_dataframe(year=2025):
    zeitindex = pd.date_range(
        start=f"{year}-01-01 00:00",
        end=f"{year}-12-31 23:00",
        freq="h"
    )
    df = pd.DataFrame(index=zeitindex)
    df["Monat"] = df.index.month
    df["Stunde"] = df.index.hour
    df["Tag_im_Jahr"] = df.index.dayofyear
    return df
def add_household_load_profile(df, jahresstromverbrauch):
    df = df.copy()
    # Einfaches Tagesprofil
    # nachts tief, morgens etwas höher, abends am höchsten
    stundenfaktoren = {
        0: 0.4, 1: 0.35, 2: 0.3, 3: 0.3, 4: 0.35, 5: 0.5,
        6: 0.8, 7: 1.0, 8: 0.9, 9: 0.7, 10: 0.6, 11: 0.6,
        12: 0.7, 13: 0.6, 14: 0.6, 15: 0.7, 16: 0.9, 17: 1.2,
        18: 1.4, 19: 1.5, 20: 1.3, 21: 1.0, 22: 0.7, 23: 0.5
    }
    df["haus_faktor"] = df["Stunde"].map(stundenfaktoren)
    # auf Jahresstromverbrauch normieren
    faktor_summe = df["haus_faktor"].sum()
    df["hauslast_kWh"] = df["haus_faktor"] / faktor_summe * jahresstromverbrauch
    return df
def add_heating_profile(df, heizwaermebedarf_jahr):
    df = df.copy()
    # Heizanteile pro Monat (typisches Schweizer EFH)
    monatsanteile = {
        1: 0.17,
        2: 0.15,
        3: 0.12,
        4: 0.08,
        5: 0.04,
        6: 0.01,
        7: 0.00,
        8: 0.01,
        9: 0.03,
        10: 0.09,
        11: 0.14,
        12: 0.16
    }
    df["heiz_monat"] = df["Monat"].map(monatsanteile)
    # leichtes Tagesprofil
    stundenfaktoren = {
        0:0.9,1:0.85,2:0.8,3:0.8,4:0.85,5:1.0,
        6:1.1,7:1.2,8:1.1,9:1.0,10:0.95,11:0.95,
        12:0.9,13:0.9,14:0.9,15:0.95,16:1.0,17:1.1,
        18:1.2,19:1.25,20:1.2,21:1.1,22:1.0,23:0.95
    }
    df["heiz_stunde"] = df["Stunde"].map(stundenfaktoren)
    df["heiz_faktor"] = df["heiz_monat"] * df["heiz_stunde"]
    faktor_summe = df["heiz_faktor"].sum()
    if faktor_summe > 0:
        df["heizwaerme_kWh"] = df["heiz_faktor"] / faktor_summe * heizwaermebedarf_jahr
    else:
        df["heizwaerme_kWh"] = 0
    return df


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


st.write("------------------------------")
st.subheader("Test Zeitreihe")

df_ts = create_base_dataframe()

df_ts = add_household_load_profile(df_ts, jahresstromverbrauch)

# Heizwärmebedarf übernehmen (oder Testwert)
if "Heizwaermebedarf_input" in locals():
    heizwaerme_jahr = Heizwaermebedarf_input
else:
    heizwaerme_jahr = 12000

df_ts = add_heating_profile(df_ts, heizwaerme_jahr)

st.write("Anzahl Stunden im Jahr:", len(df_ts))
st.write("Summe Haushaltsstrom [kWh/a]:", round(df_ts["hauslast_kWh"].sum(), 2))

st.write("Erste 24 Stunden:")
st.dataframe(df_ts[["Monat","Stunde","hauslast_kWh","heizwaerme_kWh"]].head(24))

st.write("Haushaltslast über 24 Stunden:")
st.bar_chart(df_ts["hauslast_kWh"].head(24))

st.write("Haushaltslast über 7 Tage:")
st.line_chart(df_ts[["hauslast_kWh","heizwaerme_kWh"]].head(168))