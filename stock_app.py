import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st


plt.rcParams.update({
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7
})
def plot_prices(prices, ticker):
    
    fig, ax = plt.subplots(figsize=(3,2), dpi=180)
    ax.plot(prices.index, prices.values, linewidth=0.6)
    ax.set_title(f"{ticker.upper()} Price History")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.tick_params(axis="both")
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    return fig

def fetch_prices(ticker, period):
    return yf.Ticker(ticker).history(period=period)["Close"]

def compute_volatility(prices):
    returns = prices.pct_change().dropna()
    vol = returns.std() * (252 ** 0.5)

    if vol > 0.4:
        risk = "High"
    elif vol > 0.2:
        risk = "Medium"
    else:
        risk = "Low"

    return vol, risk

def get_free_cash_flow(ticker):
    cashflow = ticker.quarterly_cashflow

    if cashflow is None or cashflow.empty:
        return None

    index = cashflow.index.str.lower()

    #try direct Free Cash Flow first
    if "free cash flow" in index.tolist():
        fcf = cashflow.loc[index == "free cash flow"].iloc[0]
        return fcf.sort_index()

    #otherwise compute FCF = OCF - CapEx
    ocf_candidates = [
        "operating cash flow",
        "total cash from operating activities",
        "cash flow from operating activities"
    ]

    ocf = None
    for name in ocf_candidates:
        if name in index.tolist():
            ocf = cashflow.loc[index == name].iloc[0]
            break

    if ocf is None:
        return None

    if "capital expenditures" not in index.tolist():
        return None

    capex = cashflow.loc[index == "capital expenditures"].iloc[0]

    fcf = ocf - capex
    return fcf.sort_index()

def sharpe_ratio(prices, risk_free_rate=0): #return of 1 = good, 2 = great, 3 = perfect
    returns = prices.pct_change().dropna()
    
    avg_return = returns.mean() - risk_free_rate
    volatility = returns.std()
    
    sharpe = (avg_return / volatility) * (252 ** 0.5)
    return sharpe

def plot_fcf(fcf, ticker):
    fig, ax = plt.subplots(figsize=(3,2), dpi=180)
    ax.bar(fcf.index.astype(str), fcf.values / 1e9)
    ax.set_title(f"{ticker.upper()} Free Cash Flow (Quarterly)")
    ax.set_ylabel("FCF (Billion USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

st.set_page_config(page_title="Stock Risk & FCF Analyzer", layout="wide")
st.title("📊 Stock Risk, Sharpe Ratio & Free Cash Flow Analyzer")

st.sidebar.header("Inputs")
ticker_symbol = st.sidebar.text_input("Stock Ticker", value="AAPL")
period = st.sidebar.selectbox(
    "Price History Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
)

analyze = st.sidebar.button("Analyze")

if analyze:
    try:
        ticker = yf.Ticker(ticker_symbol)
        prices = fetch_prices(ticker_symbol, period)

        if prices.empty:
            st.error("Invalid ticker or no price data available.")
        else:
            sharpe = sharpe_ratio(prices)
            vol, risk = compute_volatility(prices)

            col1, col2, col3 = st.columns(3)
            col1.metric("Sharpe Ratio", f"{sharpe:.2f}")
            col2.metric("Annualized Volatility", f"{vol:.2%}")
            col3.metric("Risk Level", risk)

            plot_prices(prices, ticker_symbol)

            #Free Cash Flow Section
            st.subheader("💰 Free Cash Flow Analysis")

            fcf = get_free_cash_flow(ticker)
            if fcf is None:
                st.warning("Free Cash Flow data not available.")
            else:
                latest_fcf = fcf.iloc[-1]
                status = "Positive" if latest_fcf > 0 else "Negative"

                col4, col5 = st.columns(2)
                col4.metric(
                    "Latest Free Cash Flow",
                    f"${latest_fcf/1e9:.2f}B"
                )
                col5.metric("FCF Status", status)

                plot_fcf(fcf, ticker_symbol)

    except Exception as e:
        st.error(f"Error: {e}")