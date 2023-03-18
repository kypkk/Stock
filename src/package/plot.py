import mplfinance as mpf
import pandas as pd
import sqlite3
from pathlib import Path
import datetime
import matplotlib.pyplot as plt


def get_dataframe(num, n):
    dbname = Path.cwd() / 'data' / 'stock_data.db'
    db = sqlite3.connect(dbname)
    df = pd.read_sql('select * from tws_{}'.format(str(num)),
                     con=db).tail((int(n)))
    return df


def plot(name, df):
    df.index = pd.to_datetime(df["Time"])
    df = df[["Open", "Close", "High", "Low", "Number"]]
    df.columns = ["Open", "Close", "High", "Low", "Volume"]
    df["Open"] = pd.to_numeric(df["Open"])
    df["Close"] = pd.to_numeric(df["Close"])
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])
    df["Volume"] = df["Volume"].apply(lambda x: x.replace(',', ''))
    df["Volume"] = pd.to_numeric(df["Volume"])
    mc = mpf.make_marketcolors(up='r',
                               down='g',
                               edge='',
                               wick='inherit',
                               volume='inherit')
    s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    mpf.plot(df, type='candle', style=s, title=str(name), volume=True)


if __name__ == '__main__':
    name, n = input("Id? Days?").split()
    df = get_dataframe(name, n)
    plot(name, df)


# fig = plt.figure(figsize=(24, 8))

# ax = fig.add_subplot(1, 1, 1)
# ax.set_xticks(range(0, len(df.index), 10))
# ax.set_xticklabels(df.index[::10])
