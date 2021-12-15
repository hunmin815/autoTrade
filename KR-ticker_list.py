#-*- coding:utf-8 -*-

import pyupbit

# 원화 시장 티커목록 조회
krw_tickers = pyupbit.get_tickers("KRW")
print("== 원화(KR) 시장의 종목을 조회합니다 ==")
print("")
print("종목 리스트 : ", krw_tickers)
print("종목 개수 : ", len(krw_tickers))