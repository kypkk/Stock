from email import message
from pickle import TRUE
from re import S
import requests
import pandas as pd
import io
import os
import datetime
import time
from bs4 import BeautifulSoup
import random
import sqlite3
import numpy as np
import threading
from queue import Queue
from package import save


class DataException(Exception):
    def __init__(self, message):
        super().__init__(message)


message = "No Data"
dbname = os.getcwd() + '\\src\\resource\\daily_data.db'
db2name = os.getcwd() + '\\src\\resource\\stock_data.db'


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
        if existense(now_date) == False:
            try:
                df1 = twscrawler(now_date)
                df2 = tecrawler(now_date)
                save.savebydate(df1, df2, now_date)
                i += 1
            except Exception as e:
                print(e)
                pass
        else:
            print("exist " + now_date.strftime("%Y%m%d"))
            i += 1
        now_date -= datetime.timedelta(days=1)
    save.savebyname(n)

# Need Modify: use Sql DB


def existense(date):
    str_date = date.strftime("%Y%m%d")
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    cursor.execute("select name from sqlite_master where type='table'")
    namelist = [x[0] for x in cursor.fetchall()]
    if "tws_{}".format(str_date) in namelist:
        return True
    else:
        return False

# crawl Tws stock


def twscrawler(date_time):
    date_time = date_time.strftime("%Y%m%d")
    url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=" + \
        date_time+"&type=ALLBUT0999"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
    print("getting tws_{} ...".format(date_time))
    response = requests.get(url, headers=headers)
    data = response.text.splitlines()
    e = False

    for i, lines in enumerate(data):
        if lines == '"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",':
            index = i
            e = True
            break
    if e == False:
        raise DataException(message)
    else:
        pass
    data_list = ''.join([x[:-1] + '\n' for x in data[index:]])
    test_df = pd.read_csv(io.StringIO(data_list))

    test_df = test_df[["證券代號", "證券名稱", "開盤價", "收盤價",
                       "最高價", "最低價", "成交股數", "成交金額", "成交筆數"]]
    test_df.columns = ["Id", "Name", "Open", "Close",
                       "High", "Low", "Number", "Price", "Deal"]
    test_df["Id"] = test_df["Id"].apply(
        lambda x: x.replace('"', ''))
    test_df["Id"] = test_df["Id"].apply(
        lambda x: x.replace('=', ''))
    test_df["Time"] = pd.to_datetime(date_time)
    test_df["Time"] = [x.strftime("%Y%m%d") for x in test_df["Time"]]
    test_df = test_df.dropna(thresh=2)
    return test_df

# crawl TE Stock


def tecrawler(time):
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
