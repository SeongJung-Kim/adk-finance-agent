import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# yfinance을 사용하여 KOSPI 데이터 다운로드
# yf.download()는 Pandas DataFrame을 직접 반환
dow = yf.download('^DJI', start='2000-01-04')
kospi = yf.download('^KS11', start='2000-01-04')

#df = pd.DataFrame({'DOW': dow['Close'], 'KOSPI': kospi['Close']})
df = pd.DataFrame()
df['DOW'] = dow['Close']
df['KOSPI'] = kospi['Close']

df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

regr = stats.linregress(df['DOW'], df['KOSPI'])
regr_line = f'Y = {regr.slope:.2f}  X + {regr.intercept:.2f}'

plt.figure(figsize=(7, 7))
plt.plot(df['DOW'], df['KOSPI'], '.')
plt.plot(df['DOW'], regr.slope * df['DOW'] + regr.intercept, 'r')
plt.legend(['DOW vs KOSPI', regr_line])
plt.title('DOW vs KOSPI (R= {regr.rvalue:2f})')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()