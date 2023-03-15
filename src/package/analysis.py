from re import L
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sympy import false
import tushare as ts
import statsmodels.api as sm
from statsmodels import regression
import sqlite3
from unittest import result
import yfinance as yf
from pandas_datareader import data as pdr
from scipy.optimize import curve_fit
import datetime
import gc


def tech(df):
    df = Ma(df)
    df = Kd(df)
    return df


def Ma(df):
    df["ma_short"] = df["Close"].rolling(5).mean()
    df["ma_long"] = df["Close"].rolling(20).mean()
    return df


def Kd(df):
    # Rsv
    df_copy = df.copy()
    df_copy = df_copy[["Close", "High", "Low"]]
    df_copy["Min"] = df_copy["Low"].rolling(9).min()
    df_copy["Max"] = df_copy["High"].rolling(9).max()
    df_copy["Rsv"] = (df_copy["Close"] - df_copy["Min"]) / \
        (df_copy["Max"] - df_copy["Min"])*100
    # K
    df_copy = df_copy.dropna()
    k_list = [50]
    for index, rsv in enumerate(list(df_copy["Rsv"])):
        k_yesterday = k_list[index]
        k_today = 2/3*k_yesterday + 1/3*rsv
        k_list.append(k_today)
    df_copy["K"] = k_list[1:]
    # D
    d_list = [50]
    for index, k in enumerate(list(df_copy["K"])):
        d_yesterday = d_list[index]
        d_today = 2/3*d_yesterday + 1/3*k
        d_list.append(d_today)
    df_copy["D"] = d_list[1:]
    # J
    j_list = [50]
    for i in range(len(df_copy["K"])):
        k = df_copy["K"][i]
        d = df_copy["D"][i]
        j_today = 3*k - 2*d
        j_list.append(j_today)
    df_copy["J"] = j_list[1:]
    use_df = pd.merge(df, df_copy[["K", "D", "J"]],
                      left_index=True, right_index=True, how='left')
    return use_df


def analyze(name):
    global dfsp500
    dbname = "D:\\college\\proj\\Stock_analysis\\data\\stock_data.db"

    db = sqlite3.connect(dbname)

    df = pd.read_sql('select * from {}'.format(name), con=db)
    df.sort_values(by=["Time"], inplace=True)
    time = df["Time"].tolist()
    start = time[0]
    end = time[-1]

    n = 0
    while(n < 3):
        try:
            dfsp500 = pdr.get_data_yahoo("00646.TW", start=start, end=end)
            n = 3
        except Exception as e:
            print(e)
            n += 1

    df = df.iloc[:, 1:]

    for x in df.keys():
        df[x] = df[x].apply(lambda x: np.nan if x == ' ----' else x)
    for x in df.keys():
        df[x] = df[x].apply(lambda x: np.nan if x == '----' else x)
    for x in df.keys():
        df[x] = df[x].apply(lambda x: np.nan if x == '---' else x)
    for x in df.keys():
        df[x] = df[x].apply(lambda x: np.nan if x == '--' else x)

    df = df.fillna(method='pad')
    df = df.fillna(method='backfill')
    df["Open"] = pd.to_numeric(
        df["Open"].str.replace(',', ''))
    df["Close"] = pd.to_numeric(
        df["Close"].str.replace(',', ''))
    df["High"] = pd.to_numeric(
        df["High"].str.replace(',', ''))
    df["Low"] = pd.to_numeric(
        df["Low"].str.replace(',', ''))

    dfsp500["Time"] = pd.to_datetime(dfsp500.index.tolist())

    dfsp500["Time"] = [x.strftime("%Y%m%d") for x in dfsp500["Time"].tolist()]

    df = df.drop_duplicates(subset="Time", keep="first")
    dfsp500 = dfsp500.drop_duplicates(subset="Time", keep="first")

    df.index = df["Time"]
    dfsp500.index = dfsp500["Time"]

    df.drop(columns="Time", inplace=True)
    dfsp500.drop(columns="Time", inplace=True)

    # print(len(dfsp500.index.tolist()))
    # print(len(df.index.tolist()))

    for index, time in enumerate(df.index.tolist()):
        if time not in dfsp500.index.tolist():
            df.drop(time, inplace=True)

    # print(len(dfsp500.index.tolist()))
    # print(len(df.index.tolist()))

    for index, time in enumerate(dfsp500.index.tolist()):
        if time not in df.index.tolist():
            dfsp500.drop(time, inplace=True)

    # print(len(dfsp500.index.tolist()))
    # print(len(df.index.tolist()))

    pct_sp500 = dfsp500["Close"].pct_change()
    pct_df = df["Close"].pct_change()
    mean_sp500 = np.mean(pct_sp500[1:])
    mean_df = np.mean(pct_df[1:])
    cov = np.cov(pct_sp500[1:], pct_df[1:])
    covr = cov[0][1]
    varx = np.var(pct_sp500[1:])
    vary = np.var(pct_df[1:])
    corref = np.corrcoef(pct_sp500[1:], pct_df[1:])[0][1]
    beta = covr/varx
    alpha = mean_df/mean_sp500 - 1
    df["pct_sp500"] = pct_sp500
    df["pct_df"] = pct_df
    df["covr"] = covr
    df["varx"] = varx
    df["vary"] = vary
    df["corref"] = corref
    df["Beta"] = beta
    df["Alpha"] = alpha
    df["Sharpe"] = alpha/beta
    df = tech(df)
    return df
