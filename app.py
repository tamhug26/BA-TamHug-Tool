import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pvlib
import os
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
#import matplotlib.pyplot as plt
import copy
PROFILE_DIR = "profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)
st.set_page_config(layout="wide")

st.write("Prototyp 2 test4")

#https://ba-tamhug-tool-j82ipmep3hfrkgr36hxv9e.streamlit.app/#dimensionierungstool


#Herstellung und Entsorgung
UBP = {
    "HeizölEL pro kWh":437,
    "Erdgas pro kWh": 279,
    "Pellets pro kWh": 142,
    "Sole Wasser WP 7 kW, Gerät stk": 4690000,
    "Sole Wasser WP 7 kW, Masse kg": 29700,
    "Erdsonden für Sole-Wasser-Wärmepumpe, Sondenlänge m": 46100,
    "Luft Wasser WP 7 kW, Gerät stk": 7440000,
    "Luft Wasser WP 7 kW, Masse kg": 29100,
    "Förder- und Schluckbrunnen für Grundwasser-Wärmepumpe, Gerät stk": 947000,
    "Batterie Li-Ionen 5 kWh, Speicherkap. kWh": 2100000,
    "Batterie Li-Ionen 20 kWh, Speicherkap. kWh": 932000,
    "Solarstromanlage Marktmix, Max. Leistung kWp": 2240000,
    "Solarstromanlage Schrägdach Marktmix, Max. Leistung kWp": 2090000,
    "Solarstromanlage Flachdach Marktmix, Max. Leistung kWp": 2370000,
    "Solarstromanlage Fassade Marktmix, Max. Leistung kWp": 2890000,
    "Solarstromanlage Schrägdach Kleinanlage Mono-Si, Max. Leistung kWp": 2940000,
    "Solarstromanlage Schrägdach Kleinanlage Multi-Si, Max. Leistung kWp": 2980000,
    "Wechselrichter 2.5 kW, Max. Leistung kWp": 534000,
    "Wechselrichter 5 kW, Max. Leistung kWp": 428000,
    "Wechselrichter 10 kW, Max. Leistung kWp": 343000,
    "Wechselrichter 20 kW, Max. Leistung kWp": 274000,
    "Elektroinstallation Photovoltaikanlage": 167000,
    "Wärmeerzeuger spez. Leistungsbedarf 10 W/m², EBF in m²": 1810,
    "Wärmeerzeuger spez. Leistungsbedarf 30 W/m², EBF in m²": 5420,
    "Wärmeerzeuger spez. Leistungsbedarf 50 W/m², EBF in m²": 9030,
}
#Herstellung und Entsorgung
kgCO2eq = {
    "HeizölEL pro kWh": 0.343,
    "Erdgas pro kWh": 0.234,
    "Pellets pro kWh": 0.038,
    "Sole Wasser WP 7 kW, Gerät stk": 2400.00,
    "Sole Wasser WP 7 kW, Masse kg": 15.20,
    "Erdsonden für Sole-Wasser-Wärmepumpe, Sondenlänge m": 23.20,
    "Luft Wasser WP 7 kW, Gerät stk": 4000.00,
    "Luft Wasser WP 7 kW, Masse kg": 15.60,
    "Förder- und Schluckbrunnen für Grundwasser-Wärmepumpe, Gerät stk": 661.00,
    "Batterie Li-Ionen 5 kWh, Speicherkap. kWh": 730.00,
    "Batterie Li-Ionen 20 kWh, Speicherkap. kWh": 332.00,
    "Solarstromanlage Marktmix, Max. Leistung kWp": 1070.00,
    "Solarstromanlage Schrägdach Marktmix, Max. Leistung kWp": 1000.00,
    "Solarstromanlage Flachdach Marktmix, Max. Leistung kWp": 1140.00,
    "Solarstromanlage Fassade Marktmix, Max. Leistung kWp": 1220.00,
    "Solarstromanlage Schrägdach Kleinanlage Mono-Si, Max. Leistung kWp": 1260.00,
    "Solarstromanlage Schrägdach Kleinanlage Multi-Si, Max. Leistung kWp": 1250.00,
    "Wechselrichter 2.5 kW, Max. Leistung kWp": 144.00,
    "Wechselrichter 5 kW, Max. Leistung kWp": 115.00,
    "Wechselrichter 10 kW, Max. Leistung kWp": 92.50,
    "Wechselrichter 20 kW, Max. Leistung kWp": 74.10,
    "Elektroinstallation Photovoltaikanlage": 42.10,
    "Wärmeerzeuger spez. Leistungsbedarf 10 W/m², EBF in m²": 0.86,
    "Wärmeerzeuger spez. Leistungsbedarf 30 W/m², EBF in m²": 2.58,
    "Wärmeerzeuger spez. Leistungsbedarf 50 W/m², EBF in m²": 4.29,
}
#lebenszeit Hausgeräte
LebenszeitJahre = {
    "WP": 20,
    "Batterie": 30, 
    "Fossil/Holzheizung": 20,
    "Erdsonde": 50,
    "Wechselreichter": 15,
    "PV": 30,
}
Auto_Faktoren = {
    "Benzin": {"UBP/Fzkm": 442, "kg CO2-eq/Fzkm": 0.243, "MJ/Fzkm": 4.07},
    "Diesel": {"UBP/Fzkm": 400, "kg CO2-eq/Fzkm": 0.213, "MJ/Fzkm": 3.54},
    "Gas": {"UBP/Fzkm": 378, "kg CO2-eq/Fzkm": 0.196, "MJ/Fzkm": 3.61},
    "E-Auto": {"UBP/Fzkm": 351, "kg CO2-eq/Fzkm": 0.1108, "MJ/Fzkm": 0.0},
}

strompreis_mapping = {
    "9,64": 9.64,
    "20,96": 20.96,
    "32,29": 32.29,
    "43,61": 43.61
}

basis_pfad_weather = "Weather_data"
#dateipfad = f"{basis_pfad_weather}/{dateiname}"

standort_dateien = {
    "Aadorf / Tänikon": "TAE_2023_DRY.csv",
    "Aigle": "AIG_2023_DRY.csv",
    "Altdorf": "ALT_2023_DRY.csv",
    "Basel-Binningen": "BAS_2023_DRY.csv",
    "Bern-Liebefeld": "BER_2023_DRY.csv",
    "Buchs-Aarau": "BUS_2023_DRY.csv",
    "Chur": "CHU_2023_DRY.csv",
    "Davos": "DAV_2023_DRY.csv",
    "Disentis": "DIS_2023_DRY.csv",
    "Engelberg": "ENG_2023_DRY.csv",
    "Genève-Cointrin": "GVE_2023_DRY.csv",
    "Glarus": "GLA_2023_DRY.csv",
    "Grand-St-Bernard": "SBO_2023_DRY.csv",
    "Güttingen": "GUT_2023_DRY.csv",
    "Interlaken": "INT_2023_DRY.csv",
    "La Chaux-de-Fonds": "CDF_2023_DRY.csv",
    "La Frétaz": "FRE_2023_DRY.csv",
    "Locarno-Monti": "OTL_2023_DRY.csv",
    "Lugano": "LUG_2023_DRY.csv",
    "Luzern": "LUZ_2023_DRY.csv",
    "Magadino": "MAG_2023_DRY.csv",
    "Montana": "MVE_2023_DRY.csv",
    "Neuchâtel": "NEU_2023_DRY.csv",
    "Payerne": "PAY_2023_DRY.csv",
    "Piotta": "PIO_2023_DRY.csv",
    "Pully": "PLF_2023_DRY.csv",
    "Robbia": "ROB_2023_DRY.csv",
    "Rünenberg": "RUE_2023_DRY.csv",
    "Samedan": "SAM_2023_DRY.csv",
    "San Bernardino": "SBE_2023_DRY.csv",
    "St. Gallen": "STG_2023_DRY.csv",
    "Schaffhausen": "SHA_2023_DRY.csv",
    "Scuol": "SCU_2023_DRY.csv",
    "Sion": "SIO_2023_DRY.csv",
    "Ulrichen": "ULR_2023_DRY.csv",
    "Vaduz": "VAD_2023_DRY.csv",
    "Wynau": "WYN_2023_DRY.csv",
    "Zermatt": "ZER_2023_DRY.csv",
    "Zürich-Kloten": "KLO_2023_DRY.csv",
    "Zürich-MeteoSchweiz": "ZUESTA_2023_DRY.csv"
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
GEAK_Klassen = {
    "A": 25, 
    "B": 50, 
    "C": 75, 
    "D": 100, 
    "E": 125, 
    "F": 150,
    "G": 175
}
reduktionen = {
                "Dämmung Dach": 0.15,
                "neue Fenster": 0.15,
                "Dämmung Fassade": 0.25,
                "Dämmmung Kellerdecke": 0.1
            }

EV_MORGEN = "Morgens (05:00–08:00 Uhr)"
EV_PV = "PV-Überschussgeführt (11:00–15:00 Uhr)"
EV_ABEND = "Abends (17:00–22:00 Uhr)"
EV_KOMBI = "Kombiniert (05:00–08:00 Uhr und 17:00–22:00 Uhr)"

WW_PV = "PV-Überschussgeführt (spätestens 11:00 Uhr)"
WW_MORGEN = "Morgens (05:00–07:00 Uhr)"
WW_ABEND = "Abends (17:00–20:00 Uhr)"
WW_KOMBI = "Morgens + Abends (05:00–07:00 Uhr und 17:00–20:00 Uhr)"
WW_NACHMITTAG_LWWP = "Nachmittags für Luft/Wasser-WP (14:00–17:00 Uhr)"

#Standartlastprofile
slp_df = pd.read_excel("Standartprofil H25.xlsx")
slp_df.columns = slp_df.columns.str.strip()
slp_df["Monat"] = slp_df["Monat"].astype(int)
slp_df["Zeit"] = pd.to_datetime(slp_df["Zeit"], format="%H:%M:%S").dt.strftime("%H:%M")

g25_df = pd.read_excel("Standartprofil G25.xlsx")
g25_df.columns = g25_df.columns.str.strip()
g25_df["Monat"] = g25_df["Monat"].astype(int)
g25_df["Zeit"] = pd.to_datetime(
    g25_df["Zeit"], format="%H:%M:%S"
).dt.strftime("%H:%M")

#def Zeitdimension mit Dataframe
def create_base_dataframe(year=2025):
    zeitindex = pd.date_range(
        start=f"{year}-01-01 00:00",
        end=f"{year}-12-31 23:45",
        freq="15min",
        tz="Europe/Zurich"
    )
    df = pd.DataFrame(index=zeitindex)
    df["Monat"] = df.index.month
    df["Stunde"] = df.index.hour
    df["Tag_im_Jahr"] = df.index.dayofyear
    return df
def get_day_type(timestamp):
    if timestamp.weekday() < 5:
        return "WT" #Werktag
    elif timestamp.weekday() == 5:
        return "SA" #Saturday
    else:
        return "FT" #Feiertag bzw sonntag
def add_slp_profile(df, slp_df, jahresstromverbrauch):
    df = df.copy()

    # Tagtyp WT, SA FT bestimmen
    df["Tagtyp"] = df.index.map(get_day_type)

    #Uhrzeit entnehmen
    df["Zeit"] = df.index.strftime("%H:%M")

    # Excel vorbereiten
    slp_lookup = slp_df.copy()
    slp_lookup["Monat"] = slp_lookup["Monat"].astype(int)
    slp_lookup["Zeit"] = slp_lookup["Zeit"].astype(str).str[:5]
    slp_lookup = slp_lookup.set_index(["Monat", "Zeit"]) #Multiindex

    # Werte holen
    df["SA"] = [slp_lookup.loc[(m, z), "SA"] for m, z in zip(df["Monat"], df["Zeit"])]
    df["FT"] = [slp_lookup.loc[(m, z), "FT"] for m, z in zip(df["Monat"], df["Zeit"])]
    df["WT"] = [slp_lookup.loc[(m, z), "WT"] for m, z in zip(df["Monat"], df["Zeit"])]
        
    # richtigen Typtag wählen
    df["slp_wert"] = np.where(
        df["Tagtyp"] == "WT", df["WT"],
        np.where(df["Tagtyp"] == "SA", df["SA"], df["FT"])
    )

    t = df["Tag_im_Jahr"].astype("float64") #Tagesnummern 1-365
    dynamikfaktor = (
        - 3.92e-10 * t**4
        + 3.20e-7 * t**3
        - 7.02e-5 * t**2
        + 2.10e-3 * t
        + 1.24
    )
    df["slp_dyn"] = df["slp_wert"] * dynamikfaktor
    df["slp_dyn"] = df["slp_dyn"].clip(lower=0)

    # auf Jahresverbrauch normieren
    faktor_summe = df["slp_dyn"].sum() #normierung auf Jahresverbrauch
    df["hauslast_kWh"] = df["slp_dyn"] / faktor_summe * jahresstromverbrauch

    return df
def add_heating_profile_weather_based(df, df_weather, heizwaermebedarf_jahr, raumtemperatur=20, stationshoehe_m=None,standorthoehe_m=None, auslegetemperatur=-7, vorlauf_auslegung=40):
    df = df.copy()

    weather = df_weather[["temp"]].copy()
    weather["temp"] = pd.to_numeric(weather["temp"], errors="coerce")

    weather_15min = weather.resample("15min").ffill()

    df = df.join(weather_15min, how="left")
    df["temp"] = df["temp"].interpolate("time")

    if stationshoehe_m is not None and standorthoehe_m is not None:
        hoehenunterschied_m = standorthoehe_m - stationshoehe_m

        if abs(hoehenunterschied_m) >= 100:
            temperaturkorrektur = -0.65 * (hoehenunterschied_m / 100)
            df["temp"] = df["temp"] + temperaturkorrektur

    df["vorlauftemperatur_C"] = berechne_vorlauftemperatur(
        df["temp"],
        auslegetemperatur=auslegetemperatur,
        vorlauf_auslegung=vorlauf_auslegung,
        raumtemperatur=raumtemperatur
    )

    # Heizbedarf nur, wenn Aussentemperatur unter gewünschter Raumtemperatur liegt
    df["heiz_faktor"] = (raumtemperatur - df["temp"]).clip(lower=0)

    #Normierung
    faktor_summe = df["heiz_faktor"].sum()
    if faktor_summe > 0:
        df["heizwaerme_kWh"] = (
            df["heiz_faktor"] / faktor_summe * heizwaermebedarf_jahr
        )
    else:
        df["heizwaerme_kWh"] = 0.0

    return df
def berechne_vorlauftemperatur(temp_aussen, auslegetemperatur=-7, vorlauf_auslegung=40, raumtemperatur=20):
    steigung = (vorlauf_auslegung - raumtemperatur) / (auslegetemperatur - raumtemperatur)

    vorlauf = raumtemperatur + steigung * (temp_aussen - raumtemperatur)

    return vorlauf.clip(
        lower=raumtemperatur,
        upper=vorlauf_auslegung
    )
def add_heatpump_consumption(df, heizsystem, jaz=None, wp_typ=None, wp_strom_jahr=None):
    df = df.copy()
    if heizsystem == "Wärmepumpe" and wp_strom_jahr is not None:
        faktor_summe = df["heizwaerme_kWh"].sum()

        if faktor_summe > 0:
            df["wp_strom_kWh"] = df["heizwaerme_kWh"] / faktor_summe * wp_strom_jahr
        else:
            df["wp_strom_kWh"] = 0.0
    elif heizsystem == "Wärmepumpe" and jaz is not None and jaz > 0:
        df["wp_strom_kWh"] = df["heizwaerme_kWh"] / jaz
    else:
        df["wp_strom_kWh"] = 0.0
    df["gesamtlast_kWh"] = df["hauslast_kWh"] + df["wp_strom_kWh"]

    return df
def simulate_battery(
    df,
    batteriekapazitaet,
    max_ladeleistung,
    max_entladeleistung,
    min_soc_prozent,
    max_soc_prozent,
    einspeisegrenze_kw,
    bezugsgrenze_kw,
    wirkungsgrad_roundtrip = 0.95
):
    delta_t = 0.25  # 15 Minuten

    # Rechnerische Aufteilung des Round-Trip-Wirkungsgrads
    eta_lade = np.sqrt(wirkungsgrad_roundtrip)
    eta_entlade = np.sqrt(wirkungsgrad_roundtrip)

    # Umrechnung der kW-Grenzen in kWh-Grenzen für dieses Intervall
    max_ladung_kWh = max_ladeleistung * delta_t
    max_entladung_kWh = max_entladeleistung * delta_t
    einspeisegrenze_kWh = einspeisegrenze_kw * delta_t
    bezugsgrenze_kWh = bezugsgrenze_kw * delta_t
    df = df.copy()

    # neue Spalten vorbereiten
    df["direktverbrauch_pv_kWh"] = 0.0
    df["batterie_ladung_kWh"] = 0.0
    df["batterie_entladung_kWh"] = 0.0
    df["soc_kWh"] = 0.0
    df["netzbezug_kWh"] = 0.0
    df["netzeinspeisung_kWh"] = 0.0
    df["abregelung_kWh"] = 0.0
    df["unterdeckung_kWh"] = 0.0

    soc_min = batteriekapazitaet * (min_soc_prozent / 100)
    soc_max = batteriekapazitaet * (max_soc_prozent / 100)

    # Startwert Batterie: Mitte zwischen min und max
    soc = (soc_min + soc_max) / 2

    for i in df.index:
        last = df.at[i, "gesamtlast_kWh"]
        pv = df.at[i, "pv_kWh"]

        # 1) direkter PV-Verbrauch
        direktverbrauch = min(pv, last) #Pv zuerst im Haus verbraucht
        pv_ueberschuss = pv - direktverbrauch # Es kann nie mehr direkt verbraucht werden als PV vorhanden ist oder als Last vorhanden ist.
        restlast = last - direktverbrauch

        # 2) Batterie laden bei PV-Überschuss
        freie_kapazitaet = (soc_max - soc) /eta_lade
        batterie_ladung = min(pv_ueberschuss, max_ladung_kWh, freie_kapazitaet)
        #Die Batterie kann nur so viel laden, wie: PV-Überschuss vorhanden ist, die maximale Ladeleistung erlaubt, und noch Platz in der Batterie ist.
        soc += batterie_ladung * eta_lade
        rest_pv_nach_batterie = pv_ueberschuss - batterie_ladung
        #Batteriestand soc erhöht
        
        # 3) Einspeisen bis Grenze, Rest abregeln
        netzeinspeisung = min(rest_pv_nach_batterie, einspeisegrenze_kWh)
        abregelung = max(0.0, rest_pv_nach_batterie - netzeinspeisung)

        # 4) Batterie entladen bei Restlast
        verfuegbar_batterie_effektiv = (soc - soc_min) * eta_entlade
        batterie_entladung = min(restlast, max_entladung_kWh, verfuegbar_batterie_effektiv)
        soc -= batterie_entladung /eta_entlade

        restlast_nach_batterie = restlast - batterie_entladung

        # 5) Netzbezug bis Grenze, Rest = Unterdeckung
        netzbezug = min(restlast_nach_batterie, bezugsgrenze_kWh)
        unterdeckung = max(0.0, restlast_nach_batterie - netzbezug)

        # speichern
        df.at[i, "direktverbrauch_pv_kWh"] = direktverbrauch
        df.at[i, "batterie_ladung_kWh"] = batterie_ladung
        df.at[i, "batterie_entladung_kWh"] = batterie_entladung
        df.at[i, "soc_kWh"] = soc
        df.at[i, "netzbezug_kWh"] = netzbezug
        df.at[i, "netzeinspeisung_kWh"] = netzeinspeisung
        df.at[i, "abregelung_kWh"] = abregelung
        df.at[i, "unterdeckung_kWh"] = unterdeckung

    return df
def create_energy_summary(df):
    df = df.copy()

    # Eigenverbrauch aus PV:
    # PV-Produktion minus Einspeisung minus Abregelung
    df["eigenverbrauch_kWh"] = df["pv_kWh"] - df["netzeinspeisung_kWh"] - df["abregelung_kWh"]

    # keine negativen Rundungsreste
    df["eigenverbrauch_kWh"] = df["eigenverbrauch_kWh"].clip(lower=0)

    # Monatsbilanz
    monatsbilanz = df.groupby("Monat")[[ #groupierung nach Monat
        "pv_kWh",
        "eigenverbrauch_kWh",
        "netzeinspeisung_kWh",
        "netzbezug_kWh"
    ]].sum()

    monatsbilanz = monatsbilanz.rename(columns={ # neubennennung der Spalten
        "pv_kWh": "Produktion_kWh",
        "eigenverbrauch_kWh": "Eigenverbrauch_kWh",
        "netzeinspeisung_kWh": "Einspeisung_kWh",
        "netzbezug_kWh": "Bezug_kWh"
    })

    # Jahreskennzahlen
    gesamtlast = df["gesamtlast_kWh"].sum()
    pv_produktion = df["pv_kWh"].sum()
    eigenverbrauch = df["eigenverbrauch_kWh"].sum()
    netzbezug = df["netzbezug_kWh"].sum()
    abregelung = df["abregelung_kWh"].sum()
    unterdeckung = df["unterdeckung_kWh"].sum()

    if gesamtlast > 0:
        autarkiegrad = (1 - netzbezug / gesamtlast) * 100
    else:
        autarkiegrad = 0.0

    if pv_produktion > 0:
        eigenverbrauchsquote = (eigenverbrauch / pv_produktion) * 100
    else:
        eigenverbrauchsquote = 0.0

    jahreskennzahlen = {
        "Autarkiegrad_%": autarkiegrad,
        "Eigenverbrauchsquote_%": eigenverbrauchsquote,
        "Abgeregelte_Energie_kWh": abregelung,
        "Unterdeckung_kWh": unterdeckung,
        "PV_Produktion_kWh": pv_produktion,
        "Eigenverbrauch_kWh": eigenverbrauch,
        "Netzbezug_kWh": netzbezug,
        "Netzeinspeisung_kWh": df["netzeinspeisung_kWh"].sum()
    }

    return df, monatsbilanz, jahreskennzahlen
#hier lernen
def get_display_dataframe(df, zeitraum, start_datum=None, start_monat=None):
    df = df.copy()

    energie_spalten = [
        "gesamtlast_kWh",
        "pv_kWh",
        "ww_kWh",
        "ev_kWh",
        "netzbezug_kWh",
        "netzeinspeisung_kWh",
        "abregelung_kWh",
        "unterdeckung_kWh"
    ]

    for col in energie_spalten:
        if col in df.columns:
            neue_spalte = col.replace("_kWh", "_kW")
            df[neue_spalte] = df[col] / 0.25

    spalten = [
        "gesamtlast_kWh",
        "pv_kWh",
        "ww_kWh",
        "ev_kWh",
        "soc_kWh",
        "soc_prozent",
        "netzbezug_kWh",
        "netzeinspeisung_kWh",
        "abregelung_kWh",
        "unterdeckung_kWh",
        "gesamtlast_kW",
        "pv_kW",
        "ww_kW",
        "ev_kW",
        "netzbezug_kW",
        "netzeinspeisung_kW",
        "abregelung_kW",
        "unterdeckung_kW",
        "temp",
        "poa_global",
    ]

    spalten = [s for s in spalten if s in df.columns]

    if zeitraum == "Tag":
        if start_datum is None:
            start_datum = df.index.min().date()

        start = pd.Timestamp(start_datum)
        if df.index.tz is not None:
            start = start.tz_localize(df.index.tz)
        ende = start + pd.Timedelta(days=1)

        df_anzeige = df[(df.index >= start) & (df.index < ende)][spalten]

        # Durchschnitt pro Stunde
        df_anzeige = df_anzeige.resample("h").mean()

    elif zeitraum == "Woche":
        if start_datum is None:
            start_datum = df.index.min().date()

        start = pd.Timestamp(start_datum)
        if df.index.tz is not None:
            start = start.tz_localize(df.index.tz)
        ende = start + pd.Timedelta(days=7)

        df_anzeige = df[(df.index >= start) & (df.index < ende)][spalten]

        # Durchschnitt pro Tag
        df_anzeige = df_anzeige.resample("D").mean()

    elif zeitraum == "Monat":
        if start_monat is None:
            start_monat = 1

        df_anzeige = df[df.index.month == start_monat][spalten]

        # Durchschnitt pro Tag
        df_anzeige = df_anzeige.resample("D").mean()

    elif zeitraum == "Jahr":
        energie_cols = [
            "gesamtlast_kWh",
            "pv_kWh",
            "ww_kWh",
            "ev_kWh",
            "netzbezug_kWh",
            "netzeinspeisung_kWh",
            "abregelung_kWh",
            "unterdeckung_kWh"
        ]

        energie_cols = [c for c in energie_cols if c in df.columns]

        df_anzeige = df[energie_cols].resample("MS").sum()

        # Monatsenergie in durchschnittliche Monatsleistung umrechnen
        stunden_pro_monat = df_anzeige.index.days_in_month * 24

        for col in energie_cols:
            neue_spalte = col.replace("_kWh", "_kW")
            df_anzeige[neue_spalte] = df_anzeige[col] / stunden_pro_monat

        if "soc_kWh" in df.columns:
            df_anzeige["soc_kWh"] = df["soc_kWh"].resample("MS").mean()
        if "soc_prozent" in df.columns:
            df_anzeige["soc_prozent"] = df["soc_prozent"].resample("MS").mean()
        if "temp" in df.columns:
            df_anzeige["temp"] = df["temp"].resample("MS").mean()

        if "poa_global" in df.columns:
            df_anzeige["poa_global"] = df["poa_global"].resample("MS").mean()
    else:
        df_anzeige = df[spalten]

    return df_anzeige
def schoene_achse_mit_ticks(max_wert, anzahl_intervalle=5):
    if pd.isna(max_wert) or max_wert <= 0:
        max_wert = 1

    zielwert = max_wert * 1.10

    moegliche_tickschritte = [
        0.1, 0.2, 0.5,
        1, 2, 2.5, 5,
        10, 20, 25, 50,
        100, 200, 250, 500,
        1000
    ]

    for schritt in moegliche_tickschritte:
        achse_max = schritt * anzahl_intervalle

        if achse_max >= zielwert:
            ticks = np.linspace(0, achse_max, anzahl_intervalle + 1)
            return achse_max, ticks

    schritt = np.ceil(zielwert / anzahl_intervalle)
    achse_max = schritt * anzahl_intervalle
    ticks = np.linspace(0, achse_max, anzahl_intervalle + 1)

    return achse_max, ticks
def schoene_achsenobergrenze_wetter(max_wert, schrittweite):
    if pd.isna(max_wert) or max_wert <= 0:
        return schrittweite

    return np.ceil(max_wert / schrittweite) * schrittweite
def schoene_leistungsachse(max_wert, anzahl_intervalle=5):
    if pd.isna(max_wert) or max_wert <= 0:
        max_wert = 1

    zielwert = max_wert * 1.1

    moegliche_maxima = [
        0.5, 1, 1.5, 2, 2.5, 3, 4, 5,
        7.5, 10, 12.5, 15, 20, 25, 30,
        40, 50, 75, 100, 150, 200
    ]

    for achse_max in moegliche_maxima:
        if achse_max >= zielwert:
            ticks = np.linspace(0, achse_max, anzahl_intervalle + 1)
            return achse_max, ticks

    achse_max = np.ceil(zielwert / anzahl_intervalle) * anzahl_intervalle
    ticks = np.linspace(0, achse_max, anzahl_intervalle + 1)

    return achse_max, ticks
def create_main_plot(df_plot, einspeisegrenze_kw, bezugsgrenze_kw, zeitraum):
    fig = go.Figure()

    # PV-Produktion
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["pv_kW"],
        mode="lines",
        name="PV-Produktion",
        line=dict(color="gold", width=5, dash="solid")
    ))

    # Gesamtlast
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["gesamtlast_kW"],
        mode="lines",
        name="Hausverbrauch / Gesamtlast",
        line=dict(color="blue", width=2.5, dash="dash")
    ))

    # Warmwasser
    if "ww_kW" in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_plot.index,
            y=df_plot["ww_kW"],
            mode="lines",
            name="Warmwasser",
            line=dict(color="red", width=2.5, dash="dot")
        ))

    # E-Auto
    if "ev_kW" in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_plot.index,
            y=df_plot["ev_kW"],
            mode="lines",
            name="E-Auto",
            line=dict(color="green", width=2.5, dash="dashdot")
        ))

    # Netzbezug
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["netzbezug_kW"],
        mode="lines",
        name="Netzbezug",
        line=dict(color="orange", width=5, dash="dot")
    ))

    # Netzeinspeisung
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["netzeinspeisung_kW"],
        mode="lines",
        name="Netzeinspeisung",
        line=dict(color="purple", width=2.5, dash="longdashdot")
    ))

    # Batterieladezustand / SoC
    if "soc_prozent" in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_plot.index,
            y=df_plot["soc_prozent"],
            mode="lines",
            name="Batterie-SoC in %",
            line=dict(color="black", width=3),
            yaxis="y2"
        ))

    # Einspeisegrenze
    # fig.add_trace(go.Scatter(
    #     x=df_plot.index,
    #     y=[einspeisegrenze_kw] * len(df_plot),
    #     mode="lines",
    #     name="Einspeisegrenze",
    #     line=dict(color="red", width=1.5, dash="dash")
    # ))

    # Bezugsgrenze
    # fig.add_trace(go.Scatter(
    #     x=df_plot.index,
    #     y=[bezugsgrenze_kw] * len(df_plot),
    #     mode="lines",
    #     name="Bezugsgrenze",
    #     line=dict(color="red", width=1.5, dash="dot")
    # ))

    # Abregelung rot markieren
    df_abregelung = df_plot[df_plot["abregelung_kW"] > 0]

    if not df_abregelung.empty:
        fig.add_trace(go.Scatter(
            x=df_abregelung.index,
            y=df_abregelung["netzeinspeisung_kW"] + df_abregelung["abregelung_kW"],
            mode="markers",
            name="Abregelung",
            marker=dict(
                color="red",
                size=14,
                symbol="x",
                line=dict(color="darkred", width=2)
            ),
            customdata=df_abregelung["abregelung_kWh"],
            hovertemplate=
                "<b>Abregelung</b><br>" +
                "Zeit: %{x}<br>" +
                "Abgeregelte Energie: %{customdata:.3f} kWh<br>" +
                "<extra></extra>"
        ))

    # Unterdeckung rot markieren
    df_unterdeckung = df_plot[df_plot["unterdeckung_kW"] > 0]
    if not df_unterdeckung.empty:
        fig.add_trace(go.Scatter(
            x=df_unterdeckung.index,
            y=df_unterdeckung["gesamtlast_kW"],
            mode="markers",
            name="Unterdeckung",
            marker=dict(color="darkred", size=8, symbol="circle-open")
        ))
    leistungs_spalten = [
        "pv_kW",
        "gesamtlast_kW",
        "ww_kW",
        "ev_kW",
        "netzbezug_kW",
        "netzeinspeisung_kW",
        "abregelung_kW",
        "unterdeckung_kW"
    ]

    max_y_roh = 0

    for spalte in leistungs_spalten:
        if spalte in df_plot.columns:
            spalten_max = df_plot[spalte].max()

            if not pd.isna(spalten_max):
                max_y_roh = max(max_y_roh, spalten_max)

    # Abregelungsmarker liegt sichtbar bei Netzeinspeisung + Abregelung.
    # Deshalb wird nur dieser sichtbare Marker zusätzlich berücksichtigt.
    if "netzeinspeisung_kW" in df_plot.columns and "abregelung_kW" in df_plot.columns:
        marker_max = (
            df_plot["netzeinspeisung_kW"] + df_plot["abregelung_kW"]
        ).max()

        if not pd.isna(marker_max):
            max_y_roh = max(max_y_roh, marker_max)

    max_y, linke_tickwerte = schoene_leistungsachse(max_y_roh)

    rechte_tickwerte = [0, 20, 40, 60, 80, 100]

    fig.update_layout(
        title="Zeitverlauf von PV, Last, Batterie und Netz",
        xaxis_title="Zeit",
        yaxis=dict(
            title="Leistung in kW",
            showgrid=True,
            gridcolor="rgba(200,200,200,0.35)",
            range=[0, max_y],
            tickmode="array",
            tickvals=linke_tickwerte,
            tickformat="~g",
            zeroline=False
        ),
        yaxis2=dict(
            title="Batterie-SoC in %",
            overlaying="y",
            side="right",
            range=[0, 100],
            tickmode="array",
            tickvals=rechte_tickwerte,
            showgrid=False,
            zeroline=False
        ),
        legend=dict(orientation="h", y=-0.25),
        height=600,
        margin=dict(l=40, r=40, t=60, b=100)
    )
    return fig
def create_weather_plot(df_plot):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["temp"],
        mode="lines",
        name="Außentemperatur in °C",
        line=dict(color="blue", width=3, dash="longdashdot")
    ))

    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["poa_global"],
        mode="lines",
        name="Sonneneinstrahlung in W/m²",
        line=dict(color="orange", width=3, dash="dot"),
        yaxis="y2"
    ))

    max_einstrahlung = df_plot["poa_global"].max()

    if pd.isna(max_einstrahlung) or max_einstrahlung <= 0:
        max_einstrahlung = 1

    # Maximum × 1.1 und dann schön aufrunden
    einstrahlung_achse_max = schoene_achsenobergrenze_wetter(
        max_einstrahlung * 1.1,
        100
    )

    temp_min = df_plot["temp"].min()
    temp_max = df_plot["temp"].max()

    if pd.isna(temp_min) or pd.isna(temp_max):
        temp_min = 0
        temp_max = 1

    # Temperaturachse unten/oben dynamisch, aber schön gerundet
    if temp_min < 0:
        temp_achse_min = np.floor((temp_min * 1.1) / 5) * 5
    else:
        temp_achse_min = np.floor((temp_min * 0.9) / 5) * 5

    if temp_max > 0:
        temp_achse_max = np.ceil((temp_max * 1.1) / 5) * 5
    else:
        temp_achse_max = np.ceil((temp_max * 0.9) / 5) * 5

    # Falls der Bereich zu klein oder komisch ist
    if temp_achse_max <= temp_achse_min:
        temp_achse_min = np.floor((temp_min - 1) / 5) * 5
        temp_achse_max = np.ceil((temp_max + 1) / 5) * 5

    # Beide Achsen bekommen gleich viele Tickwerte
    temp_tickwerte = np.linspace(temp_achse_min, temp_achse_max, 6)
    einstrahlung_tickwerte = np.linspace(0, einstrahlung_achse_max, 6)

    fig.update_layout(
        title="Temperatur und Sonneneinstrahlung",
        xaxis_title="Zeit",
        yaxis=dict(
            title="Temperatur in °C",
            showgrid=True,
            gridcolor="rgba(200,200,200,0.35)",
            range=[temp_achse_min, temp_achse_max],
            tickmode="array",
            tickvals=temp_tickwerte,
            tickformat=".1f",
            zeroline=False
        ),
        yaxis2=dict(
            title="Sonneneinstrahlung in W/m²",
            overlaying="y",
            side="right",
            range=[0, einstrahlung_achse_max],
            tickmode="array",
            tickvals=einstrahlung_tickwerte,
            tickformat=".0f",
            showgrid=False,
            zeroline=False
        ),
        legend=dict(orientation="h", y=-0.25),
        height=500,
        margin=dict(l=40, r=40, t=60, b=100)
    )

    return fig
#Pv ertragsrechnung:
def get_station_abbr(standort_name):
    dateiname = standort_dateien[standort_name]
    return dateiname.split("_")[0]
def load_weather_data(standort_name):
    dateiname = standort_dateien[standort_name]
    dateipfad = f"{basis_pfad_weather}/{dateiname}"

    df_weather = pd.read_csv(dateipfad)

    # SIA/Meteodaten haben oft Stunden 1–24.
    # Für Python-Zeitstempel brauchen wir 0–23.
    df_weather["timestamp"] = pd.to_datetime(
        dict(
            year=df_weather["time.yy"],
            month=df_weather["time.mm"],
            day=df_weather["time.dd"],
            hour=df_weather["time.hh"] - 1
        )
    )

    df_weather = df_weather.set_index("timestamp")

    return df_weather
def prepare_weather_for_simulation(df_weather, target_year):
    df = df_weather.copy().reset_index(drop=True) #copy vom original wetterindex und ignoriert dass die Wetterdaten aus verschiedenen Jahren sind
    new_index = pd.date_range(
        start=f"{target_year}-01-01 00:00",
        periods=len(df),
        freq="1h",
        tz="Europe/Zurich"
    )
    df.index = new_index
    return df
def load_station_metadata(metadata_path="SIA4028_metadata_2023.csv"):
    df_meta = pd.read_csv(metadata_path, sep=";") #neue Spalte in der Tabelle bei ; 
    df_meta.columns = df_meta.columns.str.strip() # alle Leerzeichen in Spaltennamen sind weggelöscht 
    return df_meta
def get_station_info(meta_df, standort_name, standort_dateien):
    abbr = get_station_abbr(standort_name)
    row = meta_df.loc[meta_df["Abbr."].astype(str).str.strip() == abbr]#man sucht nach dem Stationskürzel, ob es überhaupt des gibt was eingegeben ist
    if row.empty:
        raise ValueError(f"Keine Metadaten für {standort_name} / {abbr} gefunden.")
    row = row.iloc[0]
    return {
        "abbr": abbr,
        "latitude": float(row["Latitude"]),
        "longitude": float(row["Longitude"]),
        "altitude": float(row["Station Height"])
    }
def add_pv_profile_weather_based(
    df_base,
    df_weather,
    latitude,
    longitude,
    altitude,
    dachneigung,
    dachausrichtung,
    pv_peakleistung_kwp,
    wirkungsgrad_prozent,
    performance_ratio=0.85, # vlt sind diese Werte im Datenblatt von einer Pv anlage --> umändern input möglichkeit
    gamma_pdc=-0.004, #default falls es keine andere eingabe gibt
    noct=45
):
    #schon vorhin auf 15min bestimmt
    df = df_base.copy() 

    cols = ["temp", "windmean", "rad.global", "rad.direct", "rad.diffus", "albedo"]
    
    weather = df_weather[cols].copy()

    # alles numerisch machen
    for col in cols:
        weather[col] = pd.to_numeric(weather[col], errors="coerce")

    # Wetterdaten stündlich auf 15 min interpolieren
    weather_15min = weather.resample("15min").interpolate("time") 
    # wenn 12uhr 400 ist und 13 uhr 600 dann erstellt er 12:15, 12:30 und 12:45 zu 450, 500 und 550
    # falls ich hier obendran auf 30 min will dann müsste ich hier 30 min schreiben und oben wo die databasis frame gebautr wird auch 30 min bei freq machen & energieumrechnung anpassen
    df = df.join(weather_15min, how="left")

    df["temp"] = df["temp"].interpolate("time")
    df["windmean"] = df["windmean"].interpolate("time")

    df["rad.global"] = df["rad.global"].clip(lower=0).fillna(0) #negativ werte auf null und fehlende werte zu 0
    df["rad.direct"] = df["rad.direct"].clip(lower=0).fillna(0)
    df["rad.diffus"] = df["rad.diffus"].clip(lower=0).fillna(0)

    df["albedo_use"] = df["albedo"] / 100.0

    location = pvlib.location.Location(
        latitude=latitude,
        longitude=longitude,
        tz="Europe/Zurich", #zeitzone
        altitude=altitude
    )

    solar_position = location.get_solarposition(df.index) #eine pvlib-Methode. Laut pvlib verwendet sie intern pvlib.solarposition.get_solarposition(), um Solarzenit, Solarazimut usw. zu berechnen

    surface_azimuth = dachausrichtung

    dni_extra = pvlib.irradiance.get_extra_radiation(df.index) #Das ist kein Messdatensatz deiner Station, sondern ein berechneter astronomischer Wert für die extraterrestrische Strahlung, also die Sonnenstrahlung außerhalb der Atmosphäre. pvlib berechnet ihn aus Datum bzw. Tageszahl mit hinterlegten Formeln/Methoden wie standardmäßig spencer.

    poa = pvlib.irradiance.get_total_irradiance(
        surface_tilt=dachneigung,
        surface_azimuth=surface_azimuth, #modulausrichtung
        solar_zenith=solar_position["apparent_zenith"], #sonnenstand
        solar_azimuth=solar_position["azimuth"], #sonnenstand
        dni=df["rad.direct"], #Direktstrahlung
        ghi=df["rad.global"], #Globalstrahlung horizontal
        dhi=df["rad.diffus"], #Diffusstrahlung horizontal
        dni_extra=dni_extra, #extraterestrische Einstrahlung
        albedo=df["albedo_use"], #bodenreflexion
        model="haydavies" #anisotropes Diffusmodell von pvlib
    )# hier genau verstehen
    # mit get_total_irradiance() wird aus den horizontal gemessenen Wetterdaten die wirksame Einstrahlung auf die geneigte und ausgerichtete PV-Fläche berechnet
    
    df["poa_global"] = poa["poa_global"].clip(lower=0) #plane of array irradiance, Negative Werte werden auf 0 gesetzt

    # Zelltemperatur
    df["temp_cell"] = df["temp"] + (df["poa_global"] / 800.0) * (noct - 20)# quelle formel 20°C = Referenzbedingungen/Umgebungstemp

    temp_factor = 1 + gamma_pdc * (df["temp_cell"] - 25) #formel quelle , hier kommt ein wert in dez raus und in % sagt es quasi wie "nur noch 90% Leistung" wenn es so heiss ist
    df["temp_factor"] = temp_factor.clip(lower=0) #nicht unter null

    # Wirkungsgrad von % auf Dezimalzahl
    eta_modul = wirkungsgrad_prozent / 100.0

    # Modulfläche aus Peakleistung und Wirkungsgrad unter STC:
    # P_stc = A * eta * 1000 W/m²
    modulflaeche_m2 = pv_peakleistung_kwp / eta_modul

    df["modulflaeche_m2"] = modulflaeche_m2

    # Leistung
    df["pv_power_kW"] = (
        (df["poa_global"] / 1000.0)
        * modulflaeche_m2
        * eta_modul
        * df["temp_factor"]
        * performance_ratio
    ).clip(lower=0)#keine below 0 werte
    # mit SIA 2056 nohcmal genau vergleichen Seite 82

    # Energie pro 15 min
    df["pv_kWh"] = df["pv_power_kW"] * 0.25 #E[kWh] = P [kW] * t[h]

    return df

#Warmwasser:
# def add_hotwater_profile(df, ww_aktiv, ww_bedarf_kWh_tag, ww_ladeleistung_kw, ww_strategie):
    df = df.copy()
    df["ww_kWh"] = 0.0

    if not ww_aktiv or ww_bedarf_kWh_tag <= 0 or ww_ladeleistung_kw <= 0:
        return df

    delta_t = 0.25
    max_ww_kWh_pro_schritt = ww_ladeleistung_kw * delta_t
    tage = pd.to_datetime(df.index.date).unique()

    for tag in tage:
        verbleibend = ww_bedarf_kWh_tag

        def verteile_gleichmaessig(mask, ziel_kWh):
            nonlocal verbleibend
            idx = df.index[mask]
            if len(idx) == 0 or ziel_kWh <= 0 or verbleibend <= 0:
                return

            ziel_kWh = min(ziel_kWh, verbleibend)
            energie_pro_schritt = min(ziel_kWh / len(idx), max_ww_kWh_pro_schritt)
            noch_offen = ziel_kWh

            for ts in idx:
                ladung = min(energie_pro_schritt, noch_offen, max_ww_kWh_pro_schritt)
                df.at[ts, "ww_kWh"] += ladung
                noch_offen -= ladung
                verbleibend -= ladung

                if noch_offen <= 0 or verbleibend <= 0:
                    break

        def verteile_pv_optimiert(mask, ziel_kWh):
            nonlocal verbleibend
            idx = df.index[mask]
            if len(idx) == 0 or ziel_kWh <= 0 or verbleibend <= 0:
                return

            ziel_kWh = min(ziel_kWh, verbleibend)

            # nach höchster PV sortieren
            pv_sortiert = df.loc[idx, "pv_kWh"].sort_values(ascending=False)

            noch_offen = ziel_kWh
            for ts in pv_sortiert.index:
                ladung = min(max_ww_kWh_pro_schritt, noch_offen)
                df.at[ts, "ww_kWh"] += ladung
                noch_offen -= ladung
                verbleibend -= ladung

                if noch_offen <= 0 or verbleibend <= 0:
                    break

        mask_morgen = (
            (df.index.date == tag.date()) &
            (df.index.hour >= 5) &
            (df.index.hour < 7)
        )
        mask_mittag = (
            (df.index.date == tag.date()) &
            (df.index.hour >= 11) &
            (df.index.hour < 15)
        )
        mask_abend = (
            (df.index.date == tag.date()) &
            (df.index.hour >= 17) &
            (df.index.hour < 20)
        )

        if ww_strategie == "Morgens":
            verteile_gleichmaessig(mask_morgen, ww_bedarf_kWh_tag)

        elif ww_strategie == "Mittag / PV-optimiert":
            verteile_pv_optimiert(mask_mittag, ww_bedarf_kWh_tag)

        elif ww_strategie == "Abends":
            verteile_gleichmaessig(mask_abend, ww_bedarf_kWh_tag)

        elif ww_strategie == "Kombiniert (morgens + mittags)":
            verteile_gleichmaessig(mask_morgen, ww_bedarf_kWh_tag * 0.4)
            verteile_pv_optimiert(mask_mittag, ww_bedarf_kWh_tag * 0.6)

            if verbleibend > 0:
                verteile_pv_optimiert(mask_mittag, verbleibend)

    return df
# def add_ev_profile(df, ev_aktiv, ev_bedarf_kWh_tag, ev_ladeleistung_kw, ev_strategie):
    df = df.copy()
    df["ev_kWh"] = 0.0

    if not ev_aktiv or ev_bedarf_kWh_tag <= 0 or ev_ladeleistung_kw <= 0:
        return df

    delta_t = 0.25
    max_ev_kWh_pro_schritt = ev_ladeleistung_kw * delta_t
    tage = pd.to_datetime(df.index.date).unique()

    for tag in tage:
        verbleibend = ev_bedarf_kWh_tag

        def verteile_gleichmaessig(mask, ziel_kWh):
            nonlocal verbleibend
            idx = df.index[mask]
            if len(idx) == 0 or ziel_kWh <= 0 or verbleibend <= 0:
                return

            ziel_kWh = min(ziel_kWh, verbleibend)
            energie_pro_schritt = min(ziel_kWh / len(idx), max_ev_kWh_pro_schritt)
            noch_offen = ziel_kWh

            for ts in idx:
                ladung = min(energie_pro_schritt, noch_offen, max_ev_kWh_pro_schritt)
                df.at[ts, "ev_kWh"] += ladung
                noch_offen -= ladung
                verbleibend -= ladung

                if noch_offen <= 0 or verbleibend <= 0:
                    break

        def verteile_pv_optimiert(mask, ziel_kWh):
            nonlocal verbleibend
            idx = df.index[mask]
            if len(idx) == 0 or ziel_kWh <= 0 or verbleibend <= 0:
                return

            ziel_kWh = min(ziel_kWh, verbleibend)
            pv_sortiert = df.loc[idx, "pv_kWh"].sort_values(ascending=False)

            noch_offen = ziel_kWh
            for ts in pv_sortiert.index:
                ladung = min(max_ev_kWh_pro_schritt, noch_offen)
                df.at[ts, "ev_kWh"] += ladung
                noch_offen -= ladung
                verbleibend -= ladung

                if noch_offen <= 0 or verbleibend <= 0:
                    break

        mask_morgen = (
            (df.index.date == tag.date()) &
            (df.index.hour >= 5) &
            (df.index.hour < 8)
        )
        mask_mittag = (
            (df.index.date == tag.date()) &
            (df.index.hour >= 11) &
            (df.index.hour < 15)
        )
        mask_abend = (
            (df.index.date == tag.date()) &
            (df.index.hour >= 17) &
            (df.index.hour < 22)
        )

        if ev_strategie == "Morgens":
            verteile_gleichmaessig(mask_morgen, ev_bedarf_kWh_tag)

        elif ev_strategie == "Mittag / PV-optimiert":
            verteile_pv_optimiert(mask_mittag, ev_bedarf_kWh_tag)

        elif ev_strategie == "Abends":
            verteile_gleichmaessig(mask_abend, ev_bedarf_kWh_tag)

        elif ev_strategie == "Kombiniert (mittags + abends)":
            verteile_pv_optimiert(mask_mittag, ev_bedarf_kWh_tag * 0.6)
            verteile_gleichmaessig(mask_abend, ev_bedarf_kWh_tag * 0.4)

            if verbleibend > 0:
                verteile_gleichmaessig(mask_abend, verbleibend)

    return df
def ist_im_zeitfenster(timestamp, strategie, verbraucher):
    h = timestamp.hour

    if verbraucher == "Warmwasser":
        if strategie == WW_MORGEN:
            return 5 <= h < 7

        elif strategie == WW_NACHMITTAG_LWWP:
            return 14 <= h < 17

        elif strategie == WW_ABEND:
            return 17 <= h < 20

        elif strategie == WW_KOMBI:
            return (5 <= h < 7) or (17 <= h < 20)

        elif strategie == WW_PV:
            return 5 <= h < 15

    if verbraucher == "E-Auto":
        if strategie == EV_MORGEN:
            return 5 <= h < 8
        elif strategie == EV_PV:
            return 11 <= h < 15
        elif strategie == EV_ABEND:
            return 17 <= h < 22
        elif strategie == EV_KOMBI:
            return (5 <= h < 8) or (17 <= h < 22)

    return False
def get_ev_fahrbedarf(timestamp, ev_config):
    if not ev_config["aktiv"]:
        return 0.0

    if timestamp.weekday() in ev_config["fahrtage"]:
        return ev_config["km_pro_fahrtag"] * ev_config["verbrauch_pro_100km"] / 100

    return 0.0
def pruefe_ev_plausibilitaet(ev_config):
    if not ev_config["aktiv"]:
        return None

    ladefenster_stunden = {
        EV_MORGEN: 3,   # 05:00–08:00
        EV_PV: 4,       # 11:00–15:00
        EV_ABEND: 5,    # 17:00–22:00
        EV_KOMBI: 8     # 05:00–08:00 + 17:00–22:00
    }

    fahrbedarf_kWh = (
        ev_config["km_pro_fahrtag"]
        * ev_config["verbrauch_pro_100km"]
        / 100
    )

    max_ladung_kWh = (
        ev_config["leistung_kw"]
        * ladefenster_stunden[ev_config["strategie"]]
    )

    return {
        "fahrbedarf_kWh": fahrbedarf_kWh,
        "max_ladung_kWh": max_ladung_kWh,
        "ok": fahrbedarf_kWh <= max_ladung_kWh
    }
def simulate_ems(
    df,
    prioritaeten,
    ww_config,
    ev_config,
    batteriekapazitaet,
    max_ladeleistung,
    max_entladeleistung,
    min_soc_prozent,
    max_soc_prozent,
    einspeisegrenze_kw,
    bezugsgrenze_kw,
    batterie_wirkungsgrad
):
    df = df.copy()
    delta_t = 0.25

    df["ww_kWh"] = 0.0
    df["ev_kWh"] = 0.0
    df["direktverbrauch_pv_kWh"] = 0.0
    df["batterie_ladung_kWh"] = 0.0
    df["batterie_entladung_kWh"] = 0.0
    df["soc_kWh"] = 0.0
    df["netzbezug_kWh"] = 0.0
    df["netzeinspeisung_kWh"] = 0.0
    df["abregelung_kWh"] = 0.0
    df["unterdeckung_kWh"] = 0.0

    soc_min = batteriekapazitaet * min_soc_prozent / 100
    soc_max = batteriekapazitaet * max_soc_prozent / 100
    soc = (soc_min + soc_max) / 2

    current_day = None
    ww_rest = 0.0
    ev_rest = 0.0

    for i in df.index:
        if current_day != i.date():
            current_day = i.date()
            ww_rest = ww_config["bedarf_tag"] if ww_config["aktiv"] else 0.0
            ev_rest += (
                ev_config["km_nicht_fahrtag"]
                * ev_config["verbrauch_pro_100km"]
                / 100
            )
        # morgens entsteht einfach ein zusätzlicher Energiebedarf
        if i.hour == 17 and i.minute == 0:
            ev_rest += get_ev_fahrbedarf(i, ev_config)


        pv = df.at[i, "pv_kWh"]
        basislast = df.at[i, "gesamtlast_kWh"]

        direkt = min(pv, basislast)
        pv_rest = pv - direkt
        restlast = basislast - direkt

        for element in prioritaeten:

            if element == "Warmwasser" and ww_rest > 0 and ww_config["steuerbar"]:

                laden_erlaubt = ist_im_zeitfenster(
                    i,
                    ww_config["strategie"],
                    "Warmwasser"
                )

                max_step = ww_config["leistung_kw"] * delta_t

                if ww_config["strategie"] == WW_PV:
                    if pv_rest > 0:
                        ladung = min(max_step, ww_rest, pv_rest)
                    elif i.hour >= 11:
                        ladung = min(max_step, ww_rest)
                    else:
                        ladung = 0
                else:
                    ladung = min(max_step, ww_rest)

                if laden_erlaubt and ladung > 0:
                    df.at[i, "ww_kWh"] += ladung
                    ww_rest -= ladung

                    pv_anteil = min(pv_rest, ladung)
                    pv_rest -= pv_anteil
                    restlast += ladung - pv_anteil

            elif element == "E-Auto" and ev_rest > 0:
                if ist_im_zeitfenster(i, ev_config["strategie"], "E-Auto"):
                    max_step = ev_config["leistung_kw"] * delta_t

                    if ev_config["strategie"] == EV_PV:
                        ladung = min(max_step, ev_rest, pv_rest)
                    else:
                        ladung = min(max_step, ev_rest)

                    if ladung > 0:
                        df.at[i, "ev_kWh"] += ladung
                        ev_rest -= ladung

                        pv_anteil = min(pv_rest, ladung)
                        pv_rest -= pv_anteil
                        restlast += ladung - pv_anteil

            elif element == "Batterie" and batteriekapazitaet > 0:
                freie_kapazitaet = soc_max - soc
                max_ladung = max_ladeleistung * delta_t

                eta = batterie_wirkungsgrad / 100
                ladung = min(pv_rest, max_ladung, freie_kapazitaet / eta)
                soc += ladung * eta
                pv_rest -= ladung

                df.at[i, "batterie_ladung_kWh"] += ladung

            elif element == "Einspeisung":
                einspeisegrenze_kWh = einspeisegrenze_kw * delta_t
                einspeisung = min(pv_rest, einspeisegrenze_kWh)

                df.at[i, "netzeinspeisung_kWh"] += einspeisung
                pv_rest -= einspeisung

        # Nicht steuerbares Warmwasser: feste Abendladung, nicht über EMS priorisiert
        if ww_config["aktiv"] and not ww_config["steuerbar"] and ww_rest > 0:
            if ist_im_zeitfenster(i, "Abends", "Warmwasser"):
                max_step = ww_config["leistung_kw"] * delta_t
                ladung = min(max_step, ww_rest)

                df.at[i, "ww_kWh"] += ladung
                ww_rest -= ladung

                pv_anteil = min(pv_rest, ladung)
                pv_rest -= pv_anteil
                restlast += ladung - pv_anteil

        # Einspeisung ist immer Pflicht: Rest-PV wird bis zur Grenze eingespeist
        einspeisegrenze_kWh = einspeisegrenze_kw * delta_t
        einspeisung = min(pv_rest, einspeisegrenze_kWh)
        df.at[i, "netzeinspeisung_kWh"] += einspeisung
        pv_rest -= einspeisung

        df.at[i, "abregelung_kWh"] = max(0.0, pv_rest)

        if batteriekapazitaet > 0 and restlast > 0:
            verfuegbar = soc - soc_min
            max_entladung = max_entladeleistung * delta_t
            entladung = min(restlast, max_entladung, verfuegbar)

            soc -= entladung
            restlast -= entladung
            df.at[i, "batterie_entladung_kWh"] = entladung
        #Die Batterie wird entladen, wenn nach PV-Direktverbrauch und flexiblen Lasten noch Restlast übrig bleibt.

        bezugsgrenze_kWh = bezugsgrenze_kw * delta_t
        netzbezug = min(restlast, bezugsgrenze_kWh)
        unterdeckung = max(0.0, restlast - netzbezug)

        df.at[i, "direktverbrauch_pv_kWh"] = direkt
        df.at[i, "soc_kWh"] = soc
        df.at[i, "soc_prozent"] = soc / batteriekapazitaet * 100 if batteriekapazitaet > 0 else 0
        df.at[i, "netzbezug_kWh"] = netzbezug
        df.at[i, "unterdeckung_kWh"] = unterdeckung

    df["gesamtlast_kWh"] = df["gesamtlast_kWh"] + df["ww_kWh"] + df["ev_kWh"]

    return df
def add_uploaded_load_profile(df_base, uploaded_file, lastprofil_einheit):
    df = df_base.copy()

    if uploaded_file.name.endswith(".csv"):
        df_upload = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        excel_file = pd.ExcelFile(uploaded_file)

        if len(excel_file.sheet_names) != 1:
            st.error("Bitte lade eine Excel-Datei mit genau einem Tabellenblatt hoch.")
            st.stop()

        df_upload = pd.read_excel(uploaded_file, sheet_name=excel_file.sheet_names[0])

    df_upload.columns = df_upload.columns.str.strip()

    zeitspalte = df_upload.columns[0]
    verbrauchsspalte = df_upload.columns[-1]

    df_upload = df_upload[[zeitspalte, verbrauchsspalte]].copy()
    df_upload.columns = ["timestamp", "verbrauch_roh"]

    df_upload["timestamp"] = pd.to_datetime(df_upload["timestamp"], errors="coerce")
    df_upload["verbrauch_roh"] = pd.to_numeric(df_upload["verbrauch_roh"], errors="coerce")

    df_upload = df_upload.dropna(subset=["timestamp", "verbrauch_roh"])
    df_upload = df_upload.set_index("timestamp").sort_index()

    if lastprofil_einheit == "Energie pro 15-Minuten-Intervall in kWh":
        df_upload["verbrauch_kWh"] = df_upload["verbrauch_roh"]
    else:
        df_upload["verbrauch_kWh"] = df_upload["verbrauch_roh"] * 0.25

    df_upload = df_upload[["verbrauch_kWh"]]

    df_upload = df_upload.reset_index()
    df_upload["timestamp"] = df_upload["timestamp"].apply(
        lambda x: x.replace(year=df.index[0].year)
    )
    df_upload = df_upload.set_index("timestamp")
    if df_upload.index.tz is None and df.index.tz is not None:
        df_upload.index = df_upload.index.tz_localize(df.index.tz)

    df_upload = df_upload.resample("15min").sum()

    df = df.join(df_upload, how="left")
    df["hauslast_kWh"] = df["verbrauch_kWh"].fillna(0)

    return df
def get_raw_period_dataframe(df, zeitraum, start_datum=None, start_monat=None):
    tz = df.index.tz

    if zeitraum == "Tag":
        start = pd.Timestamp(start_datum)
        if tz is not None:
            start = start.tz_localize(tz)

        ende = start + pd.Timedelta(days=1)
        return df[(df.index >= start) & (df.index < ende)]

    elif zeitraum == "Woche":
        start = pd.Timestamp(start_datum)
        if tz is not None:
            start = start.tz_localize(tz)

        ende = start + pd.Timedelta(days=7)
        return df[(df.index >= start) & (df.index < ende)]

    elif zeitraum == "Monat":
        return df[df.index.month == start_monat]

    elif zeitraum == "Jahr":
        return df.copy()

    else:
        return df.copy()
def faktor_wechselrichter(wechselrichter_kw, daten):
    if wechselrichter_kw <= 2.5:
        return daten["Wechselrichter 2.5 kW, Max. Leistung kWp"]
    elif wechselrichter_kw <= 5:
        return daten["Wechselrichter 5 kW, Max. Leistung kWp"]
    elif wechselrichter_kw <= 10:
        return daten["Wechselrichter 10 kW, Max. Leistung kWp"]
    else:
        return daten["Wechselrichter 20 kW, Max. Leistung kWp"]
def faktor_batterie(batteriekapazitaet, daten):
    if batteriekapazitaet <= 5:
        return daten["Batterie Li-Ionen 5 kWh, Speicherkap. kWh"]
    else:
        return daten["Batterie Li-Ionen 20 kWh, Speicherkap. kWh"]
def faktor_pv_dachart(dachart, daten):
    if dachart == "Schrägdach":
        return daten["Solarstromanlage Schrägdach Marktmix, Max. Leistung kWp"]
    elif dachart == "Flachdach":
        return daten["Solarstromanlage Flachdach Marktmix, Max. Leistung kWp"]
    elif dachart == "Fassade":
        return daten["Solarstromanlage Fassade Marktmix, Max. Leistung kWp"]
    else:
        return daten["Solarstromanlage Marktmix, Max. Leistung kWp"]
def berechne_umweltwirkung(
    df_ts,
    pv_anlagen_daten,
    wechselrichter_kw,
    batterie_aktiv,
    batteriekapazitaet,
    heizsystem,
    fossil_typ,
    wp_typ,
    wp_kw,
    erdsondenlaenge,
    ebf_m2,
    lebensdauer_pv=LebenszeitJahre["PV"],
    lebensdauer_batterie=LebenszeitJahre["Batterie"],
    lebensdauer_wp=LebenszeitJahre["WP"],
    lebensdauer_waermeerzeuger=LebenszeitJahre["Fossil/Holzheizung"],
    lebensdauer_wechselrichter=LebenszeitJahre["Wechselreichter"],
    auto_aktiv=False,
    auto_typ=None,
    auto_km_jahr=0.0,
    ev_aktiv=False,
    ev_km_jahr=0.0
):
    ergebnisse = []

    def add(name, ubp_total, co2_total):
        ergebnisse.append({
            "Kategorie": name,
            "UBP/a": ubp_total,
            "kg CO2-eq/a": co2_total
        })

    # PV-Module nach Dachart
    for anlage in pv_anlagen_daten:
        pv_ubp = faktor_pv_dachart(anlage["Dachart"], UBP) * anlage["pv_Peakleistung"]
        pv_co2 = faktor_pv_dachart(anlage["Dachart"], kgCO2eq) * anlage["pv_Peakleistung"]

        add(
            f"PV-Anlage {anlage['Anlage']} Herstellung",
            pv_ubp / lebensdauer_pv,
            pv_co2 / lebensdauer_pv
        )

    # Wechselrichter separat
    wr_ubp = faktor_wechselrichter(wechselrichter_kw, UBP) * wechselrichter_kw
    wr_co2 = faktor_wechselrichter(wechselrichter_kw, kgCO2eq) * wechselrichter_kw

    add(
        "Wechselrichter Herstellung",
        wr_ubp / lebensdauer_wechselrichter,
        wr_co2 / lebensdauer_wechselrichter
    )

    # Elektroinstallation separat, aber mit PV-Lebensdauer
    pv_kwp_total = sum(a["pv_Peakleistung"] for a in pv_anlagen_daten)

    elektro_ubp = UBP["Elektroinstallation Photovoltaikanlage"] * pv_kwp_total
    elektro_co2 = kgCO2eq["Elektroinstallation Photovoltaikanlage"] * pv_kwp_total

    add(
        "Elektroinstallation PV",
        elektro_ubp / lebensdauer_pv,
        elektro_co2 / lebensdauer_pv
    )
    # Batterie
    if batterie_aktiv and batteriekapazitaet > 0:
        batterie_ubp = faktor_batterie(batteriekapazitaet, UBP) * batteriekapazitaet
        batterie_co2 = faktor_batterie(batteriekapazitaet, kgCO2eq) * batteriekapazitaet
        add("Batterie Herstellung", batterie_ubp / lebensdauer_batterie, batterie_co2 / lebensdauer_batterie)

    # Strombezug Betrieb
    netzbezug_kWh = df_ts["netzbezug_kWh"].sum()
    strom_co2 = netzbezug_kWh * CO2Emmisionen_input / 1000
    add("Netzstrom Betrieb", 0, strom_co2)

    # Heizung Betrieb fossil / Holz
    heizwaerme_kWh = df_ts["heizwaerme_kWh"].sum()

    if heizsystem == "Fossil & Holz":
        if fossil_typ == "Öl":
            add(
                "Heizöl Betrieb",
                heizwaerme_kWh * UBP["HeizölEL pro kWh"],
                heizwaerme_kWh * kgCO2eq["HeizölEL pro kWh"]
            )
        elif fossil_typ == "Gas":
            add(
                "Erdgas Betrieb",
                heizwaerme_kWh * UBP["Erdgas pro kWh"],
                heizwaerme_kWh * kgCO2eq["Erdgas pro kWh"]
            )
        elif fossil_typ == "Pellets":
            add(
                "Pellets Betrieb",
                heizwaerme_kWh * UBP["Pellets pro kWh"],
                heizwaerme_kWh * kgCO2eq["Pellets pro kWh"]
            )

        # Wärmeerzeuger pauschal nach EBF
        add(
            "Wärmeerzeuger Herstellung",
            UBP["Wärmeerzeuger spez. Leistungsbedarf 30 W/m², EBF in m²"] * ebf_m2 / lebensdauer_waermeerzeuger,
            kgCO2eq["Wärmeerzeuger spez. Leistungsbedarf 30 W/m², EBF in m²"] * ebf_m2 / lebensdauer_waermeerzeuger
        )

    # Wärmepumpe Herstellung
    if heizsystem == "Wärmepumpe":

        if wp_typ == "Luft/Wasser WP":
            wp_ubp = UBP["Luft Wasser WP 7 kW, Gerät stk"] * (wp_kw / 7)
            wp_co2 = kgCO2eq["Luft Wasser WP 7 kW, Gerät stk"] * (wp_kw / 7)

        elif wp_typ == "Sole/Wasser WP":
            wp_ubp = UBP["Sole Wasser WP 7 kW, Gerät stk"] * (wp_kw / 7)
            wp_co2 = kgCO2eq["Sole Wasser WP 7 kW, Gerät stk"] * (wp_kw / 7)

            erdsonde_ubp = UBP["Erdsonden für Sole-Wasser-Wärmepumpe, Sondenlänge m"] * erdsondenlaenge
            erdsonde_co2 = kgCO2eq["Erdsonden für Sole-Wasser-Wärmepumpe, Sondenlänge m"] * erdsondenlaenge

            add(
                "Erdsonde Herstellung",
                erdsonde_ubp / LebenszeitJahre["Erdsonde"],
                erdsonde_co2 / LebenszeitJahre["Erdsonde"]
            )

        else:  # Wasser/Wasser WP
            wp_ubp = UBP["Förder- und Schluckbrunnen für Grundwasser-Wärmepumpe, Gerät stk"]
            wp_co2 = kgCO2eq["Förder- und Schluckbrunnen für Grundwasser-Wärmepumpe, Gerät stk"]

        add(
            "Wärmepumpe Herstellung",
            wp_ubp / lebensdauer_wp,
            wp_co2 / lebensdauer_wp
        )

        # Fossiles Auto: Lebenszykluswert pro Fahrzeugkilometer
    if auto_aktiv and auto_typ is not None and auto_km_jahr > 0:
        auto_ubp = Auto_Faktoren[auto_typ]["UBP/Fzkm"] * auto_km_jahr
        auto_co2 = Auto_Faktoren[auto_typ]["kg CO2-eq/Fzkm"] * auto_km_jahr

        add(
            f"Auto {auto_typ} Lebenszyklus",
            auto_ubp,
            auto_co2
        )

    # E-Auto: Lebenszykluswert pro Fahrzeugkilometer
    if ev_aktiv and ev_km_jahr > 0:
        ev_ubp = Auto_Faktoren["E-Auto"]["UBP/Fzkm"] * ev_km_jahr
        ev_co2 = Auto_Faktoren["E-Auto"]["kg CO2-eq/Fzkm"] * ev_km_jahr

        add(
            "E-Auto Lebenszyklus",
            ev_ubp,
            ev_co2
        )

    return pd.DataFrame(ergebnisse)   
#Profile
def speichere_profil(profilname, profil):
    pfad = os.path.join(PROFILE_DIR, f"{profilname}.json")
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(profil, f, indent=4, ensure_ascii=False)
def lade_profil(profilname):
    pfad = os.path.join(PROFILE_DIR, f"{profilname}.json")
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)
def liste_profile():
    return [
        f.replace(".json", "")
        for f in os.listdir(PROFILE_DIR)
        if f.endswith(".json")
    ]
#farbliche Darstellung Autarkiegrad
def autarkie_farbe(wert):
    if wert < 10:
        return "#ff4b1f"
    elif wert < 20:
        return "#ff7a1a"
    elif wert < 30:
        return "#ffa51f"
    elif wert < 40:
        return "#ffc928"
    elif wert < 50:
        return "#ffe04a"
    elif wert < 60:
        return "#d9d84a"
    elif wert < 70:
        return "#b6cc38"
    elif wert < 80:
        return "#8fbd2e"
    elif wert < 90:
        return "#63a827"
    else:
        return "#3f8f1f"
def add_g25_profile(df, g25_df, jahresstromverbrauch):
    df = df.copy()

    df["Zeit"] = df.index.strftime("%H:%M")
    df["Monat"] = df.index.month

    g25 = g25_df.copy()
    g25["Monat"] = g25["Monat"].astype(int)
    g25["Zeit"] = g25["Zeit"].astype(str).str[:5]

    g25_lookup = g25.set_index(["Monat", "Zeit"])

    df["g25_wert"] = [
        g25_lookup.loc[(m, z), "G25"]
        for m, z in zip(df["Monat"], df["Zeit"])
    ]

    faktor_summe = df["g25_wert"].sum()

    df["hauslast_kWh"] = (
        df["g25_wert"] / faktor_summe * jahresstromverbrauch
    )

    return df
def create_values_pdf(jahreskennzahlen, df_umwelt, df_ts):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Export Simulationsergebnisse")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Jahreskennzahlen")
    y -= 25

    c.setFont("Helvetica", 10)
    
    max_einspeiseleistung_kw = df_ts["netzeinspeisung_kWh"].max() / 0.25

    werte = {
        "PV-Produktion kWh/a": jahreskennzahlen["PV_Produktion_kWh"],
        "Gesamtlast kWh/a": df_ts["gesamtlast_kWh"].sum(),
        "Netzbezug kWh/a": jahreskennzahlen["Netzbezug_kWh"],
        "Netzeinspeisung kWh/a": jahreskennzahlen["Netzeinspeisung_kWh"],
        "Eigenverbrauch kWh/a": jahreskennzahlen["Eigenverbrauch_kWh"],
        "Autarkiegrad %": jahreskennzahlen["Autarkiegrad_%"],
        "Eigenverbrauchsquote %": jahreskennzahlen["Eigenverbrauchsquote_%"],
        "Abgeregelte Energie kWh/a": jahreskennzahlen["Abgeregelte_Energie_kWh"],
        "Unterdeckung kWh/a": jahreskennzahlen["Unterdeckung_kWh"],
        "Eingesparte Stromkosten CHF/a": jahreskennzahlen["Eingesparte_Stromkosten_CHF"],
        "Max. Einspeiseleistung kW": max_einspeiseleistung_kw,
    }

    for name, wert in werte.items():
        c.drawString(50, y, f"{name}: {wert:,.2f}".replace(",", "'"))
        y -= 18

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Umweltwirkungen")
    y -= 25

    c.setFont("Helvetica", 10)

    for _, row in df_umwelt.iterrows():
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

        c.drawString(
            50,
            y,
            f"{row['Kategorie']}: {row['UBP/a']:,.0f} UBP/a, {row['kg CO2-eq/a']:,.0f} kg CO2-eq/a".replace(",", "'")
        )
        y -= 18

    c.save()
    buffer.seek(0)
    return buffer
def berechne_ev_jahresbedarf(ev_config):
    if not ev_config["aktiv"]:
        return 0.0

    anzahl_fahrtage_pro_woche = len(ev_config["fahrtage"])
    anzahl_nicht_fahrtage_pro_woche = 7 - anzahl_fahrtage_pro_woche

    km_jahr = (
        anzahl_fahrtage_pro_woche * ev_config["km_pro_fahrtag"] * 52
        + anzahl_nicht_fahrtage_pro_woche * ev_config["km_nicht_fahrtag"] * 52
    )

    ev_strom_jahr = km_jahr * ev_config["verbrauch_pro_100km"] / 100

    return ev_strom_jahr
def berechne_ev_jahreskilometer(ev_config):
    if not ev_config["aktiv"]:
        return 0.0

    anzahl_fahrtage_pro_woche = len(ev_config["fahrtage"])
    anzahl_nicht_fahrtage_pro_woche = 7 - anzahl_fahrtage_pro_woche

    km_jahr = (
        anzahl_fahrtage_pro_woche * ev_config["km_pro_fahrtag"] * 52
        + anzahl_nicht_fahrtage_pro_woche * ev_config["km_nicht_fahrtag"] * 52
    )

    return km_jahr
def berechne_kostenkennzahlen(
    df_ts,
    jahreskennzahlen,
    pv_kwp_total,
    batterie_aktiv,
    batteriekapazitaet,
    pv_investition_brutto,
    batteriekosten_chf,
    optimierungskosten_chf,
    foerderanteil_pv_prozent,
    betriebskosten_prozent,
    strompreis_chf_kWh,
    ruecklieferverguetung_chf_kWh,
    betrachtungsdauer_jahre
):
    gesamtlast_kWh = df_ts["gesamtlast_kWh"].sum()
    pv_produktion_kWh = jahreskennzahlen["PV_Produktion_kWh"]
    netzbezug_kWh = jahreskennzahlen["Netzbezug_kWh"]
    netzeinspeisung_kWh = jahreskennzahlen["Netzeinspeisung_kWh"]

    if batterie_aktiv and batteriekapazitaet > 0:
        batterie_investition = batteriekosten_chf
    else:
        batterie_investition = 0.0

    investition_brutto = (
        pv_investition_brutto
        + batterie_investition
        + optimierungskosten_chf
    )

    # Förderung nur auf PV-Investition bezogen
    foerderung = pv_investition_brutto * foerderanteil_pv_prozent / 100

    investition_netto = max(0.0, investition_brutto - foerderung)

    # Laufende Kosten pro Jahr
    betriebskosten_jahr = investition_brutto * betriebskosten_prozent / 100

    # Stromkosten ohne PV
    stromkosten_ohne_pv = gesamtlast_kWh * strompreis_chf_kWh

    # Stromkosten mit PV
    strombezugskosten_mit_pv = netzbezug_kWh * strompreis_chf_kWh
    einspeiseerloes = netzeinspeisung_kWh * ruecklieferverguetung_chf_kWh

    stromkosten_mit_pv_ohne_betrieb = (
        strombezugskosten_mit_pv - einspeiseerloes
    )

    stromkosten_mit_pv_inkl_betrieb = (
        strombezugskosten_mit_pv
        - einspeiseerloes
        + betriebskosten_jahr
    )

    jaehrlicher_kostenvorteil = (
        stromkosten_ohne_pv - stromkosten_mit_pv_inkl_betrieb
    )

    if jaehrlicher_kostenvorteil > 0:
        amortisationszeit_jahre = investition_netto / jaehrlicher_kostenvorteil
    else:
        amortisationszeit_jahre = np.nan

    # Vereinfachte Stromgestehungskosten des PV-Systems
    if pv_produktion_kWh > 0 and betrachtungsdauer_jahre > 0:
        stromgestehungskosten_chf_kWh = (
            investition_netto
            + betriebskosten_jahr * betrachtungsdauer_jahre
        ) / (pv_produktion_kWh * betrachtungsdauer_jahre)
    else:
        stromgestehungskosten_chf_kWh = np.nan

    return {
        "PV-Investition brutto CHF": pv_investition_brutto,
        "Batterie-Investition CHF": batterie_investition,
        "Optimierung/Steuerung CHF": optimierungskosten_chf,
        "Investition brutto CHF": investition_brutto,
        "Förderung CHF": foerderung,
        "Investition netto CHF": investition_netto,
        "Betriebskosten CHF/a": betriebskosten_jahr,
        "Stromkosten ohne PV CHF/a": stromkosten_ohne_pv,
        "Strombezugskosten mit PV CHF/a": strombezugskosten_mit_pv,
        "Einspeiseerlös CHF/a": einspeiseerloes,
        "Stromkosten mit PV ohne Betrieb CHF/a": stromkosten_mit_pv_ohne_betrieb,
        "Stromkosten mit PV inkl. Betrieb CHF/a": stromkosten_mit_pv_inkl_betrieb,
        "Jährlicher Kostenvorteil CHF/a": jaehrlicher_kostenvorteil,
        "Amortisationszeit Jahre": amortisationszeit_jahre,
        "Stromgestehungskosten CHF/kWh": stromgestehungskosten_chf_kWh,
        "Stromgestehungskosten Rp/kWh": stromgestehungskosten_chf_kWh * 100,
    }


st.header("Dimensionierungstool für Photovoltaik- und Batterieanlagen in Einfamilienhäusern mit Leistungsbegrenzung der elektrischen Einspeisung und des Bezugs ")

#profile
st.subheader("Profile")
profil_name = st.text_input("Profilname", value="Profil 1")
vorhandene_profile = liste_profile()
vergleichsmodus = st.checkbox("Profile vergleichen pro Jahr", value=False)
if vergleichsmodus:
    if len(vorhandene_profile) < 2:
        st.info("Speichere zuerst mindestens zwei Profile.")
        st.stop()

    ausgewaehlte_profile = st.multiselect(
        "Profile auswählen",
        vorhandene_profile,
        default=vorhandene_profile[:2],
        max_selections=5
    )

    if len(ausgewaehlte_profile) < 2:
        st.info("Bitte mindestens zwei Profile auswählen.")
        st.stop()

    profile_daten = []

    for name in ausgewaehlte_profile:
        profil = lade_profil(name)
        df_umwelt = pd.DataFrame(profil["df_umwelt"])

        profile_daten.append({
            "name": name,
            "profil": profil,
            "total_ubp": df_umwelt["UBP/a"].sum(),
            "total_co2": df_umwelt["kg CO2-eq/a"].sum()
        })

    st.subheader("Profilvergleich Jahreskennzahlen")

    cols = st.columns(len(profile_daten))

    for col, p in zip(cols, profile_daten):
        profil = p["profil"]

        with col:
            st.markdown(f"### {p['name']}")
            st.metric("Autarkiegrad", f"{profil['jahreskennzahlen']['Autarkiegrad_%']:,.1f} %".replace(",", "'"))
            st.metric("Eigenverbrauchsquote", f"{profil['jahreskennzahlen']['Eigenverbrauchsquote_%']:,.1f} %".replace(",", "'"))
            st.metric("PV-Produktion", f"{profil['jahreskennzahlen']['PV_Produktion_kWh']:,.0f} kWh".replace(",", "'"))
            st.metric("Netzbezug", f"{profil['jahreskennzahlen']['Netzbezug_kWh']:,.0f} kWh".replace(",", "'"))
            st.metric("Abregelung", f"{profil['jahreskennzahlen']['Abgeregelte_Energie_kWh']:,.1f} kWh".replace(",", "'"))
            st.metric("Total UBP", f"{p['total_ubp']:,.0f} UBP/a".replace(",", "'"))
            st.metric("Total CO₂", f"{p['total_co2']:,.0f} kg CO₂-eq/a".replace(",", "'"))

    st.write("------------------------------")
    st.subheader("Jahresverlauf im Vergleich")

    vergleichswert = st.selectbox(
        "Kennwert für Jahresdiagramm auswählen",
        [
            "pv_kWh",
            "gesamtlast_kWh",
            "netzbezug_kWh",
            "netzeinspeisung_kWh",
            "abregelung_kWh"
        ],
        format_func=lambda x: {
            "pv_kWh": "PV-Produktion",
            "gesamtlast_kWh": "Gesamtlast",
            "netzbezug_kWh": "Netzbezug",
            "netzeinspeisung_kWh": "Netzeinspeisung",
            "abregelung_kWh": "Abregelung"
        }[x]
    )

    fig_vergleich = go.Figure()

    for p in profile_daten:
        profil = p["profil"]

        if "monatswerte" not in profil:
            st.warning(f"Profil '{p['name']}' enthält noch keine Monatswerte. Bitte dieses Profil neu simulieren und speichern.")
            continue

        df_monat = pd.DataFrame.from_dict(profil["monatswerte"], orient="index")
        df_monat.index = pd.to_datetime(df_monat.index)

        fig_vergleich.add_trace(go.Scatter(
            x=df_monat.index,
            y=df_monat[vergleichswert],
            mode="lines+markers",
            name=p["name"]
        ))

    fig_vergleich.update_layout(
        title="Monatlicher Jahresverlauf im Profilvergleich",
        xaxis_title="Monat",
        yaxis_title="Energie in kWh/Monat",
        height=500,
        legend=dict(orientation="h", y=-0.2)
    )

    fig_vergleich.update_xaxes(
        tickformat="%b",
        dtick="M1"
    )

    st.plotly_chart(fig_vergleich, use_container_width=True)

    st.stop()

#allgemein
col1, col2, col3 = st.columns(3)
with col1: 
    EBFm2 = st.number_input("Energiebezugsfläche (EBF) in m²", 50, 5000, 200)
    st.caption(
        "Falls die Energiebezugsfläche nicht bekannt ist, kann näherungsweise die Wohnfläche verwendet werden. "
        "Die EBF umfasst alle beheizten bzw. klimatisierten Bereiche eines Gebäudes."
    ) 
with col2:
    personen = st.number_input("Anzahl Personen im Haushalt", 1, 20, 4)

with col3:
    Stromnutzung = st.radio(
        "Stromprofil wählen",
        ["Standardprofil EFH", "Standardprofil Gewerbe (G25, nur Fallstudie)", "eigene Daten"],
        horizontal=True
    )
    uploaded_file = None
    if Stromnutzung == "eigene Daten":
        uploaded_file = st.file_uploader(
            "Upload Lastprofil",
            accept_multiple_files=False,
            type=["csv", "xlsx"]
        )
        st.caption("""
        CSV-/Excel-Format: 15-Minuten-Werte
        timestamp,verbrauch
        2025-01-01 00:00,0.42
        Bei Auswahl "Energie" bedeutet 0.42: Verbrauch von 00:00 bis 00:15 Uhr in kWh.
        Bei Auswahl "Leistung" bedeutet 0.42: mittlere Leistung während 00:00 bis 00:15 Uhr in kW.
        """)
        lastprofil_einheit = st.radio(
            "Einheit der hochgeladenen Werte",
            ["Energie pro 15-Minuten-Intervall in kWh", "mittlere Leistung im Intervall in kW"],
            horizontal=False
        )
    

st.write("**Jahresstrombedarf**")

anzahl_stromjahre = st.number_input(
    "Anzahl Jahre für Strombedarf",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

stromjahre_daten = []

for i in range(anzahl_stromjahre):
    col_jahr, col_verbrauch = st.columns(2)

    with col_jahr:
            jahr = st.number_input(
                f"Jahr {i+1}",
                min_value=2000,
                max_value=2100,
                value=2024 - i,
                step=1,
                key=f"strom_jahr_{i}"
            )

    with col_verbrauch:
            verbrauch = st.number_input(
                f"Strombedarf {i+1} in kWh/a",
                min_value=0.0,
                max_value=100000.0,
                value=10000.0,
                step=100.0,
                key=f"strom_verbrauch_{i}",
                format="%.1f"
            )

    stromjahre_daten.append({
            "jahr": int(jahr),
            "verbrauch_kWh": float(verbrauch)
        })

jahresstromverbrauch = np.mean([
        eintrag["verbrauch_kWh"]
        for eintrag in stromjahre_daten
])

st.caption(
        f"Verwendeter Mittelwert für die Simulation: {jahresstromverbrauch:.0f} kWh/a"
)
strombedarf_modus = st.radio(
        "Wie soll der eingegebene Jahresstrombedarf verwendet werden?",
        [
            "Ist-Zustand: gemessene Gesamtlast aus Stromrechnung verwenden",
            "Szenario: Haushaltsstrom ohne WP/WW/E-Auto eingeben",
            "Szenario aus Stromrechnung: Gesamtstrom auf Haushaltsstrom zurückrechnen"
        ],
        index=2,
        horizontal=False
)

strombedarf_ist_gesamt = (
        strombedarf_modus == "Ist-Zustand: gemessene Gesamtlast aus Stromrechnung verwenden"
)

strombedarf_szenario_basis = (
        strombedarf_modus == "Szenario: Haushaltsstrom ohne WP/WW/E-Auto eingeben"
)

strombedarf_rueckrechnung = (
        strombedarf_modus == "Szenario aus Stromrechnung: Gesamtstrom auf Haushaltsstrom zurückrechnen"
)

if strombedarf_ist_gesamt:
        st.info(
            "Der eingegebene Jahresstrombedarf wird als gemessene Gesamtlast verwendet. "
            "Wärmepumpe, Warmwasser und E-Auto werden nicht zusätzlich addiert."
        )

elif strombedarf_szenario_basis:
        st.info(
            "Der eingegebene Jahresstrombedarf wird als Haushaltsstrom ohne Wärmepumpe, Warmwasser und E-Auto verwendet. "
            "WP, WW und E-Auto werden zusätzlich berechnet."
        )

elif strombedarf_rueckrechnung:
        st.info(
            "Der eingegebene Jahresstrombedarf wird als gemessene Gesamtlast verwendet. "
            "Das Tool zieht die geschätzten Anteile für Wärmepumpe, Warmwasser und E-Auto ab und berechnet daraus den Haushaltsstrom. "
            "Danach werden WP, WW und E-Auto für das Szenario neu dazugerechnet."
        )
    
st.write("-----------------------")
#Heizwärmebedarf-Ermittlung & Heizsystem
fossil_typ = "Gas"      # default
wp_typ = "Luft/Wasser WP"  # default
Erdsondentiefe = 0      # default
jaz = 2.5               # default
Heizwaermebedarf = 0
col1, col2 =st.columns(2)
with col1:
    st.subheader("Heizwärmebedarf-Ermittlung")
    # aus Baujahr Heizwärmebedarf kWh/m2
    m2 = st.number_input("Fläche des EFH in m²", 50, 5000, 200)
    bau_typ = st.selectbox(
        "Gebäudestandard",
        ["Baujahr", "Minergie", "Minergie-P"]
    )
    if bau_typ == "Baujahr":
        Baujahr = st.number_input("Baujahr", 1900, 2015, 1990)

        treffer = df_Bautyp_Heizwaermebedarf.loc[
            df_Bautyp_Heizwaermebedarf["Bautyp"] == Baujahr,
            "Heizwaermebedarf"
        ]

        if not treffer.empty:
            heizwaermebedarf_spez = float(treffer.iloc[0])
            Heizwaermebedarf_basis = heizwaermebedarf_spez * m2

            st.metric(
                "Typischer Heizwärmebedarf nach Baujahr",
                f"{Heizwaermebedarf_basis:,.0f} kWh/a".replace(",", "'")
            )

            st.caption(
                f"Berechnet aus {heizwaermebedarf_spez:.0f} kWh/m²a × {m2:.0f} m². "
                "Dieser Wert ist ein statistischer Vorschlagswert für ein typisches Gebäude dieses Jahrgangs. "
                "Gebäudespezifische Werte aus GEAK, Messdaten oder Projektdaten können deutlich davon abweichen."
            )

            status = st.radio(
                "Gebäude saniert oder GEAK / Projektwert bekannt?",
                ["Nein", "Ja, saniert", "GEAK Klasse", "GEAK / Wert direkt"],
                horizontal=True
            )

            if status == "Ja, saniert":
                Sanierungstyp = st.multiselect(
                    "Sanierungstyp",
                    list(reduktionen.keys())
                )

                reduktion = sum(reduktionen[typ] for typ in Sanierungstyp)
                reduktion = min(reduktion, 0.75)

                Heizwaermebedarf_vorschlag = Heizwaermebedarf_basis * (1 - reduktion)

                st.caption(
                    f"Ausgangswert: {Heizwaermebedarf_basis:,.0f} kWh/a, ".replace(",", "'") +
                    f"Reduktion durch Sanierung: {reduktion*100:.0f} %, "
                    f"Vorschlagswert nach Sanierung: {Heizwaermebedarf_vorschlag:,.0f} kWh/a".replace(",", "'")
                )

            elif status == "GEAK Klasse":
                geak_klasse = st.selectbox(
                    "GEAK Klasse wählen",
                    list(GEAK_Klassen.keys())
                )

                Heizwaermebedarf_vorschlag = GEAK_Klassen[geak_klasse] * m2

                st.caption(
                    f"GEAK-Klasse {geak_klasse}: "
                    f"{GEAK_Klassen[geak_klasse]} kWh/m²a × {m2:.0f} m² = "
                    f"{Heizwaermebedarf_vorschlag:,.0f} kWh/a".replace(",", "'")
                )

            elif status == "GEAK / Wert direkt":
                eingabe_art = st.radio(
                    "Eingabeart",
                    ["spezifisch in kWh/m²a", "total in kWh/a"],
                    horizontal=True
                )

                if eingabe_art == "spezifisch in kWh/m²a":
                    heizwaermebedarf_spez_direkt = st.number_input(
                        "Heizwärmebedarf spezifisch in kWh/m²a",
                        min_value=0.0,
                        max_value=300.0,
                        value=44.0,
                        step=1.0,
                        format="%.1f"
                    )

                    Heizwaermebedarf_vorschlag = heizwaermebedarf_spez_direkt * m2

                    st.caption(
                        f"GEAK-/Projektwert: {heizwaermebedarf_spez_direkt:.1f} kWh/m²a × "
                        f"{m2:.0f} m² = {Heizwaermebedarf_vorschlag:,.0f} kWh/a".replace(",", "'")
                    )

                else:
                    Heizwaermebedarf_vorschlag = st.number_input(
                        "Heizwärmebedarf total in kWh/a",
                        min_value=0.0,
                        max_value=500000.0,
                        value=float(round(Heizwaermebedarf_basis * 0.5, -3)),
                        step=100.0,
                        format="%.0f"
                    )

                    st.caption(
                        "Der Heizwärmebedarf wird direkt als Jahreswert eingegeben."
                    )

            else:
                Heizwaermebedarf_vorschlag = Heizwaermebedarf_basis

                st.caption(
                    "Es wird der typische Heizwärmebedarf nach Baujahr und Fläche verwendet."
                )

            heizwaerme_manuell_anpassen = st.checkbox(
                "Heizwärmebedarf manuell anpassen",
                value=False
            )

            if heizwaerme_manuell_anpassen:
                Heizwaermebedarf_input = st.number_input(
                    "Verwendeter Heizwärmebedarf für Simulation in kWh/a",
                    min_value=0.0,
                    max_value=500000.0,
                    value=float(round(Heizwaermebedarf_vorschlag, 0)),
                    step=100.0,
                    format="%.0f",
                    key=f"heizwaermebedarf_manuell_{Baujahr}_{status}_{str(locals().get('Sanierungstyp', ''))}"
                )
            else:
                Heizwaermebedarf_input = float(Heizwaermebedarf_vorschlag)

            raumheizung_waermebedarf_kWh = Heizwaermebedarf_input
            ergebnis = Heizwaermebedarf_input

            st.metric(
                "Verwendeter Heizwärmebedarf",
                f"{Heizwaermebedarf_input:,.0f} kWh/a".replace(",", "'")
            )

        else:
            st.error("Dieses Baujahr wurde in der Tabelle nicht gefunden.")
    elif bau_typ == "Minergie":
        treffer = df_Bautyp_Heizwaermebedarf.loc[df_Bautyp_Heizwaermebedarf["Bautyp"] == bau_typ, "Heizwaermebedarf"]
        if not treffer.empty:
            Heizwaermebedarf = treffer.iloc[0] * m2
            Heizwaermebedarf_input = st.number_input(
                "Heizwärmebedarf kWh/²",
                value=int(Heizwaermebedarf)
            )
            raumheizung_waermebedarf_kWh = Heizwaermebedarf_input

            st.write(f"Anteil Raumheizung in kWh/a: {raumheizung_waermebedarf_kWh:.0f}")
            ergebnis = Heizwaermebedarf_input
        else:
            st.error("Dieses Baujahr wurde in der Tabelle nicht gefunden.")
    elif bau_typ == "Minergie-P":
        treffer = df_Bautyp_Heizwaermebedarf.loc[df_Bautyp_Heizwaermebedarf["Bautyp"] == bau_typ, "Heizwaermebedarf"]
        if not treffer.empty:
            Heizwaermebedarf = treffer.iloc[0] * m2
            Heizwaermebedarf_input = st.number_input(
                "Heizwärmebedarf kWh/m²",
                value=int(Heizwaermebedarf)
            )
            ww_waermebedarf_kWh = 15 * m2 # 15 kWh/m²a × Wohnfläche wert noch nach quelle finden
            raumheizung_waermebedarf_kWh = Heizwaermebedarf_input

            st.write(f"Anteil Raumheizung in kWh/a: {raumheizung_waermebedarf_kWh:.0f}")
            ergebnis = Heizwaermebedarf_input
        else:
            st.error("Dieses Baujahr wurde in der Tabelle nicht gefunden.")
with col2:
    st.subheader("Heizsystem")

    heizsystem = st.radio(
        "Heizsystem wählen",
        ["Fossil & Holz", "Wärmepumpe"],
        index=0,
        horizontal=True
    )
    if heizsystem == "Fossil & Holz":
        fossil_typ = st.radio(
            "Fossiles Heizsystem",
            ["Gas", "Öl", "Pellets"],
            horizontal=True
        )
        if fossil_typ == "Gas":
            gas = Heizwaermebedarf / 10
            Gasverbrauch_input = st.number_input(
                "Gasverbrauch in m³/a",
                value=int(gas)
            )
            ergebnis = Gasverbrauch_input
        elif fossil_typ == "Öl":
            oel = Heizwaermebedarf / 10
            Oelverbrauch_input = st.number_input(
                "Ölverbrauch in L/a",
                value=int(oel)
            )
            ergebnis = Oelverbrauch_input
        elif fossil_typ == "Pellets":
            pellets = Heizwaermebedarf / 5
            Pelletsverbrauch_input = st.number_input(
                "Pelletsverbrauch in kg/a",
                value=int(pellets)
            )
            ergebnis = Pelletsverbrauch_input
        # .1f = 1 Nachkommastelle zb st.write(f"Gasverbrauch: {gas:.1f} m³/a")
        # variablen direkt in text als f-String (formatted string).
    elif heizsystem == "Wärmepumpe":
        wp_typ = st.radio(
            "Wärmepumpenart WP",
            [
                "Luft/Wasser WP",
                "Sole/Wasser WP",
                "Wasser/Wasser WP"
            ],
            horizontal=True
        )
        WPkW = st.number_input(
            "Wärmepumpe in kW",
            min_value=1.0,
            max_value=100.0,
            value=7.0,
            step=0.1,
            format="%.1f"
        )
        Auslegetemperatur = st.number_input(
            "Auslegetemperatur in °C",
            min_value=-25,
            max_value=10,
            value=-7
        )
        Vorlauftemperatur_Auslegung = st.number_input(
            "Vorlauftemperatur bei Auslegetemperatur in °C",
            min_value=20,
            max_value=70,
            value=40
        )
        #Wärmequellentemperatur = st.number_input("Wärmequellentemperatur (°)", 0, 60, 35)#oder aus wetterdaten
        if wp_typ == "Luft/Wasser WP":
            jaz = st.number_input("JAZ", min_value=0.1, max_value=10.0, value=2.5, step=0.1, format="%.1f")
        elif wp_typ == "Sole/Wasser WP":
            Erdsondentiefe = st.number_input("Gesamt Erdsondenlänge in m", min_value=0.1, max_value=500.0, value= 150.0, step=0.1, format="%.1f")
            jaz = st.number_input("JAZ", min_value=0.1, max_value=10.0, value=4.5, step=0.1, format="%.1f")
        else:
            jaz = st.number_input("JAZ", min_value=0.1, max_value=10.0, value=4.0, step=0.1, format="%.1f")
        if "Heizwaermebedarf_input" in locals():
            StromverbrauchWP_input = Heizwaermebedarf_input / jaz
        else:
            StromverbrauchWP_input = 0.0

        st.write(
            f"Geschätzter Stromverbrauch Wärmepumpe: {StromverbrauchWP_input:.0f} kWh/a"
        )

        ergebnis = StromverbrauchWP_input
    raumtemperatur = st.number_input(
        "Gewünschte Raumtemperatur in °C",
        min_value=15.0,
        max_value=25.0,
        value=20.0,
        step=0.5, 
        format="%.1f"
    )
    st.caption("JAZ = Jahresarbeitszahl. Verhältnis von erzeugter Wärme zu elektrischem Energiebedarf über ein Jahr.")
st.write("------------------------------")
#Warmwasser & EAuto
col1, col2 = st.columns(2)
with col1:
    st.subheader("Warmwasser (WW)")

    ww_liter_pro_person_tag = 40
    ww_tagesbedarf_liter = personen * ww_liter_pro_person_tag

    ww_system = st.selectbox(
        "WW-System",
        [
            "nicht elektrisch",
            "Elektroboiler",
            "Wärmepumpenboiler"
        ]
    )

    ww_aktiv = ww_system != "nicht elektrisch"
    ww_steuerbar = False
    ww_bedarf_kWh_tag = 0.0
    ww_ladeleistung_kw = 0.0
    ww_strategie = WW_ABEND

    if not ww_aktiv:
        st.caption("WW wird nicht als elektrische Last simuliert.")

    else:
        st.caption(f"{ww_system} wird als elektrische WW-Last berücksichtigt.")

        ww_speicher_liter = st.selectbox(
            "WWspeicher / Boiler in Liter",
            list(range(50, 1001, 50)),
            index=3
        )

        ladezyklen_pro_tag = int(np.ceil(ww_tagesbedarf_liter / ww_speicher_liter))

        st.write(f"Geschätzter Tagesbedarf WW für Haushalt (40L/p/Tag): {ww_tagesbedarf_liter:.0f} Liter/Tag")
        st.write(f"Gewählter Speicher: {ww_speicher_liter:.0f} Liter")
        st.write(f"Erforderliche Speicherladung: {ladezyklen_pro_tag}× pro Tag")

        ww_waermebedarf_kWh_jahr = personen * 45 * 0.058 * 7 * 50
        speicherverlust_kWh_jahr = 365 / 2

        if ww_system == "Elektroboiler":
            ww_bedarf_kWh_tag_berechnet = (
                ww_waermebedarf_kWh_jahr + speicherverlust_kWh_jahr
            ) / 365

            ww_label = "Strombedarf Elektroboiler in kWh/Tag"

        elif ww_system == "Wärmepumpenboiler":
            jaz_ww = st.number_input(
                "JAZ WW-Wärmepumpe",
                min_value=0.1,
                max_value=10.0,
                value=2.5,
                step=0.1,
                format="%.1f"
            )

            ww_bedarf_kWh_tag_berechnet = (
                (ww_waermebedarf_kWh_jahr + speicherverlust_kWh_jahr) / jaz_ww
            ) / 365

            ww_label = "Strombedarf Wärmepumpenboiler in kWh/Tag"

        ww_bedarf_kWh_tag_berechnet = float(round(ww_bedarf_kWh_tag_berechnet, 2))

        ww_bedarf_kWh_tag = st.number_input(
            ww_label,
            min_value=0.0,
            max_value=max(100.0, ww_bedarf_kWh_tag_berechnet),
            value=ww_bedarf_kWh_tag_berechnet,
            step=0.1,
            format="%.1f"
        )

        ww_ladeleistung_kw = st.number_input(
            "WW-/Boiler-Leistung in kW",
            min_value=0.1,
            max_value=20.0,
            value=3.0,
            step=0.1,
            format="%.1f"
        )

        ww_steuerbar = st.checkbox("Warmwasser zeitgesteuert", value=True)

        if ww_steuerbar:

            lwwp_relevant = (
                heizsystem == "Wärmepumpe"
                and wp_typ == "Luft/Wasser WP"
            )

            if lwwp_relevant:
                if ladezyklen_pro_tag <= 1:
                    ww_optionen = [
                        WW_NACHMITTAG_LWWP,
                        WW_PV,
                        WW_MORGEN,
                        WW_ABEND
                    ]
                else:
                    ww_optionen = [
                        WW_NACHMITTAG_LWWP,
                        WW_PV,
                        WW_KOMBI
                    ]

                ww_default_index = 0

                st.caption(
                    "Bei Luft/Wasser-Wärmepumpen ist eine Warmwasserbereitung am Nachmittag "
                    "energetisch günstiger, da die Außentemperatur meist höher ist und der "
                    "Temperaturhub der Wärmepumpe dadurch kleiner wird. Dieser Effekt gilt nicht "
                    "in gleicher Form für Sole/Wasser- oder Wasser/Wasser-Wärmepumpen."
                )

            else:
                if ladezyklen_pro_tag <= 1:
                    ww_optionen = [
                        WW_PV,
                        WW_MORGEN,
                        WW_ABEND
                    ]
                else:
                    ww_optionen = [
                        WW_PV,
                        WW_KOMBI
                    ]

                ww_default_index = 0

            ww_strategie = st.selectbox(
                "WW-Strategie",
                ww_optionen,
                index=ww_default_index
            )

            if ww_strategie == WW_PV:
                st.caption(
                    "Der Boiler wird bevorzugt mit PV-Überschuss geladen. "
                    "Falls bis 11:00 Uhr nicht genügend PV-Energie verfügbar war, "
                    "wird die Ladung ab 11:00 Uhr automatisch abgeschlossen."
                )
    
with col2:
    st.subheader("E-Auto")

    ev_aktiv = st.checkbox("E-Auto vorhanden", value=False)

    if ev_aktiv:
        ev_fahrtage_namen = st.multiselect(
            "Fahrtage auswählen",
            ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
            default=["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        )

        tag_mapping = {
            "Montag": 0,
            "Dienstag": 1,
            "Mittwoch": 2,
            "Donnerstag": 3,
            "Freitag": 4,
            "Samstag": 5,
            "Sonntag": 6
        }

        ev_fahrtage = [tag_mapping[tag] for tag in ev_fahrtage_namen]

        ev_verbrauch_kWh_pro_100km = st.number_input(
            "Verbrauch in kWh/100 km",
            min_value=5.0,
            max_value=35.0,
            value=18.0,
            step=0.5,
            format="%.1f"
        )

        ev_km_pro_fahrtag = st.number_input(
            "Durchschnittliche Fahrstrecke pro Fahrtag in km",
            min_value=0.0,
            max_value=300.0,
            value=50.0,
            step=5.0,
            format="%.1f"
        )

        ev_km_nicht_fahrtag = st.number_input(
            "Fahrstrecke außerhalb der gewählten Fahrtage in km/Tag",
            min_value=0.0,
            max_value=300.0,
            value=0.0,
            step=5.0,
            format="%.1f"
        )
        st.caption("Für Tage, die nicht als regelmäßige Fahrtage ausgewählt wurden (z. B. Wochenenden, Freizeit oder Ferien)")
        st.caption(
            "Der Ladebedarf wird an Nicht-Fahrtagen zu Tagesbeginn und an den ausgewählten Fahrtagen nach der Rückkehr (17:00 Uhr) erzeugt. "
            "Die Ladung erfolgt anschließend innerhalb des gewählten Ladefensters."
        )
        ev_ladeleistung_kw = st.number_input(
            "E-Auto Ladeleistung in kW",
            min_value=0.1,
            max_value=22.0,
            value=3.7,
            step=0.1,
            format="%.1f"
        )

        ev_strategie = st.selectbox(
            "Wann steht das E-Auto zuhause und kann geladen werden?",
            [
                EV_MORGEN,
                EV_PV,
                EV_ABEND,
                EV_KOMBI
            ],
            index=2
        )
        st.write("Hinweis: Für die Berechnung wird angenommen, dass das Elektrofahrzeug ausschließlich zu Hause geladen wird. Ladevorgänge an öffentlichen Ladestationen oder an anderen Orten werden nicht berücksichtigt.")
    else:
        ev_fahrtage = []
        ev_verbrauch_kWh_pro_100km = 0.0
        ev_km_pro_fahrtag = 0.0
        ev_km_nicht_fahrtag = 0.0
        ev_ladeleistung_kw = 0.0
        ev_strategie = EV_ABEND

    #fossil auto
    auto_aktiv = st.checkbox("Auto vorhanden, aber kein-E Auto", value=False)

    auto_typ = None
    auto_km_woche = 0.0
    auto_km_jahr = 0.0


    if auto_aktiv:
        auto_typ = st.selectbox(
            "Antrieb Auto",
            ["Benzin", "Diesel", "Gas"]
        )

        auto_km_woche = st.number_input(
            "Gefahrene Kilometer pro Woche in km/Woche",
            min_value=0.0,
            max_value=100000.0,
            value=100.0,
            step=500.0,
            format="%.1f"
        )
        auto_km_jahr = auto_km_woche * 52

        st.caption(f"Entspricht ca. {auto_km_jahr:.0f} km pro Jahr.")

wp_strom_ist = 0.0
ww_strom_ist = 0.0
ev_strom_ist = 0.0

if strombedarf_rueckrechnung:
    st.write("------------------------------")
    st.subheader("Rückrechnung der Stromrechnung")

    # Vorschlagswerte aus den Eingaben berechnen
    wp_strom_vorschlag = StromverbrauchWP_input if heizsystem == "Wärmepumpe" else 0.0
    ww_strom_vorschlag = ww_bedarf_kWh_tag * 365 if ww_aktiv else 0.0

    ev_config_vorschlag = {
        "aktiv": ev_aktiv,
        "verbrauch_pro_100km": ev_verbrauch_kWh_pro_100km,
        "km_pro_fahrtag": ev_km_pro_fahrtag,
        "km_nicht_fahrtag": ev_km_nicht_fahrtag,
        "fahrtage": ev_fahrtage
    }

    ev_strom_vorschlag = berechne_ev_jahresbedarf(ev_config_vorschlag)

    st.write("Geschätzte Anteile aus den Eingaben:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write(f"WP-Strom: {wp_strom_vorschlag:,.0f} kWh/a".replace(",", "'"))
    with col2:
        st.write(f"Warmwasser: {ww_strom_vorschlag:,.0f} kWh/a".replace(",", "'"))
    with col3:
        st.write(f"E-Auto: {ev_strom_vorschlag:,.0f} kWh/a".replace(",", "'"))
    with col4:
        werte_manuell_anpassen = st.checkbox(
            "Geschätzte Anteile manuell anpassen",
            value=False
        )

    if werte_manuell_anpassen:
        wp_strom_ist = st.number_input(
            "WP-Strom im Ist-Zustand in kWh/a",
            min_value=0.0,
            max_value=100000.0,
            value=float(round(wp_strom_vorschlag, 0)),
            step=100.0,
            format="%.0f",
            key="wp_strom_ist_rueckrechnung"
        )

        ww_strom_ist = st.number_input(
            "Warmwasser-Strom im Ist-Zustand in kWh/a",
            min_value=0.0,
            max_value=50000.0,
            value=float(round(ww_strom_vorschlag, 0)),
            step=50.0,
            format="%.0f",
            key="ww_strom_ist_rueckrechnung"
        )

        ev_strom_ist = st.number_input(
            "E-Auto-Strom im Ist-Zustand in kWh/a",
            min_value=0.0,
            max_value=100000.0,
            value=float(round(ev_strom_vorschlag, 0)),
            step=100.0,
            format="%.0f",
            key="ev_strom_ist_rueckrechnung"
        )

    else:
        wp_strom_ist = wp_strom_vorschlag
        ww_strom_ist = ww_strom_vorschlag
        ev_strom_ist = ev_strom_vorschlag

    basislast_berechnet = max(
    0.0,
    jahresstromverbrauch - wp_strom_ist - ww_strom_ist - ev_strom_ist
    )

    basislast_vorschau = basislast_berechnet

    st.write(
        f"Zurückgerechneter Haushaltsstrom: {basislast_vorschau:,.0f} kWh/a".replace(",", "'")
    )

    if st.button("Haushaltsbasislast neu aus aktueller Stromrechnung berechnen"):
        st.session_state["fixe_basislast_kWh"] = basislast_berechnet
        st.rerun()
    abgezogene_anteile = wp_strom_ist + ww_strom_ist + ev_strom_ist

    if abgezogene_anteile > jahresstromverbrauch:
        st.warning(
            "Die geschätzten Anteile für Wärmepumpe, Warmwasser und E-Auto sind höher "
            "als der eingegebene Jahresstrombedarf. Dadurch würde rechnerisch kein "
            "Haushaltsstrom übrig bleiben. Bitte die Werte prüfen oder manuell anpassen."
        )

    st.write(
        f"Zurückgerechneter Haushaltsstrom: {basislast_vorschau:,.0f} kWh/a".replace(",", "'")
    )

    st.caption(
        "Die geschätzten Anteile werden vom gemessenen Gesamtstrom abgezogen. "
        "Die berechnete Haushaltslast bleibt für das Szenario konstant."
    )


st.write("------------------------------")
st.subheader("Photovoltaikanlage")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    standort_auswahl = st.selectbox(
        "Standort wählen",
        list(standort_dateien.keys())
    )
    meta_df = load_station_metadata("SIA4028_metadata_2023.csv")
    station_info_ui = get_station_info(
        meta_df,
        standort_auswahl if "standort_auswahl" in locals() else list(standort_dateien.keys())[0],
        standort_dateien
    )
with col2:
    Höhenmeter_standort = st.number_input(
        "Höhenmeter am Standort in m ü. M.",
        50, 5000, int(station_info_ui["altitude"])
    )
    st.caption(
        f"MeteoSchweiz-Station an ihrem Standort: {station_info_ui['altitude']:.0f} m ü. M."
    )
with col3:
    WechselrichterkW = st.number_input(
        "Wechselrichter in kW",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )
with col4:
    PVAnlagen = st.number_input(
        "Anzahl PV-Anlagen",
        min_value=1,
        max_value=5,
        value=1,
        step=1
    )
    st.caption("Ein Anlage gleicht einer Ausrichtung.")
with col5:
    pv_bestehend = st.checkbox(
        "PV-Anlage bereits vorhanden und reale Jahresproduktion bekannt",
        value=False
    )

    pv_produktion_real_mittelwert = None

    if pv_bestehend:
        anzahl_pv_jahre = st.number_input(
            "Anzahl Jahre für gemessene PV-Produktion",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )

        pv_jahre_daten = []

        for j in range(anzahl_pv_jahre):
            col_pv_jahr, col_pv_produktion = st.columns(2)

            with col_pv_jahr:
                pv_jahr = st.number_input(
                    f"PV-Jahr {j+1}",
                    min_value=2000,
                    max_value=2100,
                    value=2024 - j,
                    step=1,
                    key=f"pv_jahr_{j}"
                )

            with col_pv_produktion:
                pv_produktion = st.number_input(
                    f"Gemessene PV-Produktion {j+1} in kWh/a",
                    min_value=0.0,
                    max_value=100000.0,
                    value=12000.0,
                    step=100.0,
                    key=f"pv_produktion_{j}",
                    format="%.1f"
                )

            pv_jahre_daten.append({
                "jahr": int(pv_jahr),
                "produktion_kWh": float(pv_produktion)
            })

        pv_produktion_real_mittelwert = np.mean([
            eintrag["produktion_kWh"]
            for eintrag in pv_jahre_daten
        ])

        st.caption(
            f"Verwendeter Mittelwert der gemessenen PV-Produktion: "
            f"{pv_produktion_real_mittelwert:,.0f} kWh/a".replace(",", "'")
        )
pv_anlagen_daten = []
# pro Zeile maximal 3 PV-Anlagen nebeneinander
for start in range(0, PVAnlagen, 3):
    cols = st.columns(3)

    for j in range(3):
        i = start + j

        if i >= PVAnlagen:
            break

        with cols[j]:
            st.markdown(f"### PV-Anlage {i+1}")

            Dachart = st.radio(
                "Dach auf welches die Photovoltaik montiert ist",
                ["Flachdach", "Schrägdach", "Fassade"],
                index=1,
                horizontal=True,
                key=f"dachart_{i}"
            )

            PV_Wirkungsgrad = st.number_input(
                "PV Wirkungsgrad in %",
                min_value=0.1,
                max_value=100.0,
                value=20.0,
                step=0.1,
                key=f"PV_Wirkungsgrad_{i}",
                format="%.1f"
            )

            pv_Peakleistung = st.number_input(
                "PV-Peakleistung in kWp",
                min_value=0.0,
                max_value=1000.0,
                value=10.0,
                step=0.1,
                key=f"peakleistung_{i}",
                format="%.1f"
            )

            gamma_pdc_input = st.number_input(
                "Temperaturkoeffizient Pmax in 1/°C",
                min_value=-0.02,
                max_value=0.0,
                value=-0.0040,
                step=0.0001,
                format="%.4f",
                key=f"gamma_pdc_{i}"
            )
            if i == 0:
                st.caption("Der Temperaturkoeffizient beschreibt die Änderung der maximalen Modulleistung pro 1 °C Zelltemperatur. Der Standardwert von −0,004 1/°C entspricht einer Leistungsabnahme von 0,4 % pro °C über den Standard-Testbedingungen (25 °C Zelltemperatur).")

            nmot_input = st.number_input(
                "NMOT / NOCT in °C",
                min_value=20.0,
                max_value=80.0,
                value=45.0,
                step=0.5,
                key=f"nmot_{i}",
                format="%.1f"
            )
            performance_ratio_input = st.number_input(
                "Performance Ratio",
                min_value=0.5,
                max_value=1.1,
                value=0.85,
                step=0.01,
                key=f"performance_ratio_{i}"
            )
            if i == 0:
                st.caption(
                    "NOCT/NMOT beschreibt die typische Modultemperatur unter realitätsnahen Betriebsbedingungen. "
                    "Höhere Werte führen zu höheren Zelltemperaturen und tendenziell geringerer PV-Leistung."
                )
                st.caption(
                    "Standardwert: 45 °C. Typischer NMOT-/NOCT-Wert moderner PV-Module gemäss Herstellerdatenblättern."
                )
            Dachneigung = st.number_input(
                "Dachneigung in °",
                min_value=0,
                max_value=90,
                value=45,
                step=1,
                key=f"neigung_{i}"
            )

            Dachausrichtung = st.number_input(
                "Dachausrichtung / Azimut in °",
                min_value=0,
                max_value=380,
                value=180,
                step=1,
                key=f"ausrichtung_{i}"
            )
            if i == 0:
                st.caption("0 = Nord, 90 = Ost, 180 = Süd, 270 = West")
            pv_anlagen_daten.append({
                "Anlage": i + 1,
                "Dachart": Dachart,
                "PV_Wirkungsgrad": PV_Wirkungsgrad,
                "pv_Peakleistung": pv_Peakleistung,
                "Dachneigung": Dachneigung,
                "Dachausrichtung": Dachausrichtung,
                "gamma_pdc": gamma_pdc_input,
                "nmot": nmot_input,
                "performance_ratio": performance_ratio_input
            })

st.write("------------------------------")
# Batterie Einspeisen EMS Auspeisen
col1, col2 = st.columns(2)
with col1:
    st.subheader("Batterie")

    batterie_aktiv = st.checkbox("Batterie vorhanden", value=True)

    if batterie_aktiv:
        batteriekapazität = st.slider("Batteriekapazität in kWh", 1, 50, 10)
        maxLadeleistungBatterie = st.slider("Maximale Ladeleistung der Batterie in kW", 1, 20, 10)
        maxEntladeleistungBatterie = st.slider("Maximale Entladeleistung der Batterie in kW", 1, 20, 10)
        minSoC = st.number_input("Mininmal SoC in %", 0, 50, 20)
        maxSoC = st.number_input("Maximal SoC in %", 60, 100, 80)
        st.caption("SoC = State of Charge, also Ladezustand der Batterie. Min. SoC verhindert Tiefentladung, Max. SoC begrenzt die nutzbare obere Kapazität.")
        batterieWirkungsgrad = st.number_input("Wirkungsgrad Batterie in %", 80, 100, 95)
    else:
        batteriekapazität = 0
        maxLadeleistungBatterie = 0
        maxEntladeleistungBatterie = 0
        minSoC = 0
        maxSoC = 100
        batterieWirkungsgrad = 95
    
with col2:
    st.subheader("Energiemanagementsystem (EMS)")

    ems_optionen = []

    if ww_aktiv and ww_steuerbar:
        ems_optionen.append("Warmwasser")

    if ev_aktiv:
        ems_optionen.append("E-Auto")

    if batterie_aktiv and batteriekapazität > 0:
        ems_optionen.append("Batterie")

    prioritaeten = st.multiselect(
        "EMS-Priorität auswählen (1 links = höchste Priorität))",
        ems_optionen,
        default=ems_optionen
    )

    st.caption("Die Einspeisung erfolgt automatisch nach der EMS-Priorität. " \
    "Nicht auswählbare Verbraucher sind nicht aktiv oder nicht steuerbar.")
    # normale Hauslast plus Wärmepumpen-Raumheizung zuerst dann WW oder ev dann Batterie  dann Einspeisung
    
    st.subheader("Einspeisen")
    # regel einbauen minSoC muss < sein als maxSoC
    Einspeisegrenze = st.number_input("Einspeisegrenze in % bezogen auf die Peak-Leistung der PV-Anlage", 1, 100, 70)
    gesamt_pv_peakleistung = sum(anlage["pv_Peakleistung"] for anlage in pv_anlagen_daten)
    EinspeisegrenzekW = (Einspeisegrenze / 100) * gesamt_pv_peakleistung
    
    st.subheader("Netzbezug")
    Bezugsgrenze = st.number_input("Bezugsgrenze in kW bezieht sich auf die Absicherung des Gebäudes", 5, 100, 80)
    Strompreis = st.selectbox(
        "Strompreis in Rp./kWh", 
        list(strompreis_mapping.keys())
    )
    EVU_name = st.selectbox(
        "EVU wählen",
        list(EVU.keys())
    )
    CO2Emmisionen = EVU[EVU_name]
    CO2Emmisionen_input = st.number_input(
        "CO2 Emmisionen in kg CO2e/MWh der vom EVU bezogenen Elektrizität",
        value=int(CO2Emmisionen)
    )
    ergebnis = CO2Emmisionen
    strompreis_rp_kWh = strompreis_mapping[Strompreis]
    strompreis_chf_kWh = strompreis_rp_kWh / 100

st.write("------------------------------")
st.subheader("Kostenannahmen")

col1, col2, col3 = st.columns(3)

with col1:
    kostenmodus_pv = st.radio(
        "Wie sollen die PV-Investitionskosten angegeben werden?",
        [
            "Über Richtwert berechnen",
            "Gesamtkosten manuell eingeben"
        ],
        horizontal=False
    )

    if kostenmodus_pv == "Über Richtwert berechnen":
        kosten_pv_chf_kwp = st.number_input(
            "Richtwert PV-Kosten in CHF/kWp",
            min_value=0.0,
            max_value=10000.0,
            value=2800.0,
            step=100.0,
            format="%.0f"
        )

        pv_investition_brutto = gesamt_pv_peakleistung * kosten_pv_chf_kwp

        st.caption(
            "Der Richtwert wird mit der installierten PV-Leistung multipliziert. "
            "Falls eine konkrete Offerte vorliegt, können stattdessen die Gesamtkosten manuell eingegeben werden."
        )

    else:
        pv_investition_brutto = st.number_input(
            "PV-Investition total in CHF",
            min_value=0.0,
            max_value=500000.0,
            value=float(gesamt_pv_peakleistung * 2800),
            step=1000.0,
            format="%.0f"
        )

        if gesamt_pv_peakleistung > 0:
            kosten_pv_chf_kwp = pv_investition_brutto / gesamt_pv_peakleistung
        else:
            kosten_pv_chf_kwp = 0.0

    st.info(
        f"Verwendete PV-Investition: {pv_investition_brutto:,.0f} CHF "
        f"bei {gesamt_pv_peakleistung:.1f} kWp "
        f"({kosten_pv_chf_kwp:,.0f} CHF/kWp).".replace(",", "'")
    )

    foerderanteil_pv_prozent = st.slider(
        "Förderanteil PV-Investition in %",
        min_value=0,
        max_value=30,
        value=30,
        step=1
    )

    st.caption(
        "Die Förderung wird vereinfacht als prozentualer Anteil der PV-Investition berücksichtigt."
    )

with col2:
    if batterie_aktiv and batteriekapazität > 0:
        batteriekosten_chf = st.number_input(
            "Batteriespeicher-Investition total in CHF",
            min_value=0.0,
            max_value=100000.0,
            value=6500.0,
            step=500.0,
            format="%.0f"
        )
    else:
        batteriekosten_chf = 0.0
        st.caption("Keine Batterie aktiv, daher keine Batterie-Investition.")

    optimierungskosten_chf = st.number_input(
        "Zusatzkosten für Energiemanagement / Steuerung in CHF",
        min_value=0.0,
        max_value=50000.0,
        value=0.0,
        step=500.0,
        format="%.0f"
    )
    st.caption(
        "Optionale Zusatzkosten für eine Steuerung, die z. B. Batterie, Boiler oder E-Auto "
        "PV-optimiert betreibt. Falls keine separate Steuerung berücksichtigt werden soll, 0 CHF eingeben."
    )

with col3:
    ruecklieferverguetung_rp_kWh = st.number_input(
        "Rückliefervergütung in Rp./kWh",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.5,
        format="%.1f"
    )

    ruecklieferverguetung_chf_kWh = ruecklieferverguetung_rp_kWh / 100

    betriebskosten_prozent = st.number_input(
        "Laufende Kosten pro Jahr in % der Investition",
        min_value=0.0,
        max_value=10.0,
        value=1.0,
        step=0.1,
        format="%.1f"
    )

    betrachtungsdauer_jahre = st.number_input(
        "Betrachtungsdauer Kostenrechnung in Jahren",
        min_value=1,
        max_value=50,
        value=LebenszeitJahre["PV"],
        step=1
    )
    kostenbestandteile = [
        "PV-Anlage",
        "Wechselrichter",
        "Unterkonstruktion",
        "Montage",
        "elektrische Installation",
        "Planung und Inbetriebnahme"
    ]

    if batterie_aktiv and batteriekapazität > 0:
        kostenbestandteile.append("Batteriespeicher")

    if optimierungskosten_chf > 0:
        kostenbestandteile.append("Energiemanagement / Steuerung")

    st.caption(
        "Die Kostenabschätzung berücksichtigt: "
        + ", ".join(kostenbestandteile)
        + ". Zusätzlich werden Förderung, laufende Betriebskosten, Strombezugskosten "
        "und Einspeiseerlöse berücksichtigt."
    )

st.write("------------------------------")
st.subheader("Test Zeitreihe")
run_simulation = st.button("Simulation starten")

if run_simulation:
    for key in ["df_ts", "monatsbilanz", "jahreskennzahlen", "df_umwelt"]:
        st.session_state.pop(key, None)
    simulation_inputs = {
        "jahresstromverbrauch": float(jahresstromverbrauch),
        "heizwaermebedarf": float(Heizwaermebedarf_input),
        "heizsystem": heizsystem,
        "jaz": float(jaz),
        "ww_aktiv": bool(ww_aktiv),
        "ww_bedarf_kWh_tag": float(ww_bedarf_kWh_tag),
        "ev_aktiv": bool(ev_aktiv),
        "batteriekapazität": float(batteriekapazität),
        "maxLadeleistungBatterie": float(maxLadeleistungBatterie),
        "maxEntladeleistungBatterie": float(maxEntladeleistungBatterie),
        "einspeisegrenze_kw": float(EinspeisegrenzekW),
        "bezugsgrenze_kw": float(Bezugsgrenze),
        "pv_anlagen_daten": copy.deepcopy(pv_anlagen_daten),
        "prioritaeten": prioritaeten.copy(),
        "kostenmodus_pv": kostenmodus_pv,
        "pv_investition_brutto": float(pv_investition_brutto),
        "kosten_pv_chf_kwp": float(kosten_pv_chf_kwp),
        "batteriekosten_chf": float(batteriekosten_chf),
        "optimierungskosten_chf": float(optimierungskosten_chf),
        "foerderanteil_pv_prozent": float(foerderanteil_pv_prozent),
        "ruecklieferverguetung_rp_kWh": float(ruecklieferverguetung_rp_kWh),
        "betriebskosten_prozent": float(betriebskosten_prozent),
        "betrachtungsdauer_jahre": int(betrachtungsdauer_jahre),
    }

    st.session_state["simulation_inputs"] = simulation_inputs
    with st.spinner("Simulation läuft... bitte warten"):

        simulationsjahr = 2025
        df_ts = create_base_dataframe(simulationsjahr)

        df_weather_raw = load_weather_data(standort_auswahl)
        df_weather = prepare_weather_for_simulation(df_weather_raw, simulationsjahr)

        # Stromprofil
        # Standardmässig wird der eingegebene Stromverbrauch als Basislast verwendet
        jahresstromverbrauch_fuer_basislast = jahresstromverbrauch

        # Für Rückrechnungsmodus: Gesamtstromrechnung auf Haushaltsstrom zurückrechnen
        if strombedarf_rueckrechnung:
            jahresstromverbrauch_fuer_basislast = max(
                0.0,
                basislast_berechnet
            )

            #st.write("Rückrechnung aus Stromrechnung:")
            #st.write(f"Gemessener Gesamtstrom: {jahresstromverbrauch:,.0f} kWh/a".replace(",", "'"))
            #st.write(f"Abzug WP-Strom Ist-Zustand: {wp_strom_ist:,.0f} kWh/a".replace(",", "'"))
            #st.write(f"Abzug Warmwasserstrom Ist-Zustand: {ww_strom_ist:,.0f} kWh/a".replace(",", "'"))
            #st.write(f"Abzug E-Auto-Strom Ist-Zustand: {ev_strom_ist:,.0f} kWh/a".replace(",", "'"))

            #st.metric(
                #"Berechneter Haushaltsstrom als Basislast",
                #f"{jahresstromverbrauch_fuer_basislast:,.0f} kWh/a".replace(",", "'")
            #)

        # Stromprofil mit Basislast erzeugen
        if Stromnutzung == "Standardprofil EFH":
            df_ts = add_slp_profile(df_ts, slp_df, jahresstromverbrauch_fuer_basislast)

        elif Stromnutzung == "Standardprofil Gewerbe (G25, nur Fallstudie)":
            df_ts = add_g25_profile(df_ts, g25_df, jahresstromverbrauch_fuer_basislast)

        elif Stromnutzung == "eigene Daten":
            if uploaded_file is not None:
                df_ts = add_uploaded_load_profile(df_ts, uploaded_file, lastprofil_einheit)
                st.write("Hochgeladener Jahresverbrauch in kWh:", round(df_ts["hauslast_kWh"].sum(), 1))

                if strombedarf_rueckrechnung:
                    faktor = jahresstromverbrauch_fuer_basislast / df_ts["hauslast_kWh"].sum()
                    df_ts["hauslast_kWh"] = df_ts["hauslast_kWh"] * faktor
                    st.write(
                        "Hochgeladenes Profil wurde auf die zurückgerechnete Basislast skaliert:",
                        round(df_ts["hauslast_kWh"].sum(), 1),
                        "kWh/a"
                    )
            else:
                st.info("Bitte eine gültige CSV-/Excel-Datei hochladen.")
                st.stop()

        # Raumheizung übernehmen (ohne Warmwasser)
        
        heizwaerme_jahr = float(Heizwaermebedarf_input)
       
        #st.write("DEBUG strombedarf_ist_gesamt:", strombedarf_ist_gesamt)

        #st.write("DEBUG Heizwärmebedarf für Simulation:", heizwaerme_jahr)

        #st.write("DEBUG JAZ:", jaz if heizsystem == "Wärmepumpe" else "keine WP")

        #st.write("DEBUG WP-Strom berechnet:", StromverbrauchWP_input if heizsystem == "Wärmepumpe" else 0)

        meta_df = load_station_metadata("SIA4028_metadata_2023.csv")
        station_info = get_station_info(meta_df, standort_auswahl, standort_dateien)


        df_ts = add_heating_profile_weather_based(
            df_ts,
            df_weather,
            heizwaerme_jahr,
            raumtemperatur,
            stationshoehe_m=station_info["altitude"],
            standorthoehe_m=Höhenmeter_standort,
            auslegetemperatur=Auslegetemperatur if heizsystem == "Wärmepumpe" else -7,
            vorlauf_auslegung=Vorlauftemperatur_Auslegung if heizsystem == "Wärmepumpe" else 40
        )


        if strombedarf_ist_gesamt:
            df_ts["wp_strom_kWh"] = 0.0
            df_ts["gesamtlast_kWh"] = df_ts["hauslast_kWh"]

        else:
            df_ts = add_heatpump_consumption(
                df_ts,
                heizsystem,
                jaz=jaz if heizsystem == "Wärmepumpe" else None,
                wp_typ=wp_typ if heizsystem == "Wärmepumpe" else None,
                wp_strom_jahr=StromverbrauchWP_input if heizsystem == "Wärmepumpe" else None
            )


        
        # st.write("Original Wetterdaten Start:", df_weather_raw.index.min())
        # st.write("Original Wetterdaten Ende:", df_weather_raw.index.max())
        # st.write("Anzahl Wetter-Zeilen:", len(df_weather_raw))

        # st.write("Simulations-Wetterdaten Start:", df_weather.index.min())
        # st.write("Simulations-Wetterdaten Ende:", df_weather.index.max())

        df_ts["pv_kWh"] = 0.0
        df_ts["pv_power_kW"] = 0.0
        df_ts["poa_global"] = 0.0
        df_ts["temp_cell"] = 0.0
        df_ts["temp_factor"] = 0.0

        for anlage in pv_anlagen_daten:
            df_tmp = add_pv_profile_weather_based(
                df_base=pd.DataFrame(index=df_ts.index),
                df_weather=df_weather,
                latitude=station_info["latitude"],
                longitude=station_info["longitude"],
                altitude=Höhenmeter_standort,
                dachneigung=anlage["Dachneigung"],
                dachausrichtung=anlage["Dachausrichtung"],
                pv_peakleistung_kwp=anlage["pv_Peakleistung"],
                wirkungsgrad_prozent=anlage["PV_Wirkungsgrad"],
                performance_ratio=anlage["performance_ratio"],
                gamma_pdc=anlage["gamma_pdc"],
                noct=anlage["nmot"]
            )

            df_ts["pv_kWh"] += df_tmp["pv_kWh"]
            df_ts["pv_power_kW"] += df_tmp["pv_power_kW"]
            df_ts["poa_global"] += df_tmp["poa_global"]
            df_ts["temp_cell"] += df_tmp["temp_cell"]
            df_ts["temp_factor"] += df_tmp["temp_factor"]

        # Korrektur anhand gemessener PV-Produktion
        pv_korrekturfaktor = 1.0

        if pv_bestehend and pv_produktion_real_mittelwert is not None:
            pv_produktion_theoretisch = df_ts["pv_kWh"].sum()

            if pv_produktion_theoretisch > 0:
                pv_korrekturfaktor = pv_produktion_real_mittelwert / pv_produktion_theoretisch

                # Sicherheitsgrenze, damit Eingabefehler nicht komplett absurde Werte erzeugen
                pv_korrekturfaktor = min(max(pv_korrekturfaktor, 0.1), 1.5)

                df_ts["pv_kWh"] = df_ts["pv_kWh"] * pv_korrekturfaktor
                df_ts["pv_power_kW"] = df_ts["pv_power_kW"] * pv_korrekturfaktor

                pv_verlust_prozent = (1 - pv_korrekturfaktor) * 100

                st.write("PV-Korrektur anhand gemessener Produktion:")
                st.write(
                    f"Theoretische PV-Produktion: {pv_produktion_theoretisch:,.0f} kWh/a".replace(",", "'")
                )
                st.write(
                    f"Gemessene PV-Produktion: {pv_produktion_real_mittelwert:,.0f} kWh/a".replace(",", "'")
                )
                st.write(
                    f"PV-Korrekturfaktor: {pv_korrekturfaktor:.3f}"
                )
                st.write(
                    f"Abweichung / zusätzlicher Verlust: {pv_verlust_prozent:.1f} %"
                )

        # Wechselrichterbegrenzung AC-seitig
        df_ts["pv_power_kW_vor_wr"] = df_ts["pv_power_kW"]

        df_ts["pv_power_kW"] = df_ts["pv_power_kW"].clip(upper=WechselrichterkW)

        df_ts["pv_kWh"] = df_ts["pv_power_kW"] * 0.25

        df_ts["wr_abregelung_kWh"] = (
            df_ts["pv_power_kW_vor_wr"] - df_ts["pv_power_kW"]
        ).clip(lower=0) * 0.25

        if strombedarf_ist_gesamt:
            ww_aktiv_sim = False
            ev_aktiv_sim = False
        else:
            ww_aktiv_sim = ww_aktiv
            ev_aktiv_sim = ev_aktiv

        ww_config = {
            "aktiv": ww_aktiv_sim,
            "steuerbar": ww_steuerbar,
            "bedarf_tag": ww_bedarf_kWh_tag,
            "leistung_kw": ww_ladeleistung_kw,
            "strategie": ww_strategie
        }

        ev_config = {
            "aktiv": ev_aktiv_sim,
            "leistung_kw": ev_ladeleistung_kw,
            "verbrauch_pro_100km": ev_verbrauch_kWh_pro_100km,
            "km_pro_fahrtag": ev_km_pro_fahrtag,
            "km_nicht_fahrtag": ev_km_nicht_fahrtag,
            "strategie": ev_strategie,
            "fahrtage": ev_fahrtage
        }

        ev_check = pruefe_ev_plausibilitaet(ev_config)

        if ev_check is not None:
            
            if not ev_check["ok"]:
                st.warning(
                    "Achtung: Der Fahrbedarf pro Fahrtag ist höher als die maximal mögliche Ladung "
                    "im gewählten Ladefenster. Das bedeutet: Der offene Ladebedarf wird über mehrere "
                    "Tage weitergeladen."
                )

        df_ts = simulate_ems(
            df_ts,
            prioritaeten,
            ww_config,
            ev_config,
            batteriekapazität,
            maxLadeleistungBatterie,
            maxEntladeleistungBatterie,
            minSoC,
            maxSoC,
            EinspeisegrenzekW,
            Bezugsgrenze,
            batterieWirkungsgrad
        )

        df_ts, monatsbilanz, jahreskennzahlen = create_energy_summary(df_ts)
        stromkosten_chf = df_ts["netzbezug_kWh"].sum() * strompreis_chf_kWh
        jahreskennzahlen["Stromkosten_CHF"] = stromkosten_chf
        eingesparte_stromkosten = (
            jahreskennzahlen["Eigenverbrauch_kWh"] * strompreis_chf_kWh
        )

        jahreskennzahlen["Eingesparte_Stromkosten_CHF"] = eingesparte_stromkosten
        kostenkennzahlen = berechne_kostenkennzahlen(
            df_ts=df_ts,
            jahreskennzahlen=jahreskennzahlen,
            pv_kwp_total=gesamt_pv_peakleistung,
            batterie_aktiv=batterie_aktiv,
            batteriekapazitaet=batteriekapazität,
            pv_investition_brutto=pv_investition_brutto,
            batteriekosten_chf=batteriekosten_chf,
            optimierungskosten_chf=optimierungskosten_chf,
            foerderanteil_pv_prozent=foerderanteil_pv_prozent,
            betriebskosten_prozent=betriebskosten_prozent,
            strompreis_chf_kWh=strompreis_chf_kWh,
            ruecklieferverguetung_chf_kWh=ruecklieferverguetung_chf_kWh,
            betrachtungsdauer_jahre=betrachtungsdauer_jahre
        )

        st.session_state["kostenkennzahlen"] = kostenkennzahlen
        
        if heizsystem != "Wärmepumpe":
            wp_typ_use = None
            WPkW_use = 0
            Erdsondentiefe_use = 0
        else:
            wp_typ_use = wp_typ
            WPkW_use = WPkW
            Erdsondentiefe_use = Erdsondentiefe if wp_typ == "Sole/Wasser WP" else 0
        ev_km_jahr = berechne_ev_jahreskilometer(ev_config)
        df_umwelt = berechne_umweltwirkung(
            df_ts=df_ts,
            pv_anlagen_daten=pv_anlagen_daten,
            wechselrichter_kw=WechselrichterkW,
            batterie_aktiv=batterie_aktiv,
            batteriekapazitaet=batteriekapazität,
            heizsystem=heizsystem,
            fossil_typ=fossil_typ if heizsystem == "Fossil & Holz" else None,
            wp_typ=wp_typ_use,
            wp_kw=WPkW_use,
            erdsondenlaenge=Erdsondentiefe_use,
            ebf_m2=EBFm2,
            auto_aktiv=auto_aktiv,
            auto_typ=auto_typ,
            auto_km_jahr=auto_km_jahr,
            ev_aktiv=ev_aktiv,
            ev_km_jahr=ev_km_jahr
        )

        st.session_state["df_umwelt"] = df_umwelt
                
        st.success("Simulation abgeschlossen ✅")

        st.session_state["df_ts"] = df_ts
        st.session_state["monatsbilanz"] = monatsbilanz
        st.session_state["jahreskennzahlen"] = jahreskennzahlen

        monatswerte = df_ts.resample("MS")[[
            "pv_kWh",
            "gesamtlast_kWh",
            "netzbezug_kWh",
            "netzeinspeisung_kWh",
            "abregelung_kWh"
        ]].sum()

        monatswerte.index = monatswerte.index.strftime("%Y-%m")

        profil = {
            "name": profil_name,
            "personen": int(personen),
            "jahresstromverbrauch": float(jahresstromverbrauch),
            "m2": float(m2),
            "bau_typ": bau_typ,
            "heizsystem": heizsystem,
            "fossil_typ": fossil_typ,
            "wp_typ": wp_typ,
            "WPkW": float(WPkW) if heizsystem == "Wärmepumpe" else 0,
            "jaz": float(jaz),
            "Erdsondentiefe": float(Erdsondentiefe),
            "ww_system": ww_system,
            "ww_bedarf_kWh_tag": float(ww_bedarf_kWh_tag),
            "ev_aktiv": bool(ev_aktiv),
            "ev_km_jahr": float(ev_km_jahr),
            "batterie_aktiv": bool(batterie_aktiv),
            "batteriekapazität": float(batteriekapazität),
            "standort": standort_auswahl,
            "pv_anlagen_daten": pv_anlagen_daten,
            "jahreskennzahlen": jahreskennzahlen,
            "df_umwelt": df_umwelt.to_dict(orient="records"),
            "monatswerte": monatswerte.to_dict(orient="index"),
            "auto_aktiv": bool(auto_aktiv),
            "auto_typ": auto_typ,
            "strompreis_rp_kWh": float(strompreis_rp_kWh),
            "stromkosten_chf": float(stromkosten_chf),
            "kostenkennzahlen": kostenkennzahlen,
            "pv_investition_brutto": float(pv_investition_brutto),
            "batteriekosten_chf": float(batteriekosten_chf),
            "optimierungskosten_chf": float(optimierungskosten_chf),
            "foerderanteil_pv_prozent": float(foerderanteil_pv_prozent),
            "ruecklieferverguetung_rp_kWh": float(ruecklieferverguetung_rp_kWh),
            "betriebskosten_prozent": float(betriebskosten_prozent),
            "betrachtungsdauer_jahre": int(betrachtungsdauer_jahre)
        }
        speichere_profil(profil_name, profil)
        st.success(f"Profil '{profil_name}' wurde gespeichert.")
        if "profile" not in st.session_state:
            st.session_state["profile"] = {}

        st.session_state["profile"][profil_name] = profil

if "df_ts" in st.session_state:
        df_ts = st.session_state["df_ts"]
        monatsbilanz = st.session_state["monatsbilanz"]
        jahreskennzahlen = st.session_state["jahreskennzahlen"]

        st.subheader("Zeitverlauf Graphik")

        zeitraum = st.selectbox(
            "Zeitraum wählen",
            ["Tag", "Woche", "Monat", "Jahr"]
        )

        if zeitraum in ["Tag", "Woche"]:
            start_datum = st.date_input(
                "Startdatum wählen",
                value=df_ts.index.min().date(),
                min_value=df_ts.index.min().date(),
                max_value=df_ts.index.max().date()
            )
            df_plot = get_display_dataframe(df_ts, zeitraum, start_datum=start_datum)

        elif zeitraum == "Monat":
            monat_namen = {
                1: "Januar", 2: "Februar", 3: "März", 4: "April",
                5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
                9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
            }

            start_monat = st.selectbox(
                "Monat wählen",
                list(monat_namen.keys()),
                format_func=lambda x: monat_namen[x]
            )
            df_plot = get_display_dataframe(df_ts, zeitraum, start_monat=start_monat)

        else:
            df_plot = get_display_dataframe(df_ts, zeitraum)

        st.write("Ausgewählter Zeitraum:")
        st.write(f"Anzahl Zeitschritte: {len(df_plot)}")

        fig = create_main_plot(df_plot, EinspeisegrenzekW, Bezugsgrenze, zeitraum)
        st.plotly_chart(fig, use_container_width=True)
        
        fig_weather = create_weather_plot(df_plot)
        st.plotly_chart(fig_weather, use_container_width=True)


        if zeitraum in ["Tag", "Woche"]:
            df_sum = get_raw_period_dataframe(df_ts, zeitraum, start_datum=start_datum)

        elif zeitraum == "Monat":
            df_sum = get_raw_period_dataframe(df_ts, zeitraum, start_monat=start_monat)

        else:
            df_sum = get_raw_period_dataframe(df_ts, zeitraum)

        # Maximale Einspeiseleistung im ausgewählten Zeitraum
        max_einspeiseleistung_kw = df_sum["netzeinspeisung_kWh"].max() / 0.25

        if zeitraum == "Tag":
            titel = "Zusammenfassung des ausgewählten Tages"
        elif zeitraum == "Woche":
            titel = "Zusammenfassung der ausgewählten Woche"
        elif zeitraum == "Monat":
            titel = "Zusammenfassung des ausgewählten Monats"
        else:
            titel = "Zusammenfassung des gesamten Jahres"

        st.subheader(titel)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("PV-Produktion", f"{df_sum['pv_kWh'].sum():,.1f} kWh".replace(",", "'"))
            st.metric("Gesamtlast", f"{df_sum['gesamtlast_kWh'].sum():,.1f} kWh".replace(",", "'"))

        with col2:
            st.metric("Netzbezug", f"{df_sum['netzbezug_kWh'].sum():,.1f} kWh".replace(",", "'"))
            st.metric("Netzeinspeisung", f"{df_sum['netzeinspeisung_kWh'].sum():,.1f} kWh".replace(",", "'"))

        with col3:
            st.metric("Abregelung", f"{df_sum['abregelung_kWh'].sum():,.1f} kWh".replace(",", "'"))
            st.metric("Unterdeckung", f"{df_sum['unterdeckung_kWh'].sum():,.1f} kWh".replace(",", "'"))
            st.metric("Max. Einspeiseleistung", f"{max_einspeiseleistung_kw:,.2f} kW".replace(",", "'"))

        with st.expander("Daten im ausgewählten Zeitraum anzeigen"):
            st.dataframe(
                df_plot[[
                    "gesamtlast_kWh",
                    "pv_kWh",
                    "ww_kWh",
                    "ev_kWh",
                    "soc_kWh",
                    "netzbezug_kWh",
                    "netzeinspeisung_kWh",
                    "abregelung_kWh",
                    "unterdeckung_kWh"
                ]].round(3)
            )

        st.write("------------------------------")
        st.subheader("Jahreskennzahlen")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            
            autarkie = jahreskennzahlen["Autarkiegrad_%"]

            farbe = autarkie_farbe(autarkie)

            st.markdown(
                f"""
                <div style="text-align:center">
                    <div style="font-size:18px;">
                        Autarkiegrad
                    </div>
                    <div style="
                        font-size:48px;
                        font-weight:bold;
                        color:{farbe};
                    ">
                        {autarkie:,.1f} %
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.metric("Eigenverbrauchsquote", f"{jahreskennzahlen['Eigenverbrauchsquote_%']:,.1f} %".replace(",", "'"))

        with col3:
            st.metric("Abgeregelte Energie", f"{jahreskennzahlen['Abgeregelte_Energie_kWh']:,.1f} kWh".replace(",", "'"))
            if jahreskennzahlen["Abgeregelte_Energie_kWh"] > 0:
                st.info(
                    f"Im Jahresverlauf wurden insgesamt {jahreskennzahlen['Abgeregelte_Energie_kWh']:,.1f} kWh aufgrund der "
                    f"Einspeisebegrenzung abgeregelt."
                )
            else:
                st.success(
                    "Die Abregelung tritt nur auf, wenn der PV-Überschuss nach Eigenverbrauch und Batterieladung " \
                    "die Einspeisegrenze überschreitet. Die Einspeisegrenze beträgt hier "
                    f"{EinspeisegrenzekW:.2f} kW. Da die maximale PV-Leistung bei "
                    f"{df_ts['pv_power_kW'].max():.2f} kW liegt und zusätzlich ein Teil direkt verbraucht oder gespeichert wird, "
                    "entsteht in diesem Szenario keine Abregelung."
                )
        with col4:
            st.metric(
                "Vermiedene Bezugskosten",
                f"{jahreskennzahlen['Eingesparte_Stromkosten_CHF']:,.0f} CHF/a".replace(",", "'")
            )
            st.caption(
                "Entspricht den vermiedenen Strombezugskosten durch direkt genutzten PV-Strom. "
                "Einspeisevergütung, Betriebskosten und Investitionskosten werden unten in der Kostenabschätzung berücksichtigt."
            )
        with col5:
            st.metric(
                "PV-Jahresproduktion",
                f"{jahreskennzahlen['PV_Produktion_kWh']:,.0f} kWh/a".replace(",", "'")
            )

        if "kostenkennzahlen" in st.session_state:
            kostenkennzahlen = st.session_state["kostenkennzahlen"]

            st.write("------------------------------")
            st.subheader("Kostenabschätzung")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Investition brutto",
                    f"{kostenkennzahlen['Investition brutto CHF']:,.0f} CHF".replace(",", "'")
                )
                st.metric(
                    "Förderung",
                    f"{kostenkennzahlen['Förderung CHF']:,.0f} CHF".replace(",", "'")
                )
                st.metric(
                    "Investition netto",
                    f"{kostenkennzahlen['Investition netto CHF']:,.0f} CHF".replace(",", "'")
                )

            with col2:
                st.metric(
                    "Stromkosten ohne PV",
                    f"{kostenkennzahlen['Stromkosten ohne PV CHF/a']:,.0f} CHF/a".replace(",", "'")
                )
                st.metric(
                    "Stromkosten mit PV",
                    f"{kostenkennzahlen['Stromkosten mit PV inkl. Betrieb CHF/a']:,.0f} CHF/a".replace(",", "'")
                )
                st.metric(
                    "Jährlicher Kostenvorteil",
                    f"{kostenkennzahlen['Jährlicher Kostenvorteil CHF/a']:,.0f} CHF/a".replace(",", "'")
                )

            with col3:
                amortisation = kostenkennzahlen["Amortisationszeit Jahre"]

                if np.isnan(amortisation):
                    amortisation_text = "nicht berechenbar"
                else:
                    amortisation_text = f"{amortisation:,.1f} Jahre".replace(",", "'")

                st.metric(
                    "Amortisationszeit",
                    amortisation_text
                )

                st.metric(
                    "Stromgestehungskosten",
                    f"{kostenkennzahlen['Stromgestehungskosten Rp/kWh']:,.1f} Rp./kWh".replace(",", "'")
                )

                st.metric(
                    "Betriebskosten",
                    f"{kostenkennzahlen['Betriebskosten CHF/a']:,.0f} CHF/a".replace(",", "'")
                )

            with st.expander("Details der Kostenrechnung anzeigen"):
                df_kosten = pd.DataFrame(
                    list(kostenkennzahlen.items()),
                    columns=["Kennzahl", "Wert"]
                )

                df_kosten["Wert"] = df_kosten["Wert"].apply(
                    lambda x: f"{x:,.2f}".replace(",", "'") if isinstance(x, (int, float, np.number)) and not pd.isna(x) else x
                )

                st.dataframe(df_kosten, use_container_width=True)

            st.caption(
                "Die Kostenabschätzung vergleicht die jährlichen Stromkosten ohne PV-Anlage mit den "
                "Stromkosten bei PV-Nutzung. Berücksichtigt werden Netzbezugskosten, Einspeiseerlöse, "
                "Investitionskosten, Förderung und laufende Betriebskosten. Die Berechnung stellt eine "
                "vereinfachte Abschätzung dar und ersetzt keine detaillierte Wirtschaftlichkeitsanalyse."
            )


        st.write("---------------------")

        col1, col2 =st.columns(2)

        with col1:

            df_year_plot = df_ts["gesamtlast_kWh"].resample("MS").sum().to_frame()
            df_year_plot = df_year_plot.rename(columns={"gesamtlast_kWh": "monatslast_kWh"})
            fig_year = go.Figure()
            fig_year.add_trace(go.Bar(
                x=df_year_plot.index,
                y=df_year_plot["monatslast_kWh"],
                name="Gesamtlast"
            ))
            fig_year.update_layout(
                title="Monatliche Gesamtlast Strom (kWh/Monat)",
                xaxis_title="Monat",
                yaxis_title="Elektrische Gesamtlast in kWh pro Monat",
                height=450
            )
            fig_year.update_xaxes(
                tickformat="%b",
                dtick="M1"
            )
            fig_year.update_yaxes(rangemode="tozero")

            st.plotly_chart(fig_year, use_container_width=True)
            
            st.write("PV-Produktion Jahreswert in kWh/Jahr:", round(df_ts["pv_kWh"].sum(), 1))
            st.write("PV-Leistung Maximum in kW:", round(df_ts["pv_power_kW"].max(), 2))
            st.write("Netzeinspeisung Jahreswert in kWh/Jahr:", round(df_ts["netzeinspeisung_kWh"].sum(), 1))
            st.write("Jahresstrombedarf in kWh:", round(df_ts["gesamtlast_kWh"].sum(), 1))
            pv_monat = df_ts["pv_kWh"].resample("MS").sum()

        with col2: 
            fig_pv_monat = go.Figure()
            fig_pv_monat.add_trace(go.Bar(
                x=pv_monat.index,
                y=pv_monat,
                name="PV-Produktion"
            ))

            fig_pv_monat.update_layout(
                title="Monatliche PV-Produktion",
                xaxis_title="Monat",
                yaxis_title="PV-Produktion in kWh pro Monat",
                height=450
            )

            fig_pv_monat.update_xaxes(
                tickformat="%b",
                dtick="M1"
            )

            fig_pv_monat.update_yaxes(rangemode="tozero")

            st.plotly_chart(fig_pv_monat, use_container_width=True)

        df_umwelt = st.session_state["df_umwelt"]

        st.write("------------------------------")
        st.subheader("Umweltwirkungen")

        total_ubp = df_umwelt["UBP/a"].sum()
        total_co2 = df_umwelt["kg CO2-eq/a"].sum()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total UBP pro Jahr", f"{total_ubp:,.0f} UBP/a".replace(",", "'"))

        with col2:
            st.metric("Total Treibhausgasemissionen", f"{total_co2:,.0f} kg CO₂-eq/a".replace(",", "'"))

        st.caption(
            "Die Umweltwirkungen der Herstellung werden als jährlicher Anteil über die angenommene "
            "Lebensdauer der Komponenten dargestellt. Betriebsemissionen, z. B. Netzstrom Betrieb, "
            "werden dagegen aus dem effektiv simulierten jährlichen Energiebezug berechnet."
        )
        pv_herstellung_mask = df_umwelt["Kategorie"].str.contains(
            "PV-Anlage|Wechselrichter|Elektroinstallation PV",
            regex=True
        )

        pv_system_co2_a = df_umwelt.loc[
            pv_herstellung_mask,
            "kg CO2-eq/a"
        ].sum()

        pv_produktion_kWh_a = jahreskennzahlen["PV_Produktion_kWh"]

        if pv_produktion_kWh_a > 0:
            pv_co2_kg_kWh = pv_system_co2_a / pv_produktion_kWh_a
        else:
            pv_co2_kg_kWh = np.nan

        netz_co2_kg_kWh = CO2Emmisionen_input / 1000

        st.write("**CO₂-Referenzwerte pro kWh elektrische Energie**")

        col_ref1, col_ref2 = st.columns(2)

        with col_ref1:
            st.metric(
                "PV-Strom, Herstellung anteilig",
                f"{pv_co2_kg_kWh:.3f} kg CO₂-eq/kWh"
            )

        with col_ref2:
            st.metric(
                "Netzstrom Betrieb",
                f"{netz_co2_kg_kWh:.3f} kg CO₂-eq/kWh"
            )

        st.caption(
            "Der PV-Referenzwert berücksichtigt die auf die Lebensdauer verteilte Herstellung "
            "der PV-Anlage inklusive Wechselrichter und Elektroinstallation, bezogen auf die "
            "jährliche PV-Produktion. Der Netzstromwert entspricht dem eingegebenen CO₂-Faktor "
            "des gewählten Energieversorgers."
        )
        col1, col2 = st.columns(2)

        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write("**Treibhausgasemissionen**")
            st.write("")
            df_umwelt_anzeige = df_umwelt.copy()

            df_umwelt_anzeige["Kategorie"] = df_umwelt_anzeige["Kategorie"].apply(
                lambda x: x + ", anteilig pro Jahr" if "Herstellung" in x else x
            )

            df_umwelt_anzeige["Kategorie"] = df_umwelt_anzeige["Kategorie"].replace({
                "Elektroinstallation PV": "Elektroinstallation PV, anteilig pro Jahr",
                "Netzstrom Betrieb": "Netzstrom Betrieb, effektiv pro Jahr"
            })

            df_umwelt_anzeige["UBP/a"] = df_umwelt_anzeige["UBP/a"].map(
                lambda x: f"{x:,.0f}".replace(",", "'")
            )

            df_umwelt_anzeige["kg CO2-eq/a"] = df_umwelt_anzeige["kg CO2-eq/a"].map(
                lambda x: f"{x:,.0f}".replace(",", "'")
            )

            st.dataframe(df_umwelt_anzeige, use_container_width=True)
            st.caption(
                    "* Netzstrom Betrieb bezeichnet die Umweltwirkung des Stroms, "
                    "der während des Betriebs aus dem öffentlichen Stromnetz bezogen wird. "
                    "Die Berechnung erfolgt über den jährlichen Netzbezug und den CO₂-Faktor "
                    "des gewählten Energieversorgers."
                )
        with col2:
            fig_umwelt = go.Figure()

            fig_umwelt.add_trace(go.Bar(
                x=df_umwelt_anzeige["Kategorie"],
                y=df_umwelt["kg CO2-eq/a"],
                name="kg CO₂-eq/a"
            ))

            fig_umwelt.update_layout(
                title="Treibhausgasemissionen nach Kategorie",
                xaxis_title="Kategorie",
                yaxis_title="kg CO₂-eq pro Jahr",
                height=500
            )

            st.plotly_chart(fig_umwelt, use_container_width=True)

        csv = df_ts.to_csv().encode("utf-8")
        st.download_button(
            label="Zeitreihe als CSV herunterladen",
            data=csv,
            file_name=f"{profil_name}_zeitreihe.csv",
            mime="text/csv"
        )        
        csv_umwelt = df_umwelt.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Umweltwirkungen als CSV herunterladen",
            data=csv_umwelt,
            file_name=f"{profil_name}_umweltwirkungen.csv",
            mime="text/csv"
        )
        idx_max = df_ts["pv_power_kW"].idxmax()    
        pdf_buffer = create_values_pdf(jahreskennzahlen, df_umwelt, df_ts)
        st.download_button(
            label="Alle Kennzahlen als PDF herunterladen",
            data=pdf_buffer,
            file_name=f"{profil_name}_kennzahlen.pdf",
            mime="application/pdf"
        )
        st.write("------------------------------")
        st.subheader("Grafische Darstellung der Parameterstudien")


        # ============================================================
        # Tabelle 9
        # ============================================================

        st.write("### Tabelle 9: Reduktion des Abregelungsverlusts durch Einspeisegrenze, Batteriekapazität und EMS-Strategie")

        df_t9 = pd.DataFrame({
            "Fall": ["Fall 0", "Fall 1", "Fall 2", "Fall 3", "Fall 4", "Fall 5", "Fall 6", "Fall 7"],
            "PV-Produktion kWh/a": [14564, 17305, 17305, 17305, 17305, 17305, 17305, 17305],
            "Strombedarf kWh/a": [14639, 14639, 14639, 14639, 14639, 14639, 14639, 14639],
            "Eigenverbrauchsquote %": [49.3, 41.9, 41.9, 41.9, 49.7, 53.8, 39.7, 47.4],
            "Autarkiegrad %": [48.2, 48.6, 48.6, 48.6, 57.3, 62.0, 46.0, 54.7],
            "Netzbezug kWh/a": [7579, 7529, 7529, 7529, 6247, 5565, 7900, 6628],
            "Netzeinspeisung kWh/a": [7377, 10058, 10058, 9315, 8063, 7414, 9698, 8454],
            "Maximale Netzeinspeisung kW": [9.2, 9.44, 9.44, 7.7, 7.7, 7.7, 7.7, 7.7],
            "Abregelung kWh/a": [0, 0, 0, 744, 649, 578, 744, 649],
        })

        fig_t9_abregelung = go.Figure()

        fig_t9_abregelung.add_trace(go.Bar(
            x=df_t9["Fall"],
            y=df_t9["Abregelung kWh/a"],
            name="Abregelung"
        ))

        fig_t9_abregelung.update_layout(
            title="Tabelle 9: Abregelung je Fall",
            xaxis_title="Fall",
            yaxis_title="Abregelung in kWh/a",
            height=450,
            yaxis=dict(
                tickmode="array",
                tickvals=[0, 100, 200, 300, 400, 500, 600, 700, 800],
                range=[0, 800]
            )
        )

        st.plotly_chart(fig_t9_abregelung, use_container_width=True)


        fig_t9_anteile = go.Figure()

        fig_t9_anteile.add_trace(go.Bar(
            x=df_t9["Fall"],
            y=df_t9["Autarkiegrad %"],
            name="Autarkiegrad"
        ))

        fig_t9_anteile.add_trace(go.Bar(
            x=df_t9["Fall"],
            y=df_t9["Eigenverbrauchsquote %"],
            name="Eigenverbrauchsquote"
        ))

        fig_t9_anteile.update_layout(
            title="Tabelle 9: Autarkiegrad und Eigenverbrauchsquote je Fall",
            xaxis_title="Fall",
            yaxis_title="Anteil in %",
            barmode="group",
            height=450,
            yaxis=dict(range=[0, 70])
        )

        st.plotly_chart(fig_t9_anteile, use_container_width=True)


        fig_t9_energie = go.Figure()

        fig_t9_energie.add_trace(go.Bar(
            x=df_t9["Fall"],
            y=df_t9["Netzbezug kWh/a"],
            name="Netzbezug"
        ))

        fig_t9_energie.add_trace(go.Bar(
            x=df_t9["Fall"],
            y=df_t9["Netzeinspeisung kWh/a"],
            name="Netzeinspeisung"
        ))

        fig_t9_energie.update_layout(
            title="Tabelle 9: Netzbezug und Netzeinspeisung je Fall",
            xaxis_title="Fall",
            yaxis_title="Energie in kWh/a",
            barmode="group",
            height=450
        )

        st.plotly_chart(fig_t9_energie, use_container_width=True)


        # ============================================================
        # Tabelle 11
        # ============================================================

        st.write("### Tabelle 11: Einfluss von verschiedenen EMS-Fällen")

        df_t11 = pd.DataFrame({
            "Fall": ["Fall 0", "Fall 1", "Fall 2", "Fall 3", "Fall 4", "Fall 5", "Fall 6"],
            "Strombedarf kWh/a": [14639, 14639, 14639, 14639, 14639, 14639, 14639],
            "Eigenverbrauchsquote %": [49.3, 49.2, 48.3, 52.4, 49.3, 49.2, 49.3],
            "Autarkiegrad %": [48.2, 48.1, 47.2, 51.3, 48.2, 48.1, 48.2],
            "Netzbezug kWh/a": [7579, 7601, 7730, 7127, 7582, 7605, 7579],
            "Netzeinspeisung kWh/a": [7377, 7394, 7531, 6934, 7378, 7397, 7377],
            "Maximale Netzeinspeisung kW": [9.2, 9.2, 9.2, 9.2, 9.2, 9.2, 9.2],
        })

        fig_t11_anteile = go.Figure()

        fig_t11_anteile.add_trace(go.Bar(
            x=df_t11["Fall"],
            y=df_t11["Autarkiegrad %"],
            name="Autarkiegrad"
        ))

        fig_t11_anteile.add_trace(go.Bar(
            x=df_t11["Fall"],
            y=df_t11["Eigenverbrauchsquote %"],
            name="Eigenverbrauchsquote"
        ))

        fig_t11_anteile.update_layout(
            title="Tabelle 11: Einfluss der EMS-Fälle auf Autarkiegrad und Eigenverbrauchsquote",
            xaxis_title="EMS-Fall",
            yaxis_title="Anteil in %",
            barmode="group",
            height=450,
            yaxis=dict(range=[0, 60])
        )

        st.plotly_chart(fig_t11_anteile, use_container_width=True)


        fig_t11_energie = go.Figure()

        fig_t11_energie.add_trace(go.Bar(
            x=df_t11["Fall"],
            y=df_t11["Netzbezug kWh/a"],
            name="Netzbezug"
        ))

        fig_t11_energie.add_trace(go.Bar(
            x=df_t11["Fall"],
            y=df_t11["Netzeinspeisung kWh/a"],
            name="Netzeinspeisung"
        ))

        fig_t11_energie.update_layout(
            title="Tabelle 11: Netzbezug und Netzeinspeisung bei verschiedenen EMS-Fällen",
            xaxis_title="EMS-Fall",
            yaxis_title="Energie in kWh/a",
            barmode="group",
            height=450
        )

        st.plotly_chart(fig_t11_energie, use_container_width=True)


        # ============================================================
        # Tabelle 12
        # ============================================================

        st.write("### Tabelle 12: Einfluss verschiedener Sanierungsszenarien auf Strombedarf, Eigenverbrauch, Autarkiegrad, Netzbezug und maximale Netzeinspeisung")

        df_t12 = pd.DataFrame({
            "Fall": ["Fall 0", "Fall 1", "Fall 2", "Fall 3"],
            "Strombedarf kWh/a": [14638.7, 12530, 13795.5, 11687.4],
            "Eigenverbrauchsquote %": [49.3, 46.9, 48.4, 45.8],
            "Autarkiegrad %": [48.2, 53.5, 50.2, 55.9],
            "Netzbezug kWh/a": [7579.2, 5832, 6875, 5149],
            "Netzeinspeisung kWh/a": [7377, 7733, 7514, 7891],
            "Maximale Netzeinspeisung kW": [9.21, 9.23, 9.22, 9.24],
        })

        fig_t12_strom = go.Figure()

        fig_t12_strom.add_trace(go.Bar(
            x=df_t12["Fall"],
            y=df_t12["Strombedarf kWh/a"],
            name="Strombedarf"
        ))

        fig_t12_strom.add_trace(go.Bar(
            x=df_t12["Fall"],
            y=df_t12["Netzbezug kWh/a"],
            name="Netzbezug"
        ))

        fig_t12_strom.update_layout(
            title="Tabelle 12: Strombedarf und Netzbezug bei Sanierungsszenarien",
            xaxis_title="Sanierungsfall",
            yaxis_title="Energie in kWh/a",
            barmode="group",
            height=450
        )

        st.plotly_chart(fig_t12_strom, use_container_width=True)


        fig_t12_anteile = go.Figure()

        fig_t12_anteile.add_trace(go.Bar(
            x=df_t12["Fall"],
            y=df_t12["Autarkiegrad %"],
            name="Autarkiegrad"
        ))

        fig_t12_anteile.add_trace(go.Bar(
            x=df_t12["Fall"],
            y=df_t12["Eigenverbrauchsquote %"],
            name="Eigenverbrauchsquote"
        ))

        fig_t12_anteile.update_layout(
            title="Tabelle 12: Autarkiegrad und Eigenverbrauchsquote bei Sanierungsszenarien",
            xaxis_title="Sanierungsfall",
            yaxis_title="Anteil in %",
            barmode="group",
            height=450,
            yaxis=dict(range=[0, 65])
        )

        st.plotly_chart(fig_t12_anteile, use_container_width=True)


        fig_t12_einspeisung = go.Figure()

        fig_t12_einspeisung.add_trace(go.Bar(
            x=df_t12["Fall"],
            y=df_t12["Netzeinspeisung kWh/a"],
            name="Netzeinspeisung"
        ))

        fig_t12_einspeisung.update_layout(
            title="Tabelle 12: Netzeinspeisung bei Sanierungsszenarien",
            xaxis_title="Sanierungsfall",
            yaxis_title="Netzeinspeisung in kWh/a",
            height=450
        )

        st.plotly_chart(fig_t12_einspeisung, use_container_width=True)


        # ============================================================
        # Tabelle 13
        # ============================================================

        st.write("### Tabelle 13: Vergleich der energetischen Kennzahlen und Umweltwirkungen zwischen dem elektrifizierten Standardszenario und Varianten mit fossiler bzw. Pellet-Heizung")

        df_t13 = pd.DataFrame({
            "Fall": ["Fall 0", "Fall 1 Gas", "Fall 1 Öl", "Fall 1 Pellets"],
            "Strombedarf kWh/a": [14639, 9064, 9064, 9064],
            "Eigenverbrauchsquote %": [49, 42, 42, 42],
            "Autarkiegrad %": [48, 65, 65, 65],
            "Netzbezug kWh/a": [7579, 3144, 3144, 3144],
            "Netzeinspeisung kWh/a": [7377, 8504, 8504, 8504],
            "Maximale Netzeinspeisung kW": [9.21, 9.26, 9.26, 9.26],
            "Total UBP/a": [2331, 7825, 11275, 4833],
            "Total kg CO2eq/a": [1144, 5875, 8256, 1595],
        })

        fig_t13_energie = go.Figure()

        fig_t13_energie.add_trace(go.Bar(
            x=df_t13["Fall"],
            y=df_t13["Strombedarf kWh/a"],
            name="Strombedarf"
        ))

        fig_t13_energie.add_trace(go.Bar(
            x=df_t13["Fall"],
            y=df_t13["Netzbezug kWh/a"],
            name="Netzbezug"
        ))

        fig_t13_energie.update_layout(
            title="Tabelle 13: Strombedarf und Netzbezug nach Heizsystem",
            xaxis_title="Fall",
            yaxis_title="Energie in kWh/a",
            barmode="group",
            height=450
        )

        st.plotly_chart(fig_t13_energie, use_container_width=True)


        fig_t13_co2 = go.Figure()

        fig_t13_co2.add_trace(go.Bar(
            x=df_t13["Fall"],
            y=df_t13["Total kg CO2eq/a"],
            name="Treibhausgasemissionen"
        ))

        fig_t13_co2.update_layout(
            title="Tabelle 13: Treibhausgasemissionen nach Heizsystem",
            xaxis_title="Fall",
            yaxis_title="kg CO₂-eq/a",
            height=450
        )

        st.plotly_chart(fig_t13_co2, use_container_width=True)


        fig_t13_ubp = go.Figure()

        fig_t13_ubp.add_trace(go.Bar(
            x=df_t13["Fall"],
            y=df_t13["Total UBP/a"],
            name="UBP"
        ))

        fig_t13_ubp.update_layout(
            title="Tabelle 13: Umweltbelastungspunkte nach Heizsystem",
            xaxis_title="Fall",
            yaxis_title="UBP/a",
            height=450
        )

        st.plotly_chart(fig_t13_ubp, use_container_width=True)


        # ============================================================
        # Tabelle 14
        # ============================================================

        st.write("### Tabelle 14: Einfluss des Fahrzeugantriebs auf Strombedarf, Eigenverbrauch, Autarkiegrad, Netzbezug, Netzeinspeisung und Umweltwirkungen bei gleichem Fahrprofil")

        df_t14 = pd.DataFrame({
            "Fall": ["Fall 0", "Fall 2 Benzin", "Fall 2 Diesel", "Fall 2 Gas"],
            "Strombedarf kWh/a": [14638.7, 13021, 13021, 13021],
            "Eigenverbrauchsquote %": [49.3, 47, 47, 47],
            "Autarkiegrad %": [48.2, 51, 51, 51],
            "Netzbezug kWh/a": [7579, 6356, 6356, 6356],
            "Netzeinspeisung kWh/a": [7377, 7779, 7779, 7779],
            "Maximale Netzeinspeisung kW": [9.21, 9.21, 9.21, 9.21],
            "Total UBP/a": [2331, 5595, 5285, 5122],
            "Total kg CO2eq/a": [1144, 2924, 2702, 2577],
        })

        fig_t14_energie = go.Figure()

        fig_t14_energie.add_trace(go.Bar(
            x=df_t14["Fall"],
            y=df_t14["Strombedarf kWh/a"],
            name="Strombedarf"
        ))

        fig_t14_energie.add_trace(go.Bar(
            x=df_t14["Fall"],
            y=df_t14["Netzbezug kWh/a"],
            name="Netzbezug"
        ))

        fig_t14_energie.update_layout(
            title="Tabelle 14: Strombedarf und Netzbezug nach Fahrzeugantrieb",
            xaxis_title="Fall",
            yaxis_title="Energie in kWh/a",
            barmode="group",
            height=450
        )

        st.plotly_chart(fig_t14_energie, use_container_width=True)


        fig_t14_co2 = go.Figure()

        fig_t14_co2.add_trace(go.Bar(
            x=df_t14["Fall"],
            y=df_t14["Total kg CO2eq/a"],
            name="Treibhausgasemissionen"
        ))

        fig_t14_co2.update_layout(
            title="Tabelle 14: Treibhausgasemissionen nach Fahrzeugantrieb",
            xaxis_title="Fall",
            yaxis_title="kg CO₂-eq/a",
            height=450
        )

        st.plotly_chart(fig_t14_co2, use_container_width=True)


        fig_t14_ubp = go.Figure()

        fig_t14_ubp.add_trace(go.Bar(
            x=df_t14["Fall"],
            y=df_t14["Total UBP/a"],
            name="UBP"
        ))

        fig_t14_ubp.update_layout(
            title="Tabelle 14: Umweltbelastungspunkte nach Fahrzeugantrieb",
            xaxis_title="Fall",
            yaxis_title="UBP/a",
            height=450
        )

        st.plotly_chart(fig_t14_ubp, use_container_width=True)


        # ============================================================
        # Tabelle 15
        # ============================================================

        st.write("### Tabelle 15: Einfluss der Batteriekapazität auf Netzbezug, betriebsbedingte CO₂-Emissionen des Netzstrombezugs und herstellungsbedingte CO₂-Emissionen der Batterie")

        df_t15 = pd.DataFrame({
            "Batterie": ["1 kWh", "9 kWh", "15 kWh", "33 kWh"],
            "Batteriekapazität kWh": [1, 9, 15, 33],
            "Netzbezug kWh/a": [9706, 7579, 6600, 5858],
            "CO2 Betrieb Netzstrom kg CO2eq/a": [116, 91, 79, 70],
            "CO2 Batterie Herstellung kg CO2eq/a": [24, 100, 166, 365],
            "CO2 total kg CO2eq/a": [1095, 1144, 1199, 1389],
        })

        fig_t15_netzbezug = go.Figure()

        fig_t15_netzbezug.add_trace(go.Scatter(
            x=df_t15["Batteriekapazität kWh"],
            y=df_t15["Netzbezug kWh/a"],
            mode="lines+markers",
            name="Netzbezug"
        ))

        fig_t15_netzbezug.update_layout(
            title="Tabelle 15: Netzbezug in Abhängigkeit der Batteriekapazität",
            xaxis_title="Batteriekapazität in kWh",
            yaxis_title="Netzbezug in kWh/a",
            height=450,
            xaxis=dict(
                tickmode="array",
                tickvals=df_t15["Batteriekapazität kWh"]
            )
        )

        st.plotly_chart(fig_t15_netzbezug, use_container_width=True)


        fig_t15_co2_stack = go.Figure()

        fig_t15_co2_stack.add_trace(go.Bar(
            x=df_t15["Batterie"],
            y=df_t15["CO2 Betrieb Netzstrom kg CO2eq/a"],
            name="CO₂ Betrieb Netzstrom"
        ))

        fig_t15_co2_stack.add_trace(go.Bar(
            x=df_t15["Batterie"],
            y=df_t15["CO2 Batterie Herstellung kg CO2eq/a"],
            name="CO₂ Batterie Herstellung"
        ))

        fig_t15_co2_stack.update_layout(
            title="Tabelle 15: CO₂-Beiträge von Netzstrombetrieb und Batterieherstellung",
            xaxis_title="Batteriekapazität",
            yaxis_title="kg CO₂-eq/a",
            barmode="stack",
            height=450
        )

        st.plotly_chart(fig_t15_co2_stack, use_container_width=True)


        fig_t15_co2_total = go.Figure()

        fig_t15_co2_total.add_trace(go.Scatter(
            x=df_t15["Batteriekapazität kWh"],
            y=df_t15["CO2 total kg CO2eq/a"],
            mode="lines+markers",
            name="CO₂ total"
        ))

        fig_t15_co2_total.update_layout(
            title="Tabelle 15: Gesamte CO₂-Emissionen in Abhängigkeit der Batteriekapazität",
            xaxis_title="Batteriekapazität in kWh",
            yaxis_title="kg CO₂-eq/a",
            height=450,
            xaxis=dict(
                tickmode="array",
                tickvals=df_t15["Batteriekapazität kWh"]
            )
        )

        st.plotly_chart(fig_t15_co2_total, use_container_width=True)