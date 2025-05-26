basic_prompt = """
What was the highest and lowest closing price for {ticker} between {start_date} and {end_date}?
"""

comparative_analysis_prompt = """
Compare the performance of {ticker1} and {ticker2} between {start_date} and {end_date} in terms of volatility and growth.
"""

trend_prompt = """
Identify any significant upward or downward trends in {ticker}'s stock price over the last year.
"""

trend_analysis_prompt = """
Analyze the stock price data for {ticker} between {start_date} and {end_date} and identify any periods of high volatility or significant growth/decline.
"""

anomaly_detection_prompt = """
Detect any unusual patterns or anomalies in the stock price data for {ticker} between {start_date} and {end_date}. For example, look for sudden price spikes or drops that deviate significantly from the normal price fluctuations.
"""

comparative_analysis_prompt = """
Compare the performance of {ticker1} and {ticker2} between {start_date} and {end_date}. Identify any potential correlations or divergences in their price movements.
"""

report_prompt = """
Generate a financial report analyzing the performance of {ticker} between {start_date} and {end_date}.

Include the following sections:

* **Executive Summary:** Briefly summarize the overall performance.
* **Performance Analysis:** Detail key performance indicators like price trends, volatility and growth. Include a table summarizing these metrics.
* **Risk Assessment:** Discuss potential risks and uncertainties.
"""

table_prompt = """
Create a table summarizing the following metrics for {ticker} from {start_date} to {end_date}:
* Highest Closing Price
* Lowest Closing Price
* Average Closing Price
* Standard Deviation of Closing Price
"""

concise_prompt = """
Analyze {tickers[0]}'s financial performance ({start_date} - {end_date}).
Key metrics: High, Low, Average and Standard Deviation of closing prices.
"""

batched_prompt = """
Provide the following metrics for {tickers} from {start_date} to {end_date}:
* Highest and lowest closing prices.
* Average closing price.
"""