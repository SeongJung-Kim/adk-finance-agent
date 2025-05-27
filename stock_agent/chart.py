import yfinance as yf
import matplotlib.pyplot as plt

"""
삼성전자: 005930.KS
현대차: 005380.KS
"""

ticker = yf.Ticker('005930.KS')
data = ticker.history(start='1998-04-27', end='2025-05-31', period='1d')
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()
print(data)

plt.figure(figsize=(9, 7))
plt.plot(data.index, data['Close'], color='cyan', label='Close')
plt.plot(data.index, data['MA20'], 'm--', label='MA20')
plt.plot(data.index, data['MA200'], 'r--', label='MA200')
plt.legend(loc='best')
plt.title('Samsung Electronics')
plt.grid(color='gray', linestyle='--')
plt.yticks([65300, 50000, 100000, 150000])
plt.xticks(['1998-04-27', '2024-01-01', '2024-07-01', '2025-01-01', '2025-05-31'])
plt.show()