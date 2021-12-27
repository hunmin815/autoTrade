# -*- coding:utf-8 -*-

import time
import pyupbit
import datetime
import numpy as np
import os

access = os.environ["access"]  # Upbit API access 키
secret = os.environ["secret"]  # Upbit API secret 키

fee = 0.9995  # 거래 수수료 0.05%

# 내 잔고 조회_시작
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b["currency"] == ticker:  # 통화
            if b["balance"] is not None:
                return float(b["balance"])
            else:
                return 0


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


# 거래 시작 시각 조회_시작
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, "day", count=1)
    start_time = df.index[0]
    return start_time


# 종목 현재 가격조회_시작
def get_current_price(ticker):
    # return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"] # pyupbit==0.2.18
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0][
        "ask_price"
    ]  # pyupbit==0.2.21


# 로그인_시작
try:
    upbit = pyupbit.Upbit(access, secret)
    my_Balance = get_balance("KRW")  # 내 잔고
    print("Login OK")
    print("==========Autotrade start==========")
except:
    print("!!Login ERROR!!")
# 로그인_끝
else:
    print("내 잔고 : " + str(format(int(my_Balance), ",")) + " 원")
    print("date:" + str(datetime.datetime.now()))
    best_k_run = 1  # k값 구하기 동작 여부
    buy_price = 0  # 매수 총가
    while 1:
        try:
            ticker = "KRW-DOGE"  # 종목 코드
            now = datetime.datetime.now()  # 현재시각
            start_time = get_start_time(ticker)  # 거래 시작 시각
            end_time = start_time + datetime.timedelta(days=1)  # 거래 종료 시각

            # best_k 구하기_시작
            if best_k_run == 1:
                ror1, next_ror, best_ror, best_k = 0.0, 0.0, 0.0, 0.1
                for k in np.arange(0.1, 1.0, 0.1):
                    next_ror = get_ror(ticker, k)
                    time.sleep(0.3)
                    if ror1 < next_ror:  # k값중 최고 k 구하기
                        if next_ror != 1:  # 수익률이 0% 가 아닐 때
                            print(
                                "k : %.1f ror1 : %f  next_ror : %f"
                                % (k, ror1, next_ror),
                                "change",
                            )
                            ror1 = next_ror
                            best_k = k
                            best_ror = ror1
                        else:
                            print(
                                "k : %.1f ror1 : %f  next_ror : %f"
                                % (k, ror1, next_ror),
                                "No change_1",
                            )
                    else:
                        print(
                            "k : %.1f ror1 : %f  next_ror : %f" % (k, ror1, next_ror),
                            "No change_2",
                        )
                print("best_k : %.1f  best_ror : %f" % (best_k, best_ror))
                best_k_run = 0
            # best_k 구하기_끝

            if (
                start_time < now < end_time - datetime.timedelta(seconds=10)
            ):  # 9:00 ~ 다음날 8:59:50
                target_price = round(get_target_price(ticker, best_k), 0)
                print("target_price:", target_price)  # 매수 목표가
                current_price = round(get_current_price(ticker), 0)
                print("current_price:", current_price)  # 현재가

                if target_price == current_price:  # 매수 목표가에 현재가 도달시
                    my_ticker_bal = get_balance(ticker.split("-")[1])  # 종목 잔고
                    if (
                        my_ticker_bal == None or my_ticker_bal < 1.0
                    ):  # 코인 보유 여부 (없거나 한 개라도 보유)
                        my_krw = get_balance("KRW")  # 원화 잔고
                        print("Your_KRW_Balance:", my_krw)

                        if my_krw > 100000.0:
                            my_krw = 100000.0  # 10만 원치만 매수

                        if my_krw > 5000:  # 최소 주문금액 5000원
                            print(now, "=== Buy_" + ticker.split("-")[1] + "===")
                            # before_Buy_my_Balance = round(my_krw,0)
                            upbit.buy_market_order(ticker, my_krw * fee)  # 시장가 매수
                            time.sleep(5)

                            my_ticker_bal = get_balance(ticker.split("-")[1])
                            buy_price = (
                                current_price * my_ticker_bal
                            ) # 매수 총가 = (매수가 * 종목수량) (이미 수수료 반영됨)
                    else:
                        print(
                            "== NOT BUY!_You Have Already "
                            + ticker.split("-")[1]
                            + " =="
                        )

            else:  # 다음날 오픈 전 풀매도
                best_k_run = 1
                my_ticker_bal = get_balance(ticker.split("-")[1])
                current_price = round(get_current_price(ticker), 0)

                if (
                    current_price * my_ticker_bal
                ) > 5000:  # 보유 중인 종목의 잔고가 최소 주문금액 5000원 초과 시
                    print("My_" + ticker.split("-")[1] + "_Balance:", my_ticker_bal)
                    print(now, "=== Sell_" + ticker.split("-")[1] + "_All ===")
                    upbit.sell_market_order(ticker, my_ticker_bal)  # 시장가 매도
                    time.sleep(5)

                    sell_price = (
                        current_price * my_ticker_bal
                    ) * fee  # 매도 총가 = (매도가 * 종목수량) * 수수료 빼기
                    profit = (
                        round(buy_price - sell_price, 0) * -1
                    )  # 수익 = (매수 총가 - 매도 총가) 반올림 후 -1 곱하기
                    print("profit:", profit)
            time.sleep(1.5)  # 시세 체크 속도
        except Exception as e:
            print(e)
            time.sleep(1)
