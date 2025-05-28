import yfinance as yf

def analyze_company_fundamentals(ticker):
    """
    Analyzes a company's financial health using fundamental data.

    Args:
        ticker (str): The ticker symbol of the company. (e.g., "AAPL" for Apple)

    Returns:
        dict: A dictionary containing key financial ratios and information.
              or None if data cannot be fetched.
    """
    try:
        company = yf.Ticker(ticker)

        # --- Get Key Information ---
        info = company.info
        if not info:
            print(f"Could not retrieve information for {ticker}")
            return None
        
        # --- Key Fundamental Metrics & Ratios ---
        # (Note: Availability of these metrics depends on yfinance and the company)

        # 1. Profitability Ratios
        profit_margins = info.get("profitMargins", None)    # Net Profit Margin
        operating_margins = info.get("operatingMargins", None)  # Operating Profit Margin
        ebitda_margins = info.get("ebitdaMargins", None)  # EBITDA Margin
        gross_margins = info.get("grossMargins", None)  # Gross Profit Margin
        return_on_equity = info.get("returnOnEquity", None)  # Return on Equity (ROE)
        return_on_assets = info.get("returnOnAssets", None)  # Return on Assets (ROA)
        
        # 2. Liquidity Ratios
        current_ratio = info.get("currentRatio", None)  # Current Ratio
        quick_ratio = info.get("quickRatio", None)  # Quick Ratio

        # 3. Solvency Ratio
        debt_to_equity = info.get("debtToEquity", None)  # Debt to Equity Ratio
        total_debt = info.get("totalDebt", None)  # Total Debt
        total_cash = info.get("totalCash", None)  # Total Cash
        net_debt = total_debt - total_cash if total_debt is not None and total_cash is not None else None

        # 4. Valuation Ratios
        market_cap = info.get("marketCap", None)  # Market Capitalization
        price_to_earnings = info.get("priceToEarnings", None)  # Price to Earnings Ratio
        forward_pe = info.get("forwardPE", None)  # Forward P/E Ratio
        price_to_book = info.get("priceToBook", None)  # Price to Book Ratio
        price_to_sales = info.get("priceToSalesTrailing12Months", None)  # Price to Sales Ratio
        enterprise_value = info.get("enterpriseValue", None)  # Enterprise Value
        ev_to_revenue = info.get("enterpriseToRevenue", None)  # Enterprise Value to Revenue Ratio
        ev_to_ebitda = info.get("enterpriseToEbitda", None)  # Enterprise Value to EBITDA Ratio

        # 5. Growth Metrics (Often require historical data analysis - yfinance can provide this)
        # Example: Earnings Growth (you might need to pull historical financials for this)
        earnings_quarterly_growth = info.get("earningsQuarterlyGrowth", None)  # YoY Quarterly Earnings Growth

        # 6. Dividend Information
        dividend_yield = info.get("dividendYield", None)  # Dividend Yield
        payout_ratio = info.get("payoutRatio", None)  # Payout Ratio

        # --- Store results ---
        analysis = {
            "Ticker": ticker,
            "Company Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": market_cap,
            
            "Profitability": {
                "Profit Margin": profit_margins,
                "Operating Margin": operating_margins,
                "EBITDA Margin": ebitda_margins,
                "Gross Margin": gross_margins,
                "Return on Equity (ROE)": return_on_equity,
                "Return on Assets (ROA)": return_on_assets,
            },
            "Liquidity": {
                "Current Ratio": current_ratio,
                "Quick Ratio": quick_ratio,
            },
            "Solvency": {
                "Debt to Equity Ratio": debt_to_equity,
                "Total Debt": total_debt,
                "Total Cash": total_cash,
                "Net Debt": net_debt,
            },
            "Valuation": {
                "P/E Ratio (Trailing)": price_to_earnings,
                "P/E Ratio (Forward)": forward_pe,
                "Price to Book (P/B) Ratio": price_to_book,
                "Price to Sales (P/S) Ratio": price_to_sales,
                "Enterprise Value": enterprise_value,
                "EV/Revenue": ev_to_revenue,
                "EV/EBITDA": ev_to_ebitda,
            },
            "Growth": {
                "Earnings Quarterly Growth (YoY)": earnings_quarterly_growth,
            },
            "Dividends": {
                "Dividend Yield": dividend_yield,
                "Payout Ratio": payout_ratio,
            }
        }

        return analysis

    except Exception as e:
        print(f"An error occured for {ticker}: {e}")
        return None

def print_analysis(analysis_data):
    """Prints the fundamental analysis data in a readable format."""
    if analysis_data is None:
        return
    
    print("\n--- Company Fundamental Analysis ---")
    print(f"Ticker: {analysis_data['Ticker']}")
    print(f"Company Name: {analysis_data['Company Name']}")
    print(f"Sector: {analysis_data['Sector']}")
    print(f"Industry: {analysis_data['Industry']}")
    print(f"Market Cap: {analysis_data['Market Cap']:,}" if analysis_data['Market Cap'] else "N/A")

    for category, metrics in analysis_data.items():
        if isinstance(metrics, dict):
            print(f"\n--- {category} ----")
            for metric, value in metrics.items():
                if isinstance(value, (int, float)):
                    print(f"{metric}: {value:.2f}" if value else f"{metric}: N/A")
                else:
                    print(f"{metric}: {value}" if value else f"{metric}: N/A")
    print("------------------------------\n")
    print("Interpretation Notes:")
    print("- Higher Profitability Ratios are generally better.")
    print("- Liquidity Ratios (e.g., Current Ratio > 1.5-2) indicate ability to meet short-term obligations.")
    print("- Solvency Ratios (e.g., lower Debt-to-Equity) indicate long-term financial stability.")
    print("- Valuation Ratios help compare with industry peers or historical values.")
    print("- Consistent Growth is a positive sign.")
    print("- Dividend information is relevant for income-focused investors.")
    print("Always compare these ratios with industry averages and the company's historical trends for better context.")

if __name__ == "__main__":
    # For a global company (e.g., Apple Inc.)
    apple_ticker = "AAPL"
    apple_analysis = analyze_company_fundamentals(apple_ticker)
    if apple_analysis:
        print_analysis(apple_analysis)

    # For a Korean company (e.g., Samsung Electronics - ticker might vary on Yahoo Finance)
    # Common ticker for Samsung Electronics on Yahoo Finance is "005930.KS"
    samsung_ticker = "005930.KS"
    samsung_analysis = analyze_company_fundamentals(samsung_ticker)
    if samsung_analysis:
        print_analysis(samsung_analysis)
