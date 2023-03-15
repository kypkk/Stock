import sqlite3
from unittest import result
import pandas as pd
import numpy as np
from sympy import true
import yfinance as yf
from pandas_datareader import data as pdr
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import datetime
from package import analysis
import time
import random
import gc


class info():
    def __init__(self, alpha, beta, sharpe):
        self.alpha = alpha
        self.beta = beta
        self.sharpe = sharpe


def plot(name):
    dbname = "D:\\college\\proj\\Stock_analysis\\data\\technique.db"
    db = sqlite3.connect(dbname)
    # arr = analysis.analyze(name)
    try:
        arr = pd.read_sql(
            "select * from tws_{}".format(name), con=db)
        pct_sp500 = arr["pct_sp500"][1:]
        pct_df = arr["pct_df"][1:]
        alpha = arr["Alpha"][1]
        beta = arr["Beta"][1]
        sharpe = arr["Sharpe"][1]
        z = np.polyfit(pct_sp500, pct_df, 1)
        p1 = np.poly1d(z)
        yvals = p1(pct_sp500)
        print(name)
        print(p1)
        print(alpha)
        plt.figure(figsize=(20, 10))
        plt.scatter(pct_sp500.tolist(), pct_df.tolist())
        plt.ylabel("Daily Return of Stock")
        plt.plot(pct_sp500, yvals, color='red', label="degression")
        plt.title("{}\n{}\nalpha: {}\nsharpe: {}".format(
            name, p1, alpha, sharpe))
        plt.legend()
        plt.savefig(
            "D:\\college\\proj\\Stock_analysis\\data\\pic\\{}.png".format(name))
        plt.show()
    except Exception as e:
        print(e)


def app_df(df, name):
    dbname_new = "D:\\college\\proj\\Stock_analysis\\data\\technique.db"
    db = sqlite3.connect(dbname_new)
    df = pd.DataFrame(df)
    df.to_sql(name, db, if_exists="replace")
    print("app {}".format(name))
    db.close()
    del df
    gc.collect()


def refresh():
    dbname_base = "D:\college\proj\Stock_analysis\data\stock_data.db"
    db_base = sqlite3.connect(dbname_base)
    cursor = db_base.cursor()
    cursor.execute("select name from sqlite_master where type='table'")
    nametab = cursor.fetchall()[:-2]
    for name in nametab:
        name = name[0]
        try:
            print("update {}".format(name))
            df = analysis.analyze(name)
            app_df(df, name)
            del df
            gc.collect()
        except Exception as e:
            print(e)
    db_base.close()


"""
def rank():
    dbname = "D:\\college\\proj\\Stock_analysis\\data\\technique.db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    cursor.execute("select name from sqlite_master where type='table'")
    namelist = cursor.fetchall()
    name = [x[0][4:] for x in namelist]
    dict = []
    for name in name:
        info = {}
        arr = pd.read_sql(
            "select * from tws_{}".format(name), con=db)
        pct_sp500 = arr["pct_sp500"][1:]
        pct_df = arr["pct_df"][1:]
        alpha = arr["Alpha"][1]
        beta = arr["Beta"][1]
        sharpe = arr["Sharpe"][1]
        updo = info(alpha,beta,sharpe)
        dict.append({name:updo})
    
    
"""

while(True):
    mode = input('(1)analyze (2)plot (3)rank (4)exit:\n')
    if mode == '1':
        refresh()
    elif mode == '2':
        while(true):
            name = input()
            if name == 'exit':
                break
            else:
                plot(name)
    # elif mode == '3':
    #     rank()
    elif mode == '4':
        exit()
    else:
        pass
