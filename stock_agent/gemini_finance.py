import os
from dotenv import load_dotenv
import google.generativeai as genai

import yfinance as yf
import pandas as pd

#from .prompts import basic_prompt
#from . import prompts
import prompts

load_dotenv()

# Access and set the Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini
gemini_model = genai.GenerativeModel(model_name='gemini_2.5-pro')

# Data Download
tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL"]
end_date = "2025-05-31"
start_date = "2024-01-01"
data = yf.download(tickers, start=start_date, end=end_date)
print(data)

# Data Cleaning (Forward fill for missing values)
data.fillna(method="ffill", inplace=True)

# Data Transformation
# Calculate daily percentage change
for ticker in tickers:
    data[f"{ticker}_Daily_Change"] = data["Adj Close"][ticker].pct_change()
# Calculate 20 day moving average
for ticker in tickers:
    data[f"{ticker}_20_MA"] = data["Adj Close"][ticker].rolling(window=20).mean()


# Advanced Prompt Engineering for Financial Analysis

start_date = "2024-01-01"
end_date = "2025-05-31"

# Basic Prompting
prompt_template = prompts.basic_prompt

example_prompt = prompt_template.format(
    ticker="AAPL",
    start_date=start_date,
    end_date=end_date
)

gemini_response = gemini_model.generate_content(example_prompt).text
print(f"Basic Prompting Response:\n{gemini_response}")


# Comparative Analysis Prompts
prompt_template = prompts.comparative_analysis_prompt

example_prompt = prompt_template.format(
    ticker1="AAPL",
    ticker2="MSFT",
    start_date=start_date,
    end_date=end_date
)

gemini_response = gemini_model.generate_content(example_prompt).text
print(f"Comparative Analysis Prompt Response:\n{gemini_response}")