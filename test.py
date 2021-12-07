import time
import pyupbit
import datetime
import numpy as np


access = "key"
secret = "key"

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