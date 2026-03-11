Stock Risk & Free Cash Flow Analyzer

A lightweight financial analysis dashboard built with Streamlit that evaluates stocks using market data from Yahoo Finance.

The app analyzes:
- Price history
- Volatility (risk level)
- Sharpe Ratio (risk-adjusted return)
- Quarterly Free Cash Flow

This tool is useful for quickly evaluating a company's performance, risk, and financial health.

Features
- Price Visualization
Displays historical stock price data for a selected time period.

- Sharpe Ratio
Calculates the risk-adjusted return using annualized returns.

- Volatility Risk Classification
Classifies stock risk based on annualized volatility:

Volatility Risk Level
< 20%	Low
20–40%	Medium
> 40%	High

Free Cash Flow Analysis
- Shows quarterly Free Cash Flow (FCF) calculated as:
- FCF = Operating Cash Flow − Capital Expenditures
- If direct FCF data exists, the app uses it automatically.

Installation

Clone the repository:

git clone https://github.com/moussachebli/stock-risk-analyzer.git
cd stock-risk-analyzer

Install dependencies:
pip install streamlit yfinance matplotlib pandas
Running the App

Run the Streamlit dashboard:
streamlit run stock_app.py

The app will open at:
http://localhost:8501

Example Analysis
The dashboard allows you to analyze any stock ticker (ex: AAPL, NVDA, MSFT) and instantly see:

- Price trend
- Risk classification
- Sharpe ratio
- Free cash flow performance
- Future Improvements

Market data is retrieved from Yahoo Finance via the yfinance library.

License
MIT License
