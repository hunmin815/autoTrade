import time
import pyupbit
import datetime
import numpy as np


access = "GZ6U4HsVYRc7cWINknTZOevEAWsWnQytqEiWN9iF"
secret = "DHGBbx5i30UZiUl5mxG0IvVfAUYyEXaGgxghGFUi"


# 내 잔고 조회_시작
def get_balance(ticker):
      balances = upbit.get_balances()
      for b in balances:
          if b['currency'] == ticker:
              if b['balance'] is not None:
                  return float(b['balance'])
              else:
                  return 0
# 내 잔고 조회_끝

# best_k 구하기_시작
best_k_run = 1
def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-DOGE", count=3)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.9995
      # ror(수익율), np.where(조건문, 참일때 값, 거짓일때 값)
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)

    ror = df['ror'].cumprod()[-2]
    return ror
# best_k 구하기_끝

# 로그인_시작
try:
  upbit = pyupbit.Upbit(access, secret)
  my_krw = get_balance("KRW")
  print("Login OK")
  print("==========Autotrade start==========")
except:
  print("!!Login ERROR!!")
# 로그인_끝
else:
  print("date:"+str(datetime.datetime.now()))