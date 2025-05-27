import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

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

plt.figure(figsize=(7, 7))
plt.scatter(df['DOW'], df['KOSPI'], marker='.')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()

"""
Traceback (most recent call last):
  File "/Users/seongjungkim/Development/python/agentspace/adk-finance-agent/stock_agent/scatter.py", line 10, in <module>
    df = pd.DataFrame({'DOW': dow['Close'], 'KOSPI': kospi['Close']})
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/frame.py", line 778, in __init__
    mgr = dict_to_mgr(data, index, columns, dtype=dtype, copy=copy, typ=manager)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/internals/construction.py", line 503, in dict_to_mgr
    return arrays_to_mgr(arrays, columns, index, dtype=dtype, typ=typ, consolidate=copy)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/internals/construction.py", line 114, in arrays_to_mgr
    index = _extract_index(arrays)
            ^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/internals/construction.py", line 667, in _extract_index
    raise ValueError("If using all scalar values, you must pass an index")
ValueError: If using all scalar values, you must pass an index
"""