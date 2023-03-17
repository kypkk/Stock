# Stock
Stock Price Analysis Combine With Trading Strategy
# 程式介紹
## 步驟
### 1.資料整理
1. 利用 crawler.py 爬取 台灣證券交易所/證券櫃買交易中心 之日成交資訊
2. 整理表格成


| ID   | NAME       | OPEN   | CLOSE  | HIGH   | LOW    | NUMBER     | PRICE         | DEAL   | TIME     |
| ---- | ---------- | ------ | ------ | ------ | ------ | ---------- | ------------- | ------ | -------- |
| 0050 | 元大台灣50 | 117.85 | 118.95 | 118.95 | 117.80 | 11,087,333 | 1,312,228,564 | 10,331 | 20230317 |
| 0051       |   元大中型100         |  55.60      |     55.40   |   55.60     |    55.40    |    18,012       |    999,615           |   128     |   20230317       |
3. 利用 save.py 存取進 phpmysql
4. 將各檔資料抓出個別做歷史資料集

___
在考慮寫爬取財務報表
### 2.看盤系統(tkinter)
!. 加入KD MA 線
用 plot.py 畫K線圖
### 3.策略制定
目前考慮使用tensorflow
### 4.模擬交易
