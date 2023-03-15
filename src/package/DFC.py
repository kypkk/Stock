import pandas as pd
import requests
from bs4 import BeautifulSoup
import html5lib
import re
from lxml import html, etree

type = int(input("(1)ROCO (2)TPE? "))
if type == 1:
    type1 = "ROCO"
    type2 = "TWO"
elif type == 2:
    type1 = "TPE"
    type2 = "TW"

stock_no = input("Stock ID? ")

Wacc = f"https://www.gurufocus.cn/stock/{type1+':'+str(stock_no)}/term/wacc"
data = requests.get(Wacc)
soup = BeautifulSoup(data.text, "html5lib")
title = soup.select("#term-page-title")
WACC = float(re.search(r'\d+\.\d+', title[0].contents[3]).group())
print(f"WACC = {WACC}")

# eps_web = f"https://finance.yahoo.com/quote/{stock_no}.{type2}/financials?p=3105.TWO"
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
# res = requests.get(eps_web, headers=headers)
# byte_data = res.content
# source_code = html.fromstring((byte_data))
# result = source_code.xpath(
#     '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[3]/div[1]/div/div[2]/div[11]/div[1]/div')
# eps = []
# for i in range(1, len(result)):
#     eps.append(result[i].xpath('text()')[0])
# number = 0
# av_eps = 0
# for i in eps:
#     if i != '-':
#         number += 1
#         try:
#             av_eps += float(i)
#         except:
#             pass
# av_eps = av_eps/number
# print(f"Average_eps = {av_eps}")

eps = float(input("eps(年): "))
Growth = float(input("前五年年成長率(%): "))
Final_Growth = float(input("成熟市場成長率(%)(2~3): "))

cash_list = []
value = eps
for i in range(5):
    value = value*(1+Growth/100)
    cash_list.append(value)

final_value = value*(1+Final_Growth/100)/(WACC/100-Final_Growth/100)

total = 0
for i in range(5):
    discount = (1+WACC/100)**i
    now = cash_list[i]/discount
    total = total + now

fix_final_value = final_value/((1+WACC/100)**5)
price = total + fix_final_value

df = pd.DataFrame(cash_list)
df.columns = ["Predicted_Eps"]
df = df.append({"Predicted_Eps": fix_final_value}, ignore_index=True)
df.index = df.index + 1
print(df)
print(price)
