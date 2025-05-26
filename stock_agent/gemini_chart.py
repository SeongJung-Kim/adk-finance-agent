import os
from dotenv import load_dotenv
from google import genai
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

import prompts

# (Environment and Gemini setup is assumed from previous sections)

load_dotenv()

# Access and set the Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

#model_name='gemini_2.5-pro'
model_name = os.getenv("GOOGLE_MODEL_NAME")

# Initialize Gemini
client = genai.Client()

# Data (Assumed from previous sections)

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

# Function to generate charts (modified and improved)

def generate_chart_from_gemini_output(gemini_response, data, ticker, plot_filename):
    """Generates charts based on Gemini's analysis."""

    try:    # Handle potential errors during plotting
        if "upward trend" in gemini_response.lower():
            plt.figure(figsize=(10, 6))
            # Access values for plotting
            sns.lineplot(x=data.index, y=data["Close"][ticker].values)
            plt.title(f"{ticker} - Closing Price Trend")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.show()
            plt.close()

        elif "high volatility" in gemini_response.lower():
            window = 20
            plt.figure(figsize=(10, 6))
            data[f"{ticker}_rolling_std"] = data["Close"][ticker].rolling(window=window).std()
            # Access values
            sns.lineplot(x=data.index, y=data[f"{ticker}_rolling_std"].values)
            plt.title(f"{ticker} - Rolling {window}-Day Volatility")
            plt.xlabel("Date")
            plt.ylabel("Standard Deviation")
            plt.show()
            plt.close()

        # Add more elif blocks for other Gemini outputs and chart types

    except Exception as e:
        print(f"Error generating chart: {e}")


# Example Usage (Modified to avoid filename conflicts with previous sections)
plot_counter = 6    # Start from 6 since previous sections generated 5 plots

prompt_template = prompts.trend_analysis_prompt
for i, ticker in enumerate(tickers):
    example_prompt = prompt_template.format(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )
    gemini_response_trend_analysis = client.models.generate_content(
        model=model_name,
        contents=example_prompt,
    ).text

    try:
        generate_chart_from_gemini_output(
            gemini_response_trend_analysis, data, ticker, f"plot_{plot_counter + i}.png"
        )
    except Exception as e:
        print(f"Error in chart generation loop: {e}")

# Example: Combined Visualization (Modified for clarity and filename)
plt.figure(figsize=(12, 7))

plt.subplot(2, 1, 1)
# Access values for plotting
sns.lineplot(x=data.index, y=data["Close"]['AAPL'].values, label='AAPL Close')

# Access values for plotting
sns.lineplot(x=data.index, y=data["AAPL_20_MA"].values, label='AAPL 20-Day MA')

plt.title("AAPL Close Price and 20-Day MA")
plt.legend()

plt.subplot(2, 1, 2)
sns.lineplot(x=data.index, y=data["AAPL_Daily_Change"].values, label='AAPL Daily % Change', color='orange') # Access values for plotting
plt.axhline(0, color='gray', linestyle='--')
plt.title("AAPL Daily Percentage Change")
plt.legend()

plt.tight_layout()
plt.show()
plt.close()