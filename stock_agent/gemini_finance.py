import os
from dotenv import load_dotenv
#import google.generativeai as genai
from google import genai

import yfinance as yf
import pandas as pd

#from .prompts import basic_prompt
#from . import prompts
import prompts

load_dotenv()

# Access and set the Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

#model_name='gemini_2.5-pro'
model_name = os.getenv("GOOGLE_MODEL_NAME")

# Initialize Gemini
#gemini_model = genai.GenerativeModel(model_name=model_name)
client = genai.Client()

# Data Download
tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL"]
start_date = "2024-01-01"
end_date = "2025-05-31"

data = yf.download(tickers, start=start_date, end=end_date)
print(data)
columns = list(data.columns.values)
print(columns)

# Data Cleaning (Forward fill for missing values)
data.fillna(method="ffill", inplace=True)

# Data Transformation
# Calculate daily percentage change
for ticker in tickers:
    #data[f"{ticker}_Daily_Change"] = data["Adj Close"][ticker].pct_change()
    data[f"{ticker}_Daily_Change"] = data["Close"][ticker].pct_change()
# Calculate 20 day moving average
for ticker in tickers:
    #data[f"{ticker}_20_MA"] = data["Adj Close"][ticker].rolling(window=20).mean()
    data[f"{ticker}_20_MA"] = data["Close"][ticker].rolling(window=20).mean()


print(data)
columns = list(data.columns.values)
print(columns)

# Advanced Prompt Engineering for Financial Analysis

# Basic Prompting
prompt_template = prompts.basic_prompt

example_prompt = prompt_template.format(
    ticker="AAPL",
    start_date=start_date,
    end_date=end_date
)

#gemini_response = gemini_model.generate_content(example_prompt).text
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
print(f"Basic Prompting Response:\n{gemini_response}")


# Comparative Analysis Prompts
prompt_template = prompts.comparative_analysis_prompt

example_prompt = prompt_template.format(
    ticker1="AAPL",
    ticker2="MSFT",
    start_date=start_date,
    end_date=end_date
)

#gemini_response = gemini_model.generate_content(example_prompt).text
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
print(f"Comparative Analysis Prompt Response:\n{gemini_response}")


# Trend Identification Prompts
prompt_template = prompts.trend_prompt

example_prompt = prompt_template.format(
    ticker="GOOG"
)

#gemini_response = gemini_model.generate_content(example_prompt).text
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
print(f"Trend Identification Prompt Response:\n{gemini_response}")


# Gemini-Driven Financial Data Exploration

# Trend Analysis
prompt_template = prompts.trend_analysis_prompt

example_prompt = prompt_template.format(
    ticker="AAPL",
    start_date=start_date,
    end_date=end_date
)

#gemini_response = gemini_model.generate_content(example_prompt).text
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
print(f"Trend Analysis Response:\n{gemini_response}")


# Anomaly Detection
prompt_template = prompts.anomaly_detection_prompt

example_prompt = prompt_template.format(
    ticker="MSFT",
    start_date=start_date,
    end_date=end_date
)

#gemini_response = gemini_model.generate_content(example_prompt).text
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
print(f"Anomaly Detection Response:\n{gemini_response}")


# Comparative Analysis
prompt_template = prompts.comparative_analysis_prompt

example_prompt = prompt_template.format(
    ticker1="GOOG",
    ticker2="AAPL",
    start_date=start_date,
    end_date=end_date
)

#gemini_response = gemini_model.generate_content(example_prompt).text
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
print(f"Comparative Analysis Response:\n{gemini_response}")


# Generative Narrative Financial Reports with Gemini

# Report Structuring
prompt_template = prompts.report_prompt

for ticker in tickers:
    example_prompt = prompt_template.format(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )
    gemini_response = client.models.generate_content(
        model=model_name,
        contents=example_prompt,
    ).text
    print(f"Financial Report for {ticker}:\n{gemini_response}")

    # Table Generation (within the report generation prompt)
    # The report_template above already requests a table in the Performance Analysis.

    # Combining Insights (demonstrated below by adding calculated stats)
    # Extracting a relevant statistic (e.g., 20-day MA)
    last_ma20 = data[f"{ticker}_20_MA"].iloc[-1]
    print(f"Enhanced Report for {ticker}:\n{gemini_response}")

# Example of a more detailed table generation prompt (if not included in the main report template)
prompt_template = prompts.table_prompt

example_prompt = prompt_template.format(
    ticker=tickers[0],
    start_date=start_date,
    end_date=end_date
)

#gemini_response = gemini_model.generate_content(example_prompt).text
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
print(f"Table for {tickers[0]}:\n{gemini_response}")


"""

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.lineplot(data=data['Close'])
plt.title('Closing Prices of AAPL, MSFT and GOOG')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

"""

import time
import pandas as pd

# Performance Optimization and Error Handling

# Prompt Optimization (Example demonstrating a more concise prompt)
prompt_template = prompts.concise_prompt

example_prompt = prompt_template.format(
    ticker=tickers[0],
    start_date=start_date,
    end_date=end_date
)

start_time = time.time()    # Measure API call time
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
end_time = time.time()
print(f"Concise Prompt Response ({end_time - start_time:.2f} seconds):\n{gemini_response}")


# Batching Requests (Example for fetching multiple metrics at once)

prompt_template = prompts.batched_prompt

example_prompt = prompt_template.format(
    tickers=(', '.join(tickers)),
    start_date=start_date,
    end_date=end_date
)

start_time = time.time()    # Measure API call time
gemini_response = client.models.generate_content(
    model=model_name,
    contents=example_prompt,
).text
end_time = time.time()
print(f"Batched Prompt Response ({end_time - start_time:.2f} seconds):\n{gemini_response}")

# Error Handling (Robust error handling with retries)
def call_gemini_with_retry(prompt, retries=3, backoff_factor=2):
    """Calls Gemini API with retry mechanism."""
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except Exception as e:  # Generic exception handling for various potential errors
            if i < retries - 1:
                sleep_time = backoff_factor ** i
                print(f"Error: {e}. Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                raise Exception(f"Failed to call Gemini after {retries} retries: {e}")

prompt_template = prompts.retry_prompt

example_prompt = prompt_template.format(
    ticker=tickers[1],
    start_date=start_date,
    end_date=end_date
)

gemini_response = call_gemini_with_retry(example_prompt)
print(f"Retry Prompt Response:\n{gemini_response}")