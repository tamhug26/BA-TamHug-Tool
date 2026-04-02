import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
#st.set_page_config(layout="wide")


st.write("test4")

#https://ba-tamhug-tool-j82ipmep3hfrkgr36hxv9e.streamlit.app/#dimensionierungstool

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

basis_pfad_weather = "/Users/tamara/Library/Mobile Documents/com~apple~CloudDocs/FHNW/Bachelorarbeit UT/PV Ertragsdaten"

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

#Standartlastprofile
slp_df = pd.read_excel("Standartprofil H25.xlsx")
slp_df.columns = slp_df.columns.str.strip()
slp_df["Monat"] = slp_df["Monat"].astype(int)
slp_df["Zeit"] = pd.to_datetime(slp_df["Zeit"], format="%H:%M:%S").dt.strftime("%H:%M")

#def Zeitdimension mit Dataframe
def create_base_dataframe(year=2025):
    zeitindex = pd.date_range(
        start=f"{year}-01-01 00:00",
        end=f"{year}-12-31 23:45",
        freq="15min"
    )
    df = pd.DataFrame(index=zeitindex)
    df["Monat"] = df.index.month
    df["Stunde"] = df.index.hour
    df["Tag_im_Jahr"] = df.index.dayofyear
    return df
def get_day_type(timestamp):
    if timestamp.weekday() < 5:
        return "WT"
    elif timestamp.weekday() == 5:
        return "SA"
    else:
        return "FT"
# def add_slp_profile(df, slp_df, jahresstromverbrauch):
#     df = df.copy()

#     # Zeitinfos aus dem bestehenden DatetimeIndex
#     df["Tagtyp"] = df.index.map(get_day_type)
#     df["Zeit"] = df.index.strftime("%H:%M")

#     # Excel vorbereiten
#     slp_lookup = slp_df.copy()
#     slp_lookup["Monat"] = slp_lookup["Monat"].astype(int)
#     slp_lookup["Zeit"] = slp_lookup["Zeit"].astype(str).str[:5]
#     slp_lookup = slp_lookup.set_index(["Monat", "Zeit"])

#     # Werte holen, OHNE den DatetimeIndex zu zerstören
#     df["SA"] = [slp_lookup.loc[(m, z), "SA"] for m, z in zip(df["Monat"], df["Zeit"])]
#     df["FT"] = [slp_lookup.loc[(m, z), "FT"] for m, z in zip(df["Monat"], df["Zeit"])]
#     df["WT"] = [slp_lookup.loc[(m, z), "WT"] for m, z in zip(df["Monat"], df["Zeit"])]

#     # richtigen Typtag wählen
#     df["slp_wert"] = np.where(
#         df["Tagtyp"] == "WT", df["WT"],
#         np.where(df["Tagtyp"] == "SA", df["SA"], df["FT"])
#     )

#     t = df["Tag_im_Jahr"].astype("float64")
#     dynamikfaktor = (
#         - 3.92e-10 * t**4
#         + 3.20e-7 * t**3
#         - 7.02e-5 * t**2
#         + 2.10e-3 * t
#         + 1.24
#     )
#     df["slp_dyn"] = df["slp_wert"] * dynamikfaktor

#     # auf Jahresverbrauch normieren
#     faktor_summe = df["slp_dyn"].sum()
#     df["hauslast_kWh"] = df["slp_dyn"] / faktor_summe * jahresstromverbrauch

#     return df
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
def add_heatpump_consumption(df, heizsystem, jaz=None):
    df = df.copy()
    if heizsystem == "Wärmepumpe" and jaz is not None and jaz > 0:
        df["wp_strom_kWh"] = df["heizwaerme_kWh"] / jaz
    else:
        df["wp_strom_kWh"] = 0.0
    df["gesamtlast_kWh"] = df["hauslast_kWh"] + df["wp_strom_kWh"]
    return df
def add_pv_profile(df, pv_peakleistung):
    df = df.copy()
    # Monatsfaktoren: Sommer höher, Winter tiefer
    pv_monatsfaktoren = {
        1: 0.35,
        2: 0.50,
        3: 0.80,
        4: 1.00,
        5: 1.15,
        6: 1.20,
        7: 1.20,
        8: 1.05,
        9: 0.85,
        10: 0.60,
        11: 0.35,
        12: 0.25
    }
    df["pv_monat"] = df["Monat"].map(pv_monatsfaktoren)
    # Einfaches Tagesprofil: nachts 0, mittags Peak
    def pv_stundenfaktor(stunde):
        if 0 <= stunde <= 5:
            return 0.0
        elif stunde == 6:
            return 0.08
        elif stunde == 7:
            return 0.20
        elif stunde == 8:
            return 0.40
        elif stunde == 9:
            return 0.60
        elif stunde == 10:
            return 0.78
        elif stunde == 11:
            return 0.92
        elif stunde == 12:
            return 1.00
        elif stunde == 13:
            return 0.95
        elif stunde == 14:
            return 0.82
        elif stunde == 15:
            return 0.62
        elif stunde == 16:
            return 0.42
        elif stunde == 17:
            return 0.22
        elif stunde == 18:
            return 0.08
        else:
            return 0.0
    df["pv_stunde"] = df["Stunde"].apply(pv_stundenfaktor)
    df["pv_faktor"] = df["pv_monat"] * df["pv_stunde"]
    # grobe Annahme: 1 kWp ≈ 1000 kWh/a
    pv_jahresertrag = pv_peakleistung * 1000
    faktor_summe = df["pv_faktor"].sum()
    if faktor_summe > 0:
        df["pv_kWh"] = df["pv_faktor"] / faktor_summe * pv_jahresertrag
    else:
        df["pv_kWh"] = 0.0
    return df
def simulate_battery(
    df,
    batteriekapazitaet,
    max_ladeleistung,
    max_entladeleistung,
    min_soc_prozent,
    max_soc_prozent,
    einspeisegrenze_kw,
    bezugsgrenze_kw
):
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
        direktverbrauch = min(pv, last)

        pv_ueberschuss = pv - direktverbrauch
        restlast = last - direktverbrauch

        # 2) Batterie laden bei PV-Überschuss
        freie_kapazitaet = soc_max - soc
        batterie_ladung = min(pv_ueberschuss, max_ladeleistung, freie_kapazitaet)
        soc += batterie_ladung

        rest_pv_nach_batterie = pv_ueberschuss - batterie_ladung

        # 3) Einspeisen bis Grenze, Rest abregeln
        netzeinspeisung = min(rest_pv_nach_batterie, einspeisegrenze_kw)
        abregelung = max(0.0, rest_pv_nach_batterie - netzeinspeisung)

        # 4) Batterie entladen bei Restlast
        verfuegbar_batterie = soc - soc_min
        batterie_entladung = min(restlast, max_entladeleistung, verfuegbar_batterie)
        soc -= batterie_entladung

        restlast_nach_batterie = restlast - batterie_entladung

        # 5) Netzbezug bis Grenze, Rest = Unterdeckung
        netzbezug = min(restlast_nach_batterie, bezugsgrenze_kw)
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

    # Sicherheit: keine negativen Rundungsreste
    df["eigenverbrauch_kWh"] = df["eigenverbrauch_kWh"].clip(lower=0)

    # Monatsbilanz
    monatsbilanz = df.groupby("Monat")[[
        "pv_kWh",
        "eigenverbrauch_kWh",
        "netzeinspeisung_kWh",
        "netzbezug_kWh"
    ]].sum()

    monatsbilanz = monatsbilanz.rename(columns={
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
def get_display_dataframe(df, zeitraum, start_datum=None, start_monat=None):
    df = df.copy()

    if zeitraum == "Tag":
        if start_datum is None:
            start_datum = df.index.min().date()
        start = pd.Timestamp(start_datum)
        ende = start + pd.Timedelta(days=1)
        df_anzeige = df[(df.index >= start) & (df.index < ende)]

    elif zeitraum == "Woche":
        if start_datum is None:
            start_datum = df.index.min().date()
        start = pd.Timestamp(start_datum)
        ende = start + pd.Timedelta(days=7)
        df_anzeige = df[(df.index >= start) & (df.index < ende)]

    elif zeitraum == "Monat":
        if start_monat is None:
            start_monat = 1
        df_anzeige = df[df.index.month == start_monat]

    elif zeitraum == "Jahr":
        df_anzeige = df.copy()

    else:
        df_anzeige = df.copy()

    return df_anzeige
def create_main_plot(df_plot, einspeisegrenze_kw, bezugsgrenze_kw):
    fig = go.Figure()

    # PV-Produktion
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["pv_kWh"],
        mode="lines",
        name="PV-Produktion",
        line=dict(color="gold", width=2)
    ))

    # Gesamtlast
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["gesamtlast_kWh"],
        mode="lines",
        name="Hausverbrauch / Gesamtlast",
        line=dict(color="blue", width=2)
    ))

    # SoC
    # fig.add_trace(go.Scatter(
    #     x=df_plot.index,
    #     y=df_plot["soc_kWh"],
    #     mode="lines",
    #     name="Batterie-SoC",
    #     line=dict(color="green", width=2),
    #     yaxis="y2"
    # ))

    # Netzbezug
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["netzbezug_kWh"],
        mode="lines",
        name="Netzbezug",
        line=dict(color="orange", width=2)
    ))

    # Netzeinspeisung
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot["netzeinspeisung_kWh"],
        mode="lines",
        name="Netzeinspeisung",
        line=dict(color="purple", width=2)
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
    df_abregelung = df_plot[df_plot["abregelung_kWh"] > 0]
    if not df_abregelung.empty:
        fig.add_trace(go.Scatter(
            x=df_abregelung.index,
            y=df_abregelung["netzeinspeisung_kWh"] + df_abregelung["abregelung_kWh"],
            mode="markers",
            name="Abregelung",
            marker=dict(color="red", size=8, symbol="x")
        ))

    # Unterdeckung rot markieren
    df_unterdeckung = df_plot[df_plot["unterdeckung_kWh"] > 0]
    if not df_unterdeckung.empty:
        fig.add_trace(go.Scatter(
            x=df_unterdeckung.index,
            y=df_unterdeckung["gesamtlast_kWh"],
            mode="markers",
            name="Unterdeckung",
            marker=dict(color="darkred", size=8, symbol="circle-open")
        ))

    fig.update_layout(
        title="Zeitverlauf von PV, Last, Batterie und Netz",
        xaxis_title="Zeit",
        yaxis_title="Energie [kWh pro 15 min]",
        # yaxis2=dict(
        #     title="SoC Batterie [kWh]",
        #     overlaying="y",
        #     side="right"
        # ),
        legend=dict(orientation="h", y=-0.2),
        height=600,
        margin=dict(l=40, r=40, t=60, b=80)
    )

    return fig
def load_weather_data(standort_name):
    dateiname = standort_dateien[standort_name]
    dateipfad = f"{basis_pfad_weather}/{dateiname}"

    df_weather = pd.read_csv(dateipfad)

    df_weather["timestamp"] = pd.to_datetime(
        dict(
            year=df_weather["time.yy"],
            month=df_weather["time.mm"],
            day=df_weather["time.dd"],
            hour=df_weather["time.hh"]
        )
    )

    df_weather = df_weather.set_index("timestamp")
    return df_weather


st.header("Dimensionierungstool")

EBFm2 = st.number_input("Energiebezugsfläche bzw m2", 50, 5000, 200)
standort_auswahl = st.selectbox(
    "Standort wählen",
    list(Standort.keys())
) 
jahresstromverbrauch = st.number_input("Jahresstrombedarf total(kWh/a)", 1000, 10000, 4500)
Stromnutzung = st.segmented_control(
    f"Standartstromnutzungsprofil oder eigene daten als csv?",
    ["Standartprofil", "eigene Daten als csv"],
    default="Standartprofil",
    key=f"Stromnutzung"
)
if Stromnutzung == "Standartprofil":
    def add_slp_profile(df, slp_df, jahresstromverbrauch):
        df = df.copy()

        # Zeitinfos aus dem bestehenden DatetimeIndex
        df["Tagtyp"] = df.index.map(get_day_type)
        df["Zeit"] = df.index.strftime("%H:%M")

        # Excel vorbereiten
        slp_lookup = slp_df.copy()
        slp_lookup["Monat"] = slp_lookup["Monat"].astype(int)
        slp_lookup["Zeit"] = slp_lookup["Zeit"].astype(str).str[:5]
        slp_lookup = slp_lookup.set_index(["Monat", "Zeit"])

        # Werte holen, OHNE den DatetimeIndex zu zerstören
        df["SA"] = [slp_lookup.loc[(m, z), "SA"] for m, z in zip(df["Monat"], df["Zeit"])]
        df["FT"] = [slp_lookup.loc[(m, z), "FT"] for m, z in zip(df["Monat"], df["Zeit"])]
        df["WT"] = [slp_lookup.loc[(m, z), "WT"] for m, z in zip(df["Monat"], df["Zeit"])]
        
        # richtigen Typtag wählen
        df["slp_wert"] = np.where(
            df["Tagtyp"] == "WT", df["WT"],
            np.where(df["Tagtyp"] == "SA", df["SA"], df["FT"])
        )

        t = df["Tag_im_Jahr"].astype("float64")
        dynamikfaktor = (
            - 3.92e-10 * t**4
            + 3.20e-7 * t**3
            - 7.02e-5 * t**2
            + 2.10e-3 * t
            + 1.24
        )
        df["slp_dyn"] = df["slp_wert"] * dynamikfaktor

        # auf Jahresverbrauch normieren
        faktor_summe = df["slp_dyn"].sum()
        df["hauslast_kWh"] = df["slp_dyn"] / faktor_summe * jahresstromverbrauch

        return df
elif Stromnutzung == "eigene Daten als csv":
    uploaded_files = st.file_uploader(
        "Upload data", accept_multiple_files=False, type="csv"
    )
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.write("oui")

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
        status = st.radio(
            "Gebäude saniert oder sogar GEAK bekannt?",
            ["Nein", "Ja", "GEAK Klasse"],
            horizontal=True
        )
        reduktion = 0.0
        if status == "Ja":
            Sanierungstyp = st.multiselect(
                "Sanierungstyp",
                list(reduktionen.keys())
            )
            reduktion = sum(reduktionen[typ] for typ in Sanierungstyp)
            Heizwaermebedarf_total = Heizwaermebedarf * (1 - reduktion)
        elif status == "GEAK Klasse":
            geak_klasse = st.selectbox(
                "GEAK Klasse wählen",
                list(GEAK_Klassen.keys())
            )
            Heizwaermebedarf_total = GEAK_Klassen[geak_klasse] * m2

        else:
            Heizwaermebedarf_total = Heizwaermebedarf
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
    "Heizsystem wählen", ["Fossil & Holz", "Wärmepumpe"],
    default="Fossil & Holz"
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
    if "Heizwaermebedarf_input" in locals():
        stromverbrauch = Heizwaermebedarf_input / jaz
    else:
        stromverbrauch = 0.0
    StromverbrauchWP_input = st.number_input(
        "Stromverbrauch [kWh/a]",
        value=int(stromverbrauch)
    )
    ergebnis = stromverbrauch

st.write("------------------------------")

st.subheader("Photovoltaikanlage")
standort_auswahl = st.selectbox(
    "Standort wählen",
    list(standort_dateien.keys())
)
PVAnlagen = st.number_input(
    "Anzahl PV-Anlagen",
    min_value=1,
    max_value=5,
    value=1,
    step=1
)
pv_anlagen_daten = []
for i in range(PVAnlagen):
    st.markdown(f"### PV-Anlage {i+1}")

    PVart = st.segmented_control(
        f"Photovoltaiktyp",
        ["Monokristalin", "Polykristalin"],
        default="Monokristalin",
        key=f"pvart_{i}"
    )

    pv_Peakleistung = st.number_input(
        f"PV-Peakleistung (kWp)",
        min_value=0.0,
        max_value=1000.0,
        value=10.0,
        step=0.1,
        key=f"peakleistung_{i}"
    )

    Dachneigung = st.number_input(
        f"Dachneigung (°)",
        min_value=0,
        max_value=90,
        value=45,
        step=1,
        key=f"neigung_{i}"
    )

    Dachausrichtung = st.number_input(
        f"Dachausrichtung (°)",
        min_value=-180,
        max_value=180,
        value=0,
        step=1,
        key=f"ausrichtung_{i}"
    )

    st.caption("Neigung: 0 = Flachdach, 90 = Fassade")
    st.caption("Ausrichtung: 0 = Süd, -90 = Ost, +90 = West, -180 / +180 = Nord")

    pv_anlagen_daten.append({
        "Anlage": i + 1,
        "PVart": PVart,
        "pv_Peakleistung": pv_Peakleistung,
        "Dachneigung": Dachneigung,
        "Dachausrichtung": Dachausrichtung
    })



st.write("------------------------------")
st.subheader("Batterie")
batteriekapazität = st.slider("Batteriekapazität (kWh)", 0, 20, 10)
maxLadeleistungBatterie = st.slider("max. Ladeleistung der Batterie (kW)", 0, 20, 10)
maxEntladeleistungBatterie = st.slider("max. Entladeleistung der Batterie (kW)", 0, 20, 10)
minSoC = st.number_input("Min. SoC (%)", 0, 50, 20)
maxSoC = st.number_input("Max. SoC (%)", 60, 100, 80)


st.write("------------------------------")
st.subheader("Einspeisen")
# regel einbauen minSoC muss < sein als maxSoC
Einspeisegrenze = st.number_input("Einspeisegrenze (%)", 60, 100, 70)
EinspeisegrenzekW = (Einspeisegrenze/100)* pv_Peakleistung
st.metric("Einspeisegrenze kW:", EinspeisegrenzekW, "kW")

st.write("------------------------------")
st.subheader("Ausspeisen")
Bezugsgrenze = st.number_input("Bezugsgrenze (kW)", 60, 100, 80)
EVU_name = st.selectbox(
    "EVU wählen",
    list(EVU.keys())
)
CO2Emmisionen = EVU[EVU_name]
CO2Emmisionen_input = st.number_input(
    "CO2 Emmisionen [kg CO2e/MWh]",
    value=int(CO2Emmisionen)
)
ergebnis = CO2Emmisionen

st.write("------------------------------")
st.subheader("Test Zeitreihe")

df_ts = create_base_dataframe()

df_ts = add_slp_profile(df_ts, slp_df, jahresstromverbrauch)

# Heizwärmebedarf übernehmen (oder Testwert)
if "Heizwaermebedarf_input" in locals():
    heizwaerme_jahr = Heizwaermebedarf_input
else:
    heizwaerme_jahr = 12000

df_ts = add_heating_profile(df_ts, heizwaerme_jahr)

if heizsystem == "Wärmepumpe":
    df_ts = add_heatpump_consumption(df_ts, heizsystem, jaz)
else:
    df_ts = add_heatpump_consumption(df_ts, heizsystem)
df_ts = add_pv_profile(df_ts, pv_Peakleistung)
df_ts = simulate_battery(
    df_ts,
    batteriekapazität,
    maxLadeleistungBatterie,
    maxEntladeleistungBatterie,
    minSoC,
    maxSoC,
    EinspeisegrenzekW,
    Bezugsgrenze
)
df_ts, monatsbilanz, jahreskennzahlen = create_energy_summary(df_ts)

#Kennzahlenblock
#st.write("Anzahl Stunden im Jahr:", len(df_ts))
#st.write("Summe Haushaltsstrom [kWh/a]:", round(df_ts["hauslast_kWh"].sum(), 2))
#st.write("Summe Heizwärme [kWh/a]:", round(df_ts["heizwaerme_kWh"].sum(), 2))
#st.write("Summe Wärmepumpenstrom [kWh/a]:", round(df_ts["wp_strom_kWh"].sum(), 2))
#st.write("Summe Gesamtlast [kWh/a]:", round(df_ts["gesamtlast_kWh"].sum(), 2))
#st.write("Summe PV-Produktion [kWh/a]:", round(df_ts["pv_kWh"].sum(), 2))
#st.write("Summe Netzbezug [kWh/a]:", round(df_ts["netzbezug_kWh"].sum(), 2))
#st.write("Summe Netzeinspeisung [kWh/a]:", round(df_ts["netzeinspeisung_kWh"].sum(), 2))
#st.write("Summe Abregelung [kWh/a]:", round(df_ts["abregelung_kWh"].sum(), 2))
#st.write("Summe Unterdeckung [kWh/a]:", round(df_ts["unterdeckung_kWh"].sum(), 2))

#Tabelle
# st.write("Erste 24 Stunden:")
# st.dataframe(
#     df_ts[[
#         "Monat",
#         "Stunde",
#         "gesamtlast_kWh",
#         "pv_kWh",
#         "batterie_ladung_kWh",
#         "batterie_entladung_kWh",
#         "soc_kWh",
#         "netzbezug_kWh",
#         "netzeinspeisung_kWh",
#         "abregelung_kWh",
#         "unterdeckung_kWh"
#     ]].head(24)
# )

#Plots
# st.write("Last, PV und Batterie über 24 Stunden:")
# st.line_chart(
#     df_ts[[
#         "gesamtlast_kWh",
#         "pv_kWh",
#         "netzbezug_kWh",
#         "netzeinspeisung_kWh"
#     ]].head(24)
# )

# st.write("Last, PV und Batterie über 7 Tage:")
# st.line_chart(
#     df_ts[[
#         "gesamtlast_kWh",
#         "pv_kWh",
#         "netzbezug_kWh",
#         "netzeinspeisung_kWh"
#     ]].head(168)
# )

#st.write("Abregelung und Unterdeckung über 7 Tage:")
#st.line_chart(
    #df_ts[[
        #"abregelung_kWh",
        #"unterdeckung_kWh"
    #]].head(168)
#)

st.write("------------------------------")
st.subheader("Jahreskennzahlen")

col1, col2 = st.columns(2)

with col1:
    st.metric("Autarkiegrad", f"{jahreskennzahlen['Autarkiegrad_%']:.1f} %")
    st.metric("Eigenverbrauchsquote", f"{jahreskennzahlen['Eigenverbrauchsquote_%']:.1f} %")

with col2:
    st.metric("Abgeregelte Energie", f"{jahreskennzahlen['Abgeregelte_Energie_kWh']:.1f} kWh")
    st.metric("Unterdeckung", f"{jahreskennzahlen['Unterdeckung_kWh']:.1f} kWh")

st.write("------------------------------")
st.subheader("Monatsbilanz")

st.dataframe(monatsbilanz.round(1))

st.write("Monatsbilanz:")
st.bar_chart(monatsbilanz)

st.write("Monatlicher Netzbezug und Einspeisung:")
st.bar_chart(monatsbilanz[["Bezug_kWh", "Einspeisung_kWh"]])

st.write("Monatliche Produktion und Eigenverbrauch:")
st.bar_chart(monatsbilanz[["Produktion_kWh", "Eigenverbrauch_kWh"]])



st.write("--------------------------------")
# st.write("--------------------------------")
# st.subheader("Test: Gesamtlast – 1 Woche")

# df_woche = df_ts.loc["2025-01-06":"2025-01-12 23:45"].copy()
# df_woche["Zeitstempel"] = pd.to_datetime(df_woche.index)

# fig_week = go.Figure()
# fig_week.add_trace(go.Scatter(
#     x=df_woche["Zeitstempel"],
#     y=df_woche["gesamtlast_kWh"],
#     mode="lines",
#     name="Gesamtlast"
# ))

# fig_week.update_layout(
#     title="Gesamtlast einer Woche",
#     xaxis_title="Wochentag / Datum",
#     yaxis_title="Energie [kWh pro 15 min]",
#     height=450
# )

# fig_week.update_xaxes(
#     type="date",
#     tickformat="%a<br>%d.%m",
#     dtick=24 * 60 * 60 * 1000
# )

# # Senkrechte Linien für jeden Tagesanfang
# for tag in pd.date_range(df_woche.index.min().normalize(),
#                          df_woche.index.max().normalize(),
#                          freq="D"):

#     fig_week.add_vline(
#         x=tag,
#         line_width=1,
#         line_dash="dot",
#         line_color="lightgrey",
#         opacity= 0.5,
#         layer="below"
#     )
# st.plotly_chart(fig_week, use_container_width=True)

st.subheader("Test: Gesamtlast über das Jahr")

df_year_plot = df_ts["gesamtlast_kWh"].resample("MS").sum().to_frame()
df_year_plot = df_year_plot.rename(columns={"gesamtlast_kWh": "monatslast_kWh"})
fig_year = go.Figure()
fig_year.add_trace(go.Scatter(
    x=df_year_plot.index,
    y=df_year_plot["monatslast_kWh"],
    mode="lines+markers",
    name="Gesamtlast"
))
fig_year.update_layout(
    title="Gesamtlast im Jahresverlauf",
    xaxis_title="Monat",
    yaxis_title="Energie [kWh pro Monat]",
    height=450
)
fig_year.update_xaxes(
    tickformat="%b",
    dtick="M1"
)
fig_year.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_year, use_container_width=True)

st.write("------------------------------")
st.subheader("Graphik 1 – Zeitverlauf")

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

fig = create_main_plot(df_plot, EinspeisegrenzekW, Bezugsgrenze)
st.plotly_chart(fig, use_container_width=True)

st.write("Zusammenfassung für den ausgewählten Zeitraum:")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("PV-Produktion", f"{df_plot['pv_kWh'].sum():.1f} kWh")
    st.metric("Gesamtlast", f"{df_plot['gesamtlast_kWh'].sum():.1f} kWh")

with col2:
    st.metric("Netzbezug", f"{df_plot['netzbezug_kWh'].sum():.1f} kWh")
    st.metric("Netzeinspeisung", f"{df_plot['netzeinspeisung_kWh'].sum():.1f} kWh")

with col3:
    st.metric("Abregelung", f"{df_plot['abregelung_kWh'].sum():.1f} kWh")
    st.metric("Unterdeckung", f"{df_plot['unterdeckung_kWh'].sum():.1f} kWh")

with st.expander("Daten im ausgewählten Zeitraum anzeigen"):
    st.dataframe(
        df_plot[[
            "gesamtlast_kWh",
            "pv_kWh",
            "soc_kWh",
            "netzbezug_kWh",
            "netzeinspeisung_kWh",
            "abregelung_kWh",
            "unterdeckung_kWh"
        ]].round(3)
    )

