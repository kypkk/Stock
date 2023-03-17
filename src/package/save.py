import sqlite3
import pandas as pd
import datetime


def savebydate(df1, df2, now_date):
    print("saving date...")
    dbname = "D:\\college\\proj\\Stock_analysis\\data\\twstock.db"
    db = sqlite3.connect(dbname)
    df = pd.DataFrame(df1)
    df = df.append(df2)
    df.columns = ["Id", "Name", "Open", "Close",
                  "High", "Low", "Number", "Price", "Deal", "Time"]
    df = df.sort_values(by=["Id"])
    df.to_sql("tws_{}".format(now_date.strftime("%Y%m%d")),
              db, if_exists='replace')


def savebyname(n):
    dbname = "D:\\college\\proj\\Stock_analysis\\data\\twstock.db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    dbsave = "D:\\college\\proj\\Stock_analysis\\data\\stock_data.db"
    dbsave = sqlite3.connect(dbsave)
    cursor.execute("select name from sqlite_master where type='table'")
    tab_name = cursor.fetchall()
    tab = [x[0] for x in tab_name]
    tab.sort()
    tab = tab[-n:]
    a = 0
    print("saving name...")
    while(a < n):
        b = 0
        total_df = pd.DataFrame()
        while(b < 240):
            if(a >= n):
                break
            df = pd.read_sql('select * from {}'.format(tab[a]), db)
            df = df.iloc[:, 1:]
            total_df = pd.concat([total_df, df], axis=0, ignore_index=True)
            a += 1
            b += 1
            # print(tab[a])
        total_df.columns = ["Id", "Name", "Open", "Close",
                            "High", "Low", "Number", "Price", "Deal", "Time"]
        total_df["Time"] = pd.to_datetime(total_df["Time"])
        total_df["Time"] = [x.strftime("%Y%m%d") for x in total_df["Time"]]
        total_df = total_df.groupby('Id')
        total_dict = dict(tuple(total_df))
        for name in list(total_dict.keys())[:-1]:
            dfsingle = pd.DataFrame(total_dict[name])
            dfsingle = dfsingle.sort_values(by=["Time"])
            dfsingle.to_sql("tws_{}".format(name), dbsave, if_exists="append")
        print(a)
    check_dup()


def check_dup():
    dbsave = "D:\\college\\proj\\Stock_analysis\\data\\stock_data.db"
    dbsave = sqlite3.connect(dbsave)
    cursor = dbsave.cursor()
    cursor.execute("select name from sqlite_master where type='table'")
    tabname = cursor.fetchall()
    print("checking dup...")
    for x in tabname:
        name = x[0]
        order = "DELETE FROM {} WHERE ROWID NOT IN(SELECT ROWID FROM {} GROUP BY Time)".format(
            name, name)
        cursor.execute(order)
        # print("check {}".format(name))
    dbsave.commit()


savebyname(10)
