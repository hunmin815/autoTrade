#-*- coding:utf-8 -*-

import time
import pyupbit
import datetime
import numpy as np
import os

access = os.environ['access']                           # Upbit API access 키
secret = os.environ['secret']                           # Upbit API secret 키


fee = 0.9995  # 거래 수수료 0.05%

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

# 거래 시작 시각 조회_시작
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, "day", count=1)
    start_time = df.index[0]
    return start_time

# 종목 현재 가격조회_시작
def get_current_price(ticker):
    # return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


    # 변동성 돌파 전략 매수 목표가 추출_시작
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, "day", count=2)
    target_price = df.iloc[0]["close"] + (df.iloc[0]["high"] - df.iloc[0]["low"]) * k
    return target_price


# 로그인_시작
try:
  upbit = pyupbit.Upbit(access, secret)
  my_Balance = get_balance("KRW")             # 내 잔고
  print("Login OK")
  print("==========Autotrade start==========")
except:
  print("!!Login ERROR!!")
# 로그인_끝
else:
  print("내 잔고 : "+str(format(int(my_Balance),','))+" 원")
  # print("date:"+str(datetime.datetime.now()))
  ticker = "KRW-DOGE"
  current_price = get_current_price(ticker)
  print("current_price:", current_price)  # 현재가

  print(get_start_time(ticker))

  target_price = round(get_target_price(ticker, 0.1), 0)
  print("target_price:", target_price)  # 매수 목표가

