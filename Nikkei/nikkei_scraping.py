import datetime
import requests
import json
import pandas as pd

# 現在時刻取得
now_date = datetime.datetime.now()

# GMOコインのAPIで最新の1分足の為替レートを取得
end_point = 'https://forex-api.coin.z.com/public'
api_path = f'/v1/klines?symbol=USD_JPY&priceType=ASK&interval=1hour&date={now_date.strftime("%Y%m%d")}'

response = requests.get(f'{end_point}{api_path}')
if response.status_code != 200:
  print(f'エラーが発生しました。ステータス：{response.status_code}, メッセージ：{response.text}')
  exit(-1)

# レスポンス結果を取得
data = response.json()
print(data)

# pandasにデータを格納
df = pd.DataFrame(data["data"])
print(df)
