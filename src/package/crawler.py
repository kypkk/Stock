from email import message
from pickle import TRUE
import requests
import pandas as pd
import io
import os
import datetime
import time
from bs4 import BeautifulSoup
import random
import sqlite3
import pymysql
import numpy as np
import db
import json


class DataException(Exception):
    def __init__(self, message):
        super().__init__(message)


message = "No Data"


def parse(n, **kwargs):
    """_summary_

    Args:
        n : 回抓幾日
        start_date : 開始日
        end_date : 結束日
    """
    # try:
    #     n = kwargs[n]
    # except:
    #     try:
    #         start_date = kwargs["start_date"]
    #     except:
    #         pass
    if "end_date" in kwargs.keys():
        now_date = kwargs["end_date"]
        if "start_date" in kwargs.keys():
            start_date = kwargs["start_date"]
        elif "n" in kwargs.keys():
            n = kwargs["n"]
        else:
            print("Wrong entering!")
    else:
        now_date = datetime.datetime.today()
    i = 0
    while i < n:
        x = random.randrange(2, 5)  # Hide from ip locker
        time.sleep(x)
        if db.existense(now_date) == False:
            try:
                df1 = twscrawler(now_date)
                df2 = tecrawler(now_date)
                db.savebydate(df1, df2, now_date)
                i += 1
            except Exception as e:
                print(e)
                pass
        else:
            print("exist " + now_date.strftime("%Y%m%d"))
            i += 1
        now_date -= datetime.timedelta(days=1)
    db.savebyname(n)


# crawl Tws stock


def twscrawler(date_time: datetime):
    """_summary_

    Args:
        date_time (datatime): Days information want to get from tws

    Raises:
        DataException: Can't get data

    Returns:
        pandas.dataframe: daily data
    """
    date_time = date_time.strftime("%Y%m%d")
    url = f"https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={date_time}&type=ALLBUT0999&response=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
    print("getting tws_{} ...".format(date_time))
    response = requests.get(url, headers=headers)
    table = json.loads(response.text)['tables']
    field = table[8]['fields']
    content = table[8]['data']
    df_dict = dict()
    for i in range(len(field)):
        df_dict[field[i]] = [j[i] for j in content]
    df = pd.DataFrame(df_dict)
    df.columns = ["Stock code", "Stock name", "Volume of shares traded", "Number of transactions", "Transaction amount", "Opening price", "Highest price", "Lowest price", "Closing price",
                  "Price change (+/-)", "Price difference", "Last displayed buying price", "Last displayed buying volume", "Last displayed selling price", "Last displayed selling volume", "PE ratio"]
    diff = [BeautifulSoup(
        x, features='lxml').string for x in df["Price difference"].to_list()]
    change = [BeautifulSoup(
        x, features='lxml').string for x in df["Price change (+/-)"].to_list()]
    Price_difference = []
    for i in range(len(diff)):
        Price_difference.append(change[i] + diff[i])
    df["Price difference"] = Price_difference
    df.drop(columns=["Price change (+/-)"], inplace=True)
    df = df[['Stock code', 'Stock name', 'Volume of shares traded',
             'Number of transactions', 'Transaction amount', 'Opening price',
             'Highest price', 'Lowest price', 'Closing price', 'Price difference',
             'PE ratio']]
    df.columns = ["ID", "NAME", "SHARES_VOLUMN", "TRANSACTIONS_NUMBER",
                  "TRANSACTION_MONEY", "OPEN", "HIGH", "LOW", "CLOSE", "DIFF", "PE"]
    return df

# crawl TE Stock


def tecrawler(time: datetime):
    """_summary_

    Args:
        time (datatime): Days information want to get from tws

    Raises:
        requests.exceptions.ConnectionError: can't get data

    Returns:
        pandas.dataframe: daily data
    """
    y = int(time.strftime("%Y"))-1911
    date = time.strftime(str(y) + "/%m/%d")
    url = "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&o=htm&d={}&se=EW&s=0,asc,0".format(
        date)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
    print('getting te_{} ...'.format(time.strftime('%Y%m%d')))
    data = requests.get(url, headers=headers)
    a = data.content.decode('utf-8')
    b = BeautifulSoup(a, features="lxml")
    t = b.findAll('tr')
    arr = []
    if t[2].findAll("td")[0].string == '共0筆':
        print('no data')
        raise requests.exceptions.ConnectionError
    for i in t[1:]:
        i = i.findAll("td")
        arr.append([x.string for x in i])
    df = pd.DataFrame(arr)
    df.columns = df.iloc[0]
    df = df[["代號", "名稱", "開盤", "收盤", "最高",
             "最低", "成交股數", "成交金額(元)", "成交筆數"]]
    df.columns = ["Id", "Name", "Open", "Close",
                  "High", "Low", "Number", "Price", "Deal"]
    df = df[:-1]
    date = time.strftime("%Y%m%d")
    df["Time"] = pd.to_datetime(time)
    df["Time"] = [x.strftime("%Y%m%d") for x in df["Time"]]
    df = df.dropna(thresh=2)
    return df


if __name__ == '__main__':
    a = twscrawler(datetime.datetime.now()-datetime.timedelta(2))
    print(a)
