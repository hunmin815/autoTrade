import pyupbit
import datetime
import time
import numpy as np
import requests
import os

access = os.environ["access"]  # Upbit API access 키
secret = os.environ["secret"]  # Upbit API secret 키

fee = 0.9995  # 거래 수수료 0.05%

# best_k 구하기_시작
def get_ror(ticker, k):
    df = pyupbit.get_ohlcv(ticker, "day", count=7)  # 7일간 일봉(count)
    df["range"] = (df["high"] - df["low"]) * k
    df["target"] = df["open"] + df["range"].shift(1)  # target = 매수가

    df["ror"] = np.where(
        df["high"] > df["target"], df["close"] / df["target"] - fee, 1
    )  # ror(수익율), np.where(조건문, 참일때 값, 거짓일때 값)

    ror = df["ror"].cumprod()[-2]
    return ror


# 변동성 돌파 전략 매수 목표가 추출_시작
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, "day", count=2)
    target_price = df.iloc[0]["close"] + (df.iloc[0]["high"] - df.iloc[0]["low"]) * k
    return target_price


# 종목 현재 가격조회_시작
def get_current_price(ticker):
    # return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"] # pyupbit==0.2.18
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0][
        "ask_price"
    ]  # pyupbit==0.2.21


# 메시지 전송 함수_시작
def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)


# 시간 조회_시작
def nowtime():
    now = datetime.datetime.today().strftime("%y-%m-%d %H:%M:%S")  # 현재 DateTime
    return now


myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID

ticker = "KRW-DOGE"  # 종목 코드
ror1, next_ror, best_ror, best_k = 0.0, 0.0, 0.0, 0.1

for k in np.arange(0.1, 1.0, 0.1):
    next_ror = get_ror(ticker, k)
    time.sleep(0.3)
    if ror1 < next_ror:  # k값중 최고 k 구하기
        if next_ror != 1:  # 수익률이 0% 가 아닐 때
            print(
                "k : %.1f ror1 : %f  next_ror : %f" % (k, ror1, next_ror),
                "change",
            )
            ror1 = next_ror
            best_k = k
            best_ror = ror1
        else:
            print(
                "k : %.1f ror1 : %f  next_ror : %f" % (k, ror1, next_ror),
                "No change_1",
            )
    else:
        print(
            "k : %.1f ror1 : %f  next_ror : %f" % (k, ror1, next_ror),
            "No change_2",
        )
print("best_k : %.1f  best_ror : %f" % (best_k, best_ror))

target_price = round(get_target_price(ticker, best_k), 0)  # 매수 목표가
current_price = round(get_current_price(ticker), 0)  # 현재가

post_message(myToken, myChannel, " ")
post_message(
    myToken,
    myChannel,
    ticker.split("-")[1]
    + " - 🎯 매수 목표가 : "
    + str(target_price)
    + "원\n"
    + ticker.split("-")[1]
    + " - 🔥 현재가 : "
    + str(current_price)
    + "원\nServer Time : "
    + str(nowtime()),
)
