# autoTrade
pyupbit 라이브러리를 활용한 Upbit 자동매매 프로그램입니다.

<a href="https://velog.io/@johoon815/series/%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8-%EC%9E%90%EB%8F%99%EB%A7%A4%EB%A7%A4" target="_blank">**사용 방법(velog)**</a> 👈 쉬프트 클릭 OR 휠 클릭!
<br><br>
### Install Library
```bash
sudo pip3 install pyupbit numpy requests
```
또는
```bash
sudo pip install pyupbit numpy requests
```
<br><br>
### test.py
API와 정상적으로 **통신이 되는지 체크**하는 파일입니다.
<br><br>

### KR-ticker_list.py
**원화(KR) 시장**의 **종목 코드 리스트**를 보여줍니다.
<br><br>

### UpbitAutoTrade.py
자동매매 코드가 들어간 **Main** 파일입니다.<br>

**.profile 파일 수정**
맨 아래에 값을 추가 해 주시면 됩니다.
```bash
# Upbit API key
export access="업비트 API access key"
export secret="업비트 API secret key"
#
```
적용은 아래 명령어를 입력 해 주세요.
```bash
source .profile
```
<br><br>
일일 단위로 추세를 따라가며 빠른 상승세를 보이는 구간에서 유리한 **변동성 돌파 전략**을 사용하였습니다.

- **변동폭(range)** = (고가 - 저가) * k
- **매수가(target_price)** = (전일 종가 OR 당일 시가) - 변동폭(range)<br><br>

**k 값 이란?**<br>
**노이즈의 비율**입니다. **꾸준한 상승세**를 보이면 노이즈가 적으며, **횡보**를 하면 노이즈가 많아집니다.<br>
따라서 **k의 값이 높다 = 매수 목표가를 높게, k값이낮다 = 매수 목표가를 낮게** 산정됩니다.<br>

**ohlcv?**<br>
**o =** open (시가)<br>
**h =** high (고가)<br>
**l =** low (저가)<br>
**c =** close (종가)<br>
**v =** volume (거래량)<br><br>
**ex) 아래 코드를 print 해 보면**
```python
df = pyupbit.get_ohlcv("KRW-DOGE", "day" ,count=7) # DOGE 종목의 7일간 일봉 ohlcv를 구합니다.
```
**결과**
```bash
                      open   high    low  close        volume         value  range  target       ror
2021-12-10 09:00:00  212.0  217.0  205.0  208.0  3.670368e+08  7.748325e+10    1.2     NaN  1.000000
2021-12-11 09:00:00  208.0  212.0  205.0  210.0  2.099760e+08  4.385559e+10    0.7   209.2  0.004324
2021-12-12 09:00:00  210.0  215.0  207.0  211.0  1.760390e+08  3.700387e+10    0.8   210.7  0.001924
2021-12-13 09:00:00  210.0  212.0  193.0  198.0  4.447565e+08  8.962858e+10    1.9   210.8 -0.060221
2021-12-14 09:00:00  198.0  271.0  192.0  238.0  5.440710e+09  1.318695e+12    7.9   199.9  0.191095
2021-12-15 09:00:00  238.0  239.0  213.0  227.0  1.696942e+09  3.813893e+11    2.6   245.9  1.000000
2021-12-16 09:00:00  226.0  233.0  222.0  222.0  5.169321e+08  1.169025e+11    1.1   228.6 -0.028371
# target = 당일 시가(open) + 전 날 변동폭(range)
# ror = 수익율
```
<br><br>
**자동매매 실행 루틴** <br>
매수 목표가와 현재가가 같아지는 순간 <span style="color:red;">**시장가로 매수**</span>를 진행하며,<br>
익일 장이 시작되는 09:00 <span style="color:blue;">**10초 전 해당 종목을 모두 매도**</span>합니다.<br>
09:00가 되어 장이 다시 시작되면 **k의 값을 다시 계산하여 매수 목표가를 다시 산정**합니다.<br>
<br><br>

### start.sh
UpbitAutoTrade.py 파일을 데몬으로 **실행 스크립트** 파일입니다.
<br><br>

### stop.sh
UpbitAutoTrade.py 데몬의 PID를 찾아 **kill 스크립트** 파일입니다.
<br><br>

### SystemCheck_alertBot.py
시스템 날짜 조회로 시스템 **상태 체크 후 Slack으로 메시지**를 보냅니다.
<br><br>

### SystemCheck.sh
SystemCheck_alertBot.py 실행 스크립트입니다.
<br><br>

### ProcessCheck_alertBot.py 
ProcessCheck.sh로 부터 UpbitAutoTrade.py **프로세스의 상태 값을 인자**로 받아와 **정상이면 Alive, 죽어있으면 Dead 후 restart 메시지**를 **Slack**으로 보냅니다.
<br><br>

### ProcessCheck.sh
UpbitAutoTrade.py 프로세스의 **상태를 조회**하여 **정상=ok, 비정상=dead, 재기동=restart, 기동실패=fail** 의 값을 ProcessCheck_alertBot.py로 **전달**합니다.
<br><br>

### Tprice_alertBot.py
관련 종목의 **매수 목표가, 현재가를 조회**하여 **Slack**으로 메시지를 전달합니다.
<br><br>

### Tprice_alertBot.sh
Tprice_alertBot.py파일 실행 스크립트입니다.
