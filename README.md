Build a financial analysis agent using
"Gemini AI for Financial Analysis and Report Generation in Python"


- Data Acquistion and Preprocessing: Downloading financial data using yfinance, handling missing data and preparing it for analysis with Gemini.
- Advanced Prompt Engineering for Financial Analysis: Crafting effective prompts to extract insights, compare stock performance and identify market trends using Gemini.
- Gemini-Driven Financial Data Exploration: Exploring trends, anomalies and correlations within financial datasets using Gemini's analytical capabilities.
- 

[Gemini AI for Financial Analysis and Report Generation in Python](https://janelleturing.medium.com/gemini-for-financial-analysis-and-report-generation-in-python-99a08f853788)

[깃허브](https://github.com/SeongJung-Kim/adk-finance-agent)

[Generating content](https://ai.google.dev/api/generate-content)

[Google 모델](https://cloud.google.com/vertex-ai/generative-ai/docs/models)

```bash
git clone https://github.com/SeongJung-Kim/adk-finance-agent.git
```

##

삼성전자 주식 정보 가져오기 (005930.KS)

[yfinance API Reference](https://ranaroussi.github.io/yfinance/)

```Python
import yfinance as yf

ticker = yf.Ticker('005930.KS)
data = ticker.history(start='2024-01-01', end='2025-05-31', period='1d')
```

```bash
                                   Open          High           Low         Close    Volume  Dividends  Stock Splits
Date                                                                                                                
2024-01-02 00:00:00+09:00  76094.115323  77651.028168  76094.115323  77456.414062  17142847        0.0           0.0
2024-01-03 00:00:00+09:00  76386.035461  76677.956615  74926.429688  74926.429688  21753644        0.0           0.0
2024-01-04 00:00:00+09:00  74050.675618  75218.360385  74050.675618  74537.210938  15324439        0.0           0.0
2024-01-05 00:00:00+09:00  74634.518001  75023.746257  74342.596810  74537.210938  11304316        0.0           0.0
2024-01-08 00:00:00+09:00  74926.433721  75412.969005  74342.591381  74439.898438  11088724        0.0           0.0
...                                 ...           ...           ...           ...       ...        ...           ...
2025-05-21 00:00:00+09:00  56200.000000  56600.000000  55700.000000  55700.000000   7794181        0.0           0.0
2025-05-22 00:00:00+09:00  55300.000000  55500.000000  54500.000000  54700.000000  15254278        0.0           0.0
2025-05-23 00:00:00+09:00  55000.000000  55200.000000  54100.000000  54200.000000  11247115        0.0           0.0
2025-05-26 00:00:00+09:00  53900.000000  55000.000000  53700.000000  54700.000000  10901337        0.0           0.0
2025-05-27 00:00:00+09:00  54200.000000  54500.000000  53800.000000  53900.000000  11881043        0.0           0.0

[340 rows x 7 columns]
```

```Python
import yfinance as yf

tickers = yf.Tickers('MSFT AAPL GOOG')
tickers.tickers['MSFT'].info
yf.download(['MSFT AAPL GOOG'], period='1mo')
```

Naver Finance에서 정보 가져오기

```
https://finance.naver.com/item/sise_day.nhn?code=068270&page=1
```

#### Basic Prompting

특정 기간동안 최고가 그리고 최저가

#### Comparative Analysis Prompts

변동성과 성장주 용어로 애플과 마이크로소프트 비교
잠재적 투자 기회를 확인

#### Trend Identification Prompts

추세 확인은 투자 결정을 위해 중요한 요소이다.
특정 섹터에서 장기 상승 추세(long-term upward trend) 확인
가치 투자(profitable investment)에 도움이 됨

성장 투자
분산 투자
스윙 투자

### Gemini-Driven Financial Data Exploration

#### Trend Analysis

높은 변동성 또는 중요 상승/하락 (growth/decline)의 기간 확인

#### Anomaly Detection

이상 현상(Anomaly) - unexpected price movements

#### Comparative Analysis



![주식 가격](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/stock_prices.png)

![주식 종가 가격](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/closing_prices_of_aapl_msft.png)

![애플 20일 이동평균](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/aapl_rolling_20-day_volatility.png)  
Figure: AAPL - 롤링 (Rolling) 20일 변동성 (Volatility)

![마이크로소프트 종가 Trend](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/msft_close_price_trend.png)  
Figure: MSFT - 종가 추세 (Trend)

![애플 종가 & 20일 이동평균](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/aapl_close_price&20-day_ma.png)  
Figure: AAPL Close Price, 20-Day MA and Daily % Change