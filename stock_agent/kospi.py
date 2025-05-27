import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Maximum Drawdown (MDD) of the KOSPI index

# yfinance을 사용하여 KOSPI 데이터 다운로드
# yf.download()는 Pandas DataFrame을 직접 반환
#kospi = yf.download('^KS11', start='2004-01-04')
kospi = yf.download('^KS11', start='1990-01-04')

window = 252    # 1년 (거래일 기준)
# 'Adj Close' (수정 종가), 'Close' (종가)를 사용하여 최고점 계산
peak = kospi['Close'].rolling(window, min_periods=1).max()
# 최고점 대비 하락률(Drawdown) 계산
drawdown = kospi['Close'] / peak - 1.0
# 최대 하락률(Maximum Drawdown) 계산
max_dd = drawdown.rolling(window, min_periods=1).min()

plt.figure(figsize=(9, 7))

# 첫 번째 서브플롯: KOSPI 종가
plt.subplot(2, 1, 1)
plt.plot(kospi['Close'], label='KOSPI')

plt.subplot(2, 1, 2)
#drawdown.plot(color='blue', label='KOSPI DD', grid=True, legend=True)
#max_dd.plot(color='red', label='KOSPI MDD', grid=True, legend=True)
plt.plot(drawdown, color='blue', label='KOSPI DD')
plt.plot(max_dd,color='red', label='KOSPI MDD')

plt.show()