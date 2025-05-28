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


[OpenDartReader](https://github.com/FinanceData/OpenDartReader)

[전자공시](https://opendart.fss.or.kr/guide/detail.do)

- 사업보고서 (11011)
- 반기보고서 (11012)
- 분기보고서 (11013)
- 3분기보고서 (11014)

[퀀트 전략을 위한 인공지능 트레이딩](https://github.com/quant4junior/algoTrade)

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

```Python
mport FinanceDataReader as fdr

# 한국거래소 상장종목 전체
df_krx = fdr.StockListing('KRX')
df_krx.head()
```

```
     Code        ISU_CD       Name Market Dept    Close  ...      Low    Volume        Amount           Marcap      Stocks  MarketId
0  005930  KR7005930003       삼성전자  KOSPI         55400  ...    54200  13792784  765368725200  327947940878800  5919637922       STK
1  000660  KR7000660001     SK하이닉스  KOSPI        206500  ...   206000   2242626  466726993500  150332488372500   728002365       STK
2  207940  KR7207940008   삼성바이오로직스  KOSPI       1031000  ...  1023000     28702   29624006000   73380394000000    71174000       STK
3  373220  KR7373220003   LG에너지솔루션  KOSPI        286500  ...   272500    269518   75890998250   67041000000000   234000000       STK
4  012450  KR7012450003  한화에어로스페이스  KOSPI        850000  ...   846000    171723  150563190500   40201770850000    47296201       STK
```

```Python
df = fdr.DataReader('AAPL', '2024-01-01', '2025-05-31')
```

```
                  Open        High         Low       Close    Volume   Adj Close
2024-01-02  187.149994  188.440002  183.889999  185.639999  82488700  184.290421
2024-01-03  184.220001  185.880005  183.429993  184.250000  58414500  182.910507
2024-01-04  182.149994  183.089996  180.880005  181.910004  71983600  180.587524
2024-01-05  181.990005  182.759995  180.169998  181.179993  62303300  179.862839
2024-01-08  182.089996  185.600006  181.500000  185.559998  59144500  184.210999
...                ...         ...         ...         ...       ...         ...
2025-05-20  207.669998  208.470001  205.029999  206.860001  42496600  206.860001
2025-05-21  205.169998  207.039993  200.710007  202.089996  59211800  202.089996
2025-05-22  200.710007  202.750000  199.699997  201.360001  46742400  201.360001
2025-05-23  193.669998  197.699997  193.460007  195.270004  78432900  195.270004
2025-05-27  198.300003  200.740005  197.429993  200.210007  56229000  200.210007

[351 rows x 6 columns]
```

```Python
df = fdr.DataReader('KS11', '2025')
```

```
               Open     High      Low    Close     Volume  Change  UpDown   Comp          Amount            MarCap
Date                                                                                                              
2025-01-02  2400.87  2410.99  2386.84  2398.94  350691927 -0.0002       2  -0.55   6958648750080  1963454272081159
2025-01-03  2402.58  2454.67  2402.58  2441.92  407536387  0.0179       1  42.98   8230070287923  1998126924797077
2025-01-06  2453.30  2489.10  2446.82  2488.64  302760981  0.0191       1  46.72   8142307849602  2036394312458755
2025-01-07  2513.49  2521.86  2492.09  2492.10  407692929  0.0014       1   3.46   9405964049041  2038522932687508
2025-01-08  2481.25  2526.77  2481.25  2521.05  362908922  0.0116       1  28.95  10391057773317  2062626681696110
...             ...      ...      ...      ...        ...     ...     ...    ...             ...               ...
2025-05-22  2614.66  2616.53  2588.09  2593.67  358064259 -0.0122       2 -31.91   8965468020130  2126011918881695
2025-05-23  2603.57  2604.14  2589.51  2592.09  434024136 -0.0006       2  -1.58   8659673623776  2124299597613703
2025-05-26  2598.45  2644.40  2595.96  2644.40  380173138  0.0202       1  52.31   8342809610327  2166285731881608
2025-05-27  2630.29  2642.63  2625.66  2637.22  318285651 -0.0027       2  -7.18   7908808324037  2160239944298804
2025-05-28  2648.86  2692.47  2643.50  2672.41  323442924  0.0133       1  35.19   8391363574831  2189815113870997

[97 rows x 10 columns]
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