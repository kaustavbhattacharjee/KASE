import pandas as pd
import math

def home_weather_reader(fol_name, year):
    file_path = fol_name + "/" + fol_name[0].lower() + fol_name[1:] + year + ".csv"
    df = pd.read_csv(file_path)
    df["Date & Time"] = pd.to_datetime(df["time"], unit='s')
    df["Date"] = [d.date() for d in df["Date & Time"]]
    df["Date"] = df["Date"].astype(str)
    df["Time"] = [d.time() for d in df["Date & Time"]]
    df["Time"] = df["Time"].astype(str)
    del df['Date & Time']
    df = df[["Date", "Time", "temperature", "humidity", "pressure", "windSpeed", "windBearing", "visibility",
             "dewPoint"]].groupby(["Date"], as_index=False).mean()
    return df


def merger(fol_name, year):
    df_elec = pd.read_csv(fol_name + "/" + fol_name + year + "_electric.csv")
    df_wea = home_weather_reader(fol_name, year)
    df = pd.merge(df_elec, df_wea, on="Date", how="outer")
    return df

def roundup_v1(x):
    return int(math.ceil(x / 10.0)) * 10

def roundup_v2(x):
    return int(math.ceil(x))