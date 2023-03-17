import requests as req
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

def income_statement(num,year,season,history='true'):
    url= 'https://mops.twse.com.tw/mops/web/t164sb04'
    data = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'keyword4':'', 
        'code1':'', 
        'TYPEK2':'', 
        'checkbtn':'', 
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'all',
        'isnew': history,
        'co_id': str(num),
        'year': str(year),
        'season': '0'+str(season)
    }
    r = req.post(url,data=data)
    data = data_load(r)
    return data

def balance_sheet(num,year,season,history='true'):
    url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb04'
    data = {
    'encodeURIComponent': '1',
    'step': '1',
    'firstin': '1',
    'off': '1',
    'keyword4':'', 
    'code1': '',
    'TYPEK2': '',
    'checkbtn': '',
    'queryName': 'co_id',
    'inpuType': 'co_id',
    'TYPEK': 'all',
    'isnew': history,
    'co_id': str(num),
    'year': str(year),
    'season': '0'+str(season)
    }
    r = req.post(url,data=data)
    data = data_load(r)
    return data

def Cash_Flow_Statement(num,year,season,history='true'):
    url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb06'
    data = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'keyword4': '' ,
        'code1': '',
        'TYPEK2': '',
        'checkbtn': '',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'all',
        'isnew': history,
        'co_id': str(num),
        'year': str(year),
        'season': '0'+str(season)
    }
    r = req.post(url,data=data)
    data = data_load(r)
    return data
    
def Consolidated_Statements(num,year,season,history='true'):
    url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb06'
    data = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'keyword4': '' ,
        'code1': '',
        'TYPEK2': '',
        'checkbtn': '',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'all',
        'isnew': history,
        'co_id': str(num),
        'year': str(year),
        'season': '0'+str(season)
    }
    r = req.post(url,data=data)
    data = data_load(r)
    return data

def data_load(r):
    b = BeautifulSoup(r.text,features="lxml")
    t = b.find('table',class_='hasBorder')
    l = t.findAll('tr')
    arr = []
    for i in l:
        d = i.findAll(['th','td'])
        arr.append([x.string for x in d])
    for i in range(1,10):
        if i%2 == 0:
            arr[2].insert(i,'')
        else:
            pass
    df1 = pd.DataFrame([arr[2]])
    df2 = pd.DataFrame(arr[3:])
    df = pd.concat([df1,df2],ignore_index=True)
    return df

def get(num,year,season):
    result1 = income_statement(num,year,season)
    result1.loc[len(result1)] = pd.Series(['']*result1.shape[1])
    result2 = balance_sheet(num,year,season)
    result2.loc[len(result2)] = pd.Series(['']*result2.shape[1])
    result3 = Cash_Flow_Statement(num,year,season)
    result3.loc[len(result3)] = pd.Series(['']*result3.shape[1])   
    result4 = Consolidated_Statements(num,year,season)
    result4.loc[len(result4)] = pd.Series(['']*result4.shape[1])
    result = pd.concat([result1,result2,result3,result4],axis=0,keys=['income_statement', 'balance_sheet', 'cash_flow_statement','consolidated_statement'])
    result.to_csv('C:\proj\Stock_analysis\data\{}_{}{}.csv'.format(str(num),str(year),str(season)),encoding="utf-8-sig")

num = 3105
year = 110
season = 3
get(num,year,season)