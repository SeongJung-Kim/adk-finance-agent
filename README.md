Build a financial analysis agent using
"Gemini AI for Financial Analysis and Report Generation in Python"

[Gemini AI for Financial Analysis and Report Generation in Python](https://janelleturing.medium.com/gemini-for-financial-analysis-and-report-generation-in-python-99a08f853788)

[깃허브](https://github.com/SeongJung-Kim/adk-finance-agent)

[Generating content](https://ai.google.dev/api/generate-content)

[Google 모델](https://cloud.google.com/vertex-ai/generative-ai/docs/models)

```bash
git clone https://github.com/SeongJung-Kim/adk-finance-agent.git
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


![애플 20일 이동평균](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/aapl_rolling_20-day_volatility.png)  
Figure: AAPL - 롤링 (Rolling) 20일 변동성 (Volatility)

![마이크로소프트 종가 Trend](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/msft_close_price_trend.png)  
Figure: MSFT - 종가 추세 (Trend)

![애플 종가 & 20일 이동평균](https://raw.githubusercontent.com/SeongJung-Kim/adk-finance-agent/main/docs/images/aapl_close_price&20-day_ma.png)  
Figure: AAPL Close Price, 20-Day MA and Daily % Change