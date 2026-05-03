import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pvlib
#st.set_page_config(layout="wide")

st.write("test1")


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
        freq="15min" #auf 15 min
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
    delta_t = 0.25  # 15 Minuten

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
        direktverbrauch = min(pv, last)

        pv_ueberschuss = pv - direktverbrauch
        restlast = last - direktverbrauch

        # 2) Batterie laden bei PV-Überschuss
        freie_kapazitaet = soc_max - soc
        batterie_ladung = min(pv_ueberschuss, max_ladung_kWh, freie_kapazitaet)
        soc += batterie_ladung

        rest_pv_nach_batterie = pv_ueberschuss - batterie_ladung

        # 3) Einspeisen bis Grenze, Rest abregeln
        netzeinspeisung = min(rest_pv_nach_batterie, einspeisegrenze_kWh)
        abregelung = max(0.0, rest_pv_nach_batterie - netzeinspeisung)

        # 4) Batterie entladen bei Restlast
        verfuegbar_batterie = soc - soc_min
        batterie_entladung = min(restlast, max_entladung_kWh, verfuegbar_batterie)
        soc -= batterie_entladung

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

    spalten = [
        "gesamtlast_kWh",
        "pv_kWh",
        "ww_kWh",
        "ev_kWh",
        "soc_kWh",
        "netzbezug_kWh",
        "netzeinspeisung_kWh",
        "abregelung_kWh",
        "unterdeckung_kWh"
    ]

    spalten = [s for s in spalten if s in df.columns]

    if zeitraum == "Tag":
        if start_datum is None:
            start_datum = df.index.min().date()

        start = pd.Timestamp(start_datum)
        ende = start + pd.Timedelta(days=1)

        df_anzeige = df[(df.index >= start) & (df.index < ende)][spalten]

        # Durchschnitt pro Stunde
        df_anzeige = df_anzeige.resample("h").mean()

    elif zeitraum == "Woche":
        if start_datum is None:
            start_datum = df.index.min().date()

        start = pd.Timestamp(start_datum)
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
        df_anzeige = df[spalten]

        # Durchschnitt pro Monat
        df_anzeige = df_anzeige.resample("MS").mean()

    else:
        df_anzeige = df[spalten]

    return df_anzeige
def create_main_plot(df_plot, einspeisegrenze_kw, bezugsgrenze_kw, zeitraum):
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

    # Warmwasser
    if "ww_kWh" in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_plot.index,
            y=df_plot["ww_kWh"],
            mode="lines",
            name="Warmwasser",
            line=dict(color="red", width=2, dash="dot")
        ))

    # E-Auto
    if "ev_kWh" in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_plot.index,
            y=df_plot["ev_kWh"],
            mode="lines",
            name="E-Auto",
            line=dict(color="green", width=2, dash="dot")
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

    if zeitraum == "Tag":
        y_title = "Durchschnittliche Energie [kWh pro Stunde]"
    elif zeitraum in ["Woche", "Monat"]:
        y_title = "Durchschnittliche Energie [kWh pro Tag]"
    elif zeitraum == "Jahr":
        y_title = "Durchschnittliche Energie [kWh pro Monat]"
    else:
        y_title = "Energie [kWh]"

    fig.update_layout(
        title="Zeitverlauf von PV, Last, Batterie und Netz",
        xaxis_title="Zeit",
        yaxis_title=y_title,
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
#Pv ertragsrechnung:
def get_station_abbr(standort_name):
    dateiname = standort_dateien[standort_name]
    return dateiname.split("_")[0]
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
def prepare_weather_for_simulation(df_weather, target_year):
    df = df_weather.copy().reset_index(drop=True) #copy vom original wetterindex und ignoriert dass die Wetterdaten aus verschiedenen Jahren sind
    new_index = pd.date_range(
        start=f"{target_year}-01-01 00:00",
        periods=len(df),
        freq="1h"
    ) # neuer Index also einfach ein Jahr im Stundenabstand
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
        if strategie == "Morgens":
            return 5 <= h < 7
        elif strategie == "Mittag / PV-optimiert":
            return 11 <= h < 15
        elif strategie == "Abends":
            return 17 <= h < 20
        elif strategie == "Kombiniert (morgens + mittags)":
            return (5 <= h < 7) or (11 <= h < 15)

    if verbraucher == "E-Auto":
        if strategie == "Morgens":
            return 5 <= h < 8
        elif strategie == "Mittag / PV-optimiert":
            return 11 <= h < 15
        elif strategie == "Abends":
            return 17 <= h < 22
        elif strategie == "Kombiniert (mittags + abends)":
            return (11 <= h < 15) or (17 <= h < 22)

    return False
def get_ev_fahrbedarf(timestamp, ev_config):
    if not ev_config["aktiv"]:
        return 0.0

    if timestamp.weekday() in ev_config["fahrtage"]:
        return ev_config["fahrzeit_tag"] * ev_config["verbrauch_pro_h"]

    return 0.0
def pruefe_ev_plausibilitaet(ev_config):
    if not ev_config["aktiv"]:
        return None
    

    ladefenster_stunden = {
        "Morgens": 3,                       # 5–8 Uhr
        "Mittag / PV-optimiert": 4,          # 11–15 Uhr
        "Abends": 5,                         # 17–22 Uhr
        "Kombiniert (mittags + abends)": 9   # 11–15 + 17–22 Uhr
    }

    fahrbedarf_kWh = ev_config["fahrzeit_tag"] * ev_config["verbrauch_pro_h"]
    max_ladung_kWh = ev_config["leistung_kw"] * ladefenster_stunden[ev_config["strategie"]]

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
    bezugsgrenze_kw
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
            ev_rest += ev_config["zusatz_nicht_fahrtag"] if ev_config["aktiv"] and i.weekday() not in ev_config["fahrtage"] else 0.0
        # E-Auto-Fahrbedarf entsteht erst nach der Fahrt, hier vereinfacht ab 17:00 Uhr
        if i.hour == 17 and i.minute == 0:
            ev_rest += get_ev_fahrbedarf(i, ev_config)


        pv = df.at[i, "pv_kWh"]
        basislast = df.at[i, "gesamtlast_kWh"]

        direkt = min(pv, basislast)
        pv_rest = pv - direkt
        restlast = basislast - direkt

        for element in prioritaeten:

            if element == "Warmwasser" and ww_rest > 0 and ww_config["steuerbar"]:
                if ist_im_zeitfenster(i, ww_config["strategie"], "Warmwasser"):
                    max_step = ww_config["leistung_kw"] * delta_t
                    ladung = min(max_step, ww_rest)

                    df.at[i, "ww_kWh"] += ladung
                    ww_rest -= ladung

                    pv_anteil = min(pv_rest, ladung)
                    pv_rest -= pv_anteil
                    restlast += ladung - pv_anteil

            elif element == "E-Auto" and ev_rest > 0:
                if ist_im_zeitfenster(i, ev_config["strategie"], "E-Auto"):
                    max_step = ev_config["leistung_kw"] * delta_t
                    ladung = min(max_step, ev_rest)

                    df.at[i, "ev_kWh"] += ladung
                    ev_rest -= ladung

                    pv_anteil = min(pv_rest, ladung)
                    pv_rest -= pv_anteil
                    restlast += ladung - pv_anteil

            elif element == "Batterie" and batteriekapazitaet > 0:
                freie_kapazitaet = soc_max - soc
                max_ladung = max_ladeleistung * delta_t

                ladung = min(pv_rest, max_ladung, freie_kapazitaet)
                soc += ladung
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
        df.at[i, "netzbezug_kWh"] = netzbezug
        df.at[i, "unterdeckung_kWh"] = unterdeckung

    df["gesamtlast_kWh"] = df["gesamtlast_kWh"] + df["ww_kWh"] + df["ev_kWh"]

    return df
def add_uploaded_load_profile(df_base, uploaded_file):
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

    df_upload["verbrauch_kWh"] = df_upload["verbrauch_roh"] / 4

    df_upload = df_upload[["verbrauch_kWh"]]

    df_upload = df_upload.reset_index()
    df_upload["timestamp"] = df_upload["timestamp"].apply(
        lambda x: x.replace(year=df.index[0].year)
    )
    df_upload = df_upload.set_index("timestamp")

    df_upload = df_upload.resample("15min").sum()

    df = df.join(df_upload, how="left")
    df["hauslast_kWh"] = df["verbrauch_kWh"].fillna(0)

    return df

# Aus dem Bericht stammen methodisch:
# 	•	Strahlungsdaten als Eingangsdaten
# 	•	stündliche Verarbeitung
# 	•	Umrechnung auf geneigte Fläche
# 	•	Verwendung eines anisotropen Modells
# 	•	Berücksichtigung von Modulwirkungsgrad und Performance Ratio als Einflussgrößen auf den PV-Ertrag
# Für dein Tool habe ich konkret modelliert:
# 	•	pvlib für Sonnenstand und Transposition
# 	•	15-min-Interpolation
# 	•	Zelltemperaturmodell
# 	•	Leistungsformel für jeden Zeitschritt
# 	•	aus Peakleistung und Wirkungsgrad abgeleitete Modulfläche
# Der Wirkungsgrad-Eingabewert beeinflusst den Ertrag praktisch nicht.
# Die Batteriesimulation mischt kW und kWh.

# noch ändern
# WW schwankt
# Wochenendverhalten anders


st.header("Dimensionierungstool")

EBFm2 = st.number_input("Energiebezugsfläche bzw m2", 50, 5000, 200)
# standort_auswahl = st.selectbox(
#     "Standort wählen",
#     list(Standort.keys())
# ) 
jahresstromverbrauch = st.number_input("Jahresstrombedarf total(kWh/a)", 1000, 10000, 4500)
Stromnutzung = st.segmented_control(
    "Standartstromnutzungsprofil oder eigene daten als csv?",
    ["Standartprofil", "eigene Daten"],
    default="Standartprofil",
    key="Stromnutzung"
)
uploaded_file = None
if Stromnutzung == "eigene Daten":
    uploaded_file = st.file_uploader(
        "Upload Lastprofil",
        accept_multiple_files=False,
        type=["csv", "xlsx"]
    )
    st.info("""
    CSV-Format:
    timestamp,verbrauch_kWh
    2025-01-01 00:00,0.42
    2025-01-01 00:15,0.38
    2025-01-01 00:30,0.35
    """)

st.write("-----------------------")
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
        ww_waermebedarf_kWh = 15 * m2# 15 kWh/m²a × Wohnfläche wert noch nach quelle finden
        raumheizung_waermebedarf_kWh = max(0, Heizwaermebedarf_input - ww_waermebedarf_kWh)

        st.write(f"Anteil Warmwasser-Wärmebedarf [kWh/a]: {ww_waermebedarf_kWh:.0f}")
        st.write(f"Anteil Raumheizung [kWh/a]: {raumheizung_waermebedarf_kWh:.0f}")
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
        ww_waermebedarf_kWh = 15 * m2 # 15 kWh/m²a × Wohnfläche wert noch nach quelle finden
        raumheizung_waermebedarf_kWh = max(0, Heizwaermebedarf_input - ww_waermebedarf_kWh)

        st.write(f"Anteil Warmwasser-Wärmebedarf [kWh/a]: {ww_waermebedarf_kWh:.0f}")
        st.write(f"Anteil Raumheizung [kWh/a]: {raumheizung_waermebedarf_kWh:.0f}")
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
        ww_waermebedarf_kWh = 15 * m2 # 15 kWh/m²a × Wohnfläche wert noch nach quelle finden
        raumheizung_waermebedarf_kWh = max(0, Heizwaermebedarf_input - ww_waermebedarf_kWh)

        st.write(f"Anteil Warmwasser-Wärmebedarf [kWh/a]: {ww_waermebedarf_kWh:.0f}")
        st.write(f"Anteil Raumheizung [kWh/a]: {raumheizung_waermebedarf_kWh:.0f}")
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
    Vorlauftemperatur = st.number_input("Vorlauftemperatur (°)", 15, 60, 35)
    Wärmequellentemperatur = st.number_input("Wärmequellentemperatur (°)", 0, 60, 35)#oder aus wetterdaten
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
st.subheader("Warmwasser")

ww_aktiv = False
ww_steuerbar = False
ww_bedarf_kWh_tag = 0.0
ww_ladeleistung_kw = 0.0
ww_strategie = "Abends"
if heizsystem == "Wärmepumpe":
    ww_aktiv = True
    st.info("Warmwasser wird bei Wärmepumpe immer als elektrische Last berücksichtigt.")
    ww_steuerbar = st.checkbox("Warmwasser steuerbar", value=True)
    ww_bedarf_kWh_tag = st.number_input(
        "WW-Bedarf [kWh/Tag]",
        min_value=0.0,
        max_value=30.0,
        value=float(round(ww_waermebedarf_kWh / 365, 2)),
        step=0.1
    )
    ww_ladeleistung_kw = st.number_input(
        "WW-Ladeleistung [kW]",
        min_value=0.1,
        max_value=20.0,
        value=3.0,
        step=0.1
    )
    if ww_steuerbar:
        ww_strategie = st.selectbox(
            "WW-Strategie",
            [
                "Morgens",
                "Mittag / PV-optimiert",
                "Abends",
                "Kombiniert (morgens + mittags)"
            ]
        )
    else:
        ww_strategie = "Abends"
        st.caption("Nicht steuerbares Warmwasser wird standardmässig abends geladen.")
else:
    st.info("Warmwasser wird bei Fossil & Holz aktuell nicht als elektrische Last simuliert.")

st.write("morgens: 5-8h, Mittags: 11-15h, Abends: 17-22h")
st.write("------------------------------")
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

    ev_verbrauch_kWh_pro_h = st.number_input(
        "Verbrauch [kWh pro Fahrstunde]",
        min_value=5.0,
        max_value=30.0,
        value=12.0,
        step=0.5
    )

    ev_fahrzeit_h_tag = st.number_input(
        "Fahrzeit pro Fahrtag [h]",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
        step=0.25
    )

    ev_wochenende_kWh = st.number_input(
        "Zusatzverbrauch an Nicht-Fahrtagen [kWh/Tag]",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.5
    )

    ev_ladeleistung_kw = st.number_input(
        "E-Auto Ladeleistung [kW]",
        min_value=0.1,
        max_value=22.0,
        value=3.7,
        step=0.1
    )

    ev_strategie = st.selectbox(
        "E-Auto Ladestrategie",
        [
            "Morgens",
            "Mittag / PV-optimiert",
            "Abends",
            "Kombiniert (mittags + abends)"
        ],
        index=2
    )
else:
    ev_fahrtage = []
    ev_verbrauch_kWh_pro_h = 0.0
    ev_fahrzeit_h_tag = 0.0
    ev_wochenende_kWh = 0.0
    ev_ladeleistung_kw = 0.0
    ev_strategie = "Abends"

st.write("morgens: 5-8h, Mittags: 11-15h, Abends: 17-22h")
st.write("------------------------------")

st.subheader("Photovoltaikanlage")
standort_auswahl = st.selectbox(
    "Standort wählen",
    list(standort_dateien.keys())
)
Höhenmeter_standort = st.number_input("Höhenmeter am standort", 50, 5000, 200)
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

    PV_Wirkungsgrad = st.number_input(
        f"PV Wirkungsgrad",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.1,
        key=f"PV_Wirkungsgrad_{i}"
    )

    pv_Peakleistung = st.number_input(
        f"PV-Peakleistung (kWp)",
        min_value=0.0,
        max_value=1000.0,
        value=10.0,
        step=0.1,
        key=f"peakleistung_{i}"
    )

    gamma_pdc_input = st.number_input(
        f"Temperaturkoeffizient Pmax [1/°C]",
        min_value=-0.02,
        max_value=0.0,
        value=-0.0040,
        step=0.0001,
        format="%.4f",
        key=f"gamma_pdc_{i}"
    )

    nmot_input = st.number_input(
        f"NMOT / NOCT [°C]",
        min_value=20.0,
        max_value=80.0,
        value=45.0,
        step=0.5,
        key=f"nmot_{i}"
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
        f"Dachausrichtung/Azimuth (°)",
        min_value=0,
        max_value=380,
        value=180,
        step=1,
        key=f"ausrichtung_{i}"
    )

    st.caption("Neigung: 0 = Flachdach, 90 = Fassade")
    st.caption("Azimut: 0 = Nord, 90 = Ost, 180 = Süd, 270 = West")

    pv_anlagen_daten.append({
        "Anlage": i + 1,
        "PV_Wirkungsgrad": PV_Wirkungsgrad,
        "pv_Peakleistung": pv_Peakleistung,
        "Dachneigung": Dachneigung,
        "Dachausrichtung": Dachausrichtung,
        "gamma_pdc": gamma_pdc_input,
        "nmot": nmot_input
    })


st.write("------------------------------")
st.subheader("Batterie")

batterie_aktiv = st.checkbox("Batterie vorhanden", value=True)

if batterie_aktiv:
    batteriekapazität = st.slider("Batteriekapazität (kWh)", 1, 50, 10)
    maxLadeleistungBatterie = st.slider("max. Ladeleistung der Batterie (kW)", 1, 20, 10)
    maxEntladeleistungBatterie = st.slider("max. Entladeleistung der Batterie (kW)", 1, 20, 10)
    minSoC = st.number_input("Min. SoC (%)", 0, 50, 20)
    maxSoC = st.number_input("Max. SoC (%)", 60, 100, 80)
else:
    batteriekapazität = 0
    maxLadeleistungBatterie = 0
    maxEntladeleistungBatterie = 0
    minSoC = 0
    maxSoC = 100


st.write("------------------------------")
st.subheader("Einspeisen")
# regel einbauen minSoC muss < sein als maxSoC
Einspeisegrenze = st.number_input("Einspeisegrenze (%)", 60, 100, 70)
gesamt_pv_peakleistung = sum(anlage["pv_Peakleistung"] for anlage in pv_anlagen_daten)
EinspeisegrenzekW = (Einspeisegrenze / 100) * gesamt_pv_peakleistung
st.metric("Einspeisegrenze kW:", EinspeisegrenzekW, "kW")

st.write("------------------------------")
st.subheader("EMS")

ems_optionen = []

if ww_aktiv and ww_steuerbar:
    ems_optionen.append("Warmwasser")

if ev_aktiv:
    ems_optionen.append("E-Auto")

if batterie_aktiv and batteriekapazität > 0:
    ems_optionen.append("Batterie")

prioritaeten = st.multiselect(
    "EMS-Priorität auswählen",
    ems_optionen,
    default=ems_optionen
)

st.caption("Die Einspeisung erfolgt automatisch nach der EMS-Priorität. " \
"Nicht auswählbare Verbraucher sind nicht aktiv oder nicht steuerbar.")
# normale Hauslast plus Wärmepumpen-Raumheizung zuerst dann WW oder ev dann Batterie  dann Einspeisung

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
run_simulation = st.button("Simulation starten")

if run_simulation:
    with st.spinner("Simulation läuft... bitte warten"):

        simulationsjahr = 2025
        df_ts = create_base_dataframe(simulationsjahr)

        df_weather_raw = load_weather_data(standort_auswahl)
        df_weather = prepare_weather_for_simulation(df_weather_raw, simulationsjahr)

        # Stromprofil
        if Stromnutzung == "Standartprofil":
            df_ts = add_slp_profile(df_ts, slp_df, jahresstromverbrauch)
        elif Stromnutzung == "eigene Daten":
            if uploaded_file is not None:
                df_ts = add_uploaded_load_profile(df_ts, uploaded_file)
                st.write("Hochgeladener Jahresverbrauch [kWh]:", round(df_ts["hauslast_kWh"].sum(), 1))
            else:
                st.warning("Bitte eine Datei hochladen.")
                st.stop()

        # Raumheizung übernehmen (ohne Warmwasser)
        if "raumheizung_waermebedarf_kWh" in locals():
            heizwaerme_jahr = raumheizung_waermebedarf_kWh
        else:
            heizwaerme_jahr = 12000

        df_ts = add_heating_profile(df_ts, heizwaerme_jahr)

        if heizsystem == "Wärmepumpe":
            df_ts = add_heatpump_consumption(df_ts, heizsystem, jaz)

        else:
            df_ts = add_heatpump_consumption(df_ts, heizsystem)
            df_ts["ww_kWh"] = 0.0
            df_ts["ev_kWh"] = 0.0

        meta_df = load_station_metadata("SIA4028_metadata_2023.csv")
        station_info = get_station_info(meta_df, standort_auswahl, standort_dateien)

        # st.write("Original Wetterdaten Start:", df_weather_raw.index.min())
        # st.write("Original Wetterdaten Ende:", df_weather_raw.index.max())
        # st.write("Anzahl Wetter-Zeilen:", len(df_weather_raw))

        # st.write("Simulations-Wetterdaten Start:", df_weather.index.min())
        # st.write("Simulations-Wetterdaten Ende:", df_weather.index.max())

        df_ts["pv_kWh"] = 0.0
        df_ts["pv_power_kW"] = 0.0
        df_ts["poa_global"] = 0.0

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
                performance_ratio=0.85,
                gamma_pdc=anlage["gamma_pdc"],
                noct=anlage["nmot"]
            )

            df_ts["pv_kWh"] += df_tmp["pv_kWh"]
            df_ts["pv_power_kW"] += df_tmp["pv_power_kW"]
            df_ts["poa_global"] += df_tmp["poa_global"]

        ww_config = {
            "aktiv": ww_aktiv,
            "steuerbar": ww_steuerbar,
            "bedarf_tag": ww_bedarf_kWh_tag,
            "leistung_kw": ww_ladeleistung_kw,
            "strategie": ww_strategie
        }

        ev_config = {
            "aktiv": ev_aktiv,
            "leistung_kw": ev_ladeleistung_kw,
            "verbrauch_pro_h": ev_verbrauch_kWh_pro_h,
            "fahrzeit_tag": ev_fahrzeit_h_tag,
            "zusatz_nicht_fahrtag": ev_wochenende_kWh,
            "strategie": ev_strategie,
            "fahrtage": ev_fahrtage
        }

        ev_check = pruefe_ev_plausibilitaet(ev_config)

        if ev_check is not None:
            st.write("E-Auto Fahrbedarf pro Fahrtag [kWh]:", round(ev_check["fahrbedarf_kWh"], 1))
            st.write("Maximal mögliche Ladung im gewählten Ladefenster [kWh]:", round(ev_check["max_ladung_kWh"], 1))

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
            Bezugsgrenze
        )

        st.write("WW-Jahresverbrauch [kWh]:", round(df_ts["ww_kWh"].sum(), 1))
        st.write("EV-Jahresverbrauch [kWh]:", round(df_ts["ev_kWh"].sum(), 1))
        df_ts, monatsbilanz, jahreskennzahlen = create_energy_summary(df_ts)
        st.success("Simulation abgeschlossen ✅")

        st.session_state["df_ts"] = df_ts
        st.session_state["monatsbilanz"] = monatsbilanz
        st.session_state["jahreskennzahlen"] = jahreskennzahlen

if "df_ts" in st.session_state:
        df_ts = st.session_state["df_ts"]
        monatsbilanz = st.session_state["monatsbilanz"]
        jahreskennzahlen = st.session_state["jahreskennzahlen"]

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

        st.write("---------------------")
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

        fig = create_main_plot(df_plot, EinspeisegrenzekW, Bezugsgrenze, zeitraum)
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
                    "ww_kWh",
                    "ev_kWh",
                    "soc_kWh",
                    "netzbezug_kWh",
                    "netzeinspeisung_kWh",
                    "abregelung_kWh",
                    "unterdeckung_kWh"
                ]].round(3)
            )
        st.write("PV-Produktion Jahreswert [kWh]:", round(df_ts["pv_kWh"].sum(), 1))
        st.write("PV-Leistung Maximum [kW]:", round(df_ts["pv_power_kW"].max(), 2))
        st.write("Netzeinspeisung Jahreswert [kWh]:", round(df_ts["netzeinspeisung_kWh"].sum(), 1))
        st.write("Gesamtlast Jahreswert [kWh]:", round(df_ts["gesamtlast_kWh"].sum(), 1))
        pv_monat = df_ts["pv_kWh"].resample("MS").sum()
        st.line_chart(pv_monat)
        