import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

# --- Setup for Debug Logging ---
# This will print detailed logs to your terminal console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Data Fetching and Calculations ---

def get_stock_data(ticker_str):
    """Fetches both daily and intraday data for a stock."""
    logging.info(f"Fetching data for {ticker_str}...")
    ticker = yf.Ticker(ticker_str)
    
    daily_hist = ticker.history(period="2d", interval="1d")
    intraday_hist = ticker.history(period="7d", interval="15m")
    
    if daily_hist.empty or intraday_hist.empty:
        logging.error(f"No data returned for {ticker_str}. It might be delisted or have no recent trades.")
        return None, None
    
    logging.info(f"Successfully fetched data for {ticker_str}.")
    return daily_hist.iloc[-2], intraday_hist

def calculate_pivot_points(prev_day):
    """Calculates standard pivot points."""
    high, low, close = prev_day['High'], prev_day['Low'], prev_day['Close']
    pp = (high + low + close) / 3
    pivots = {
        "R2": pp + (high - low),
        "R1": (2 * pp) - low,
        "PP": pp,
        "S1": (2 * pp) - high,
        "S2": pp - (high - low),
    }
    logging.info(f"Calculated Pivots: {pivots}")
    return pivots

def calculate_emas(data):
    """Calculates all necessary EMAs for the Ripster system."""
    for period in [5, 8, 9, 12, 34, 50]:
        data[f'EMA{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
    logging.info("Calculated all EMAs.")
    return data

# --- Signal Generation and Charting ---

def get_ripster_signal(data):
    """Applies Ripster's rules to generate a signal."""
    latest = data.iloc[-1]
    price = latest['Close']
    
    is_bullish_bias = price > latest['EMA34'] and price > latest['EMA50']
    is_bearish_bias = price < latest['EMA34'] and price < latest['EMA50']
    is_long_confirmation = latest['EMA5'] > latest['EMA12']
    is_short_confirmation = latest['EMA5'] < latest['EMA12']

    # Default to Neutral
    signal, reason, stop_level = "⚪️ HOLD/NEUTRAL", "Price is in a consolidation or conflicting signal zone.", "No trade recommended."

    if is_bullish_bias and is_long_confirmation:
        signal, reason, stop_level = "🟢 LONG", "Bullish bias confirmed by price over 34/50 cloud and 5/12 EMA cross.", f"Primary stop is 34/50 cloud ({latest['EMA34']:.2f}-{latest['EMA50']:.2f})."
    elif is_bearish_bias and is_short_confirmation:
        signal, reason, stop_level = "🔴 SHORT", "Bearish bias confirmed by price under 34/50 cloud and 5/12 EMA cross.", f"Primary stop is 34/50 cloud ({latest['EMA34']:.2f}-{latest['EMA50']:.2f})."
    
    logging.info(f"Generated Signal: {signal} for price ${price:.2f}")
    return {"signal": signal, "reason": reason, "stop_loss": stop_level, "current_price": price}

def create_fancy_trading_chart(data, pivots, ticker_str):
    """Creates a high-end, interactive Plotly chart."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'{ticker_str} Price Action & EMAs', 'Volume'), 
                        row_heights=[0.8, 0.2])

    # --- Main Candlestick and EMA Chart ---
    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price'), row=1, col=1)

    # EMA Clouds
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA34'], line=dict(color='rgba(0,0,0,0)'), hoverinfo='none'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], line=dict(color='rgba(0,0,0,0)'), name='34/50 Cloud', fill='tonexty', fillcolor='rgba(100, 100, 255, 0.1)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA5'], line=dict(color='rgba(0,0,0,0)'), hoverinfo='none'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA12'], line=dict(color='rgba(0,0,0,0)'), name='5/12 Cloud', fill='tonexty', fillcolor='rgba(0, 255, 100, 0.2)'), row=1, col=1)

    # Pivot Points
    pivot_colors = {"R2": "#FF5733", "R1": "#FF8C33", "PP": "white", "S1": "#33FF57", "S2": "#33FFB8"}
    for level, value in pivots.items():
        fig.add_hline(y=value, line_dash="dash", line_color=pivot_colors.get(level, "grey"),
                      annotation_text=f"{level} {value:.2f}", annotation_position="bottom right", row=1, col=1)

    # --- Volume Subplot ---
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color='lightblue'), row=2, col=1)

    # --- Final Layout Touches ---
    fig.update_layout(
        template='plotly_dark',
        height=700,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        yaxis_title='Price (USD)',
        yaxis2_title='Volume'
    )
    return fig

# --- Main Streamlit App ---
def run_analysis_for_tickers(tickers_to_analyze):
    """A helper function to run analysis and display results."""
    status_message.info(f"Fetching data for {len(tickers_to_analyze)} stock(s)... Please wait.")
    
    for ticker in tickers_to_analyze:
        st.divider()
        st.header(f"Analysis for: {ticker}")
        
        prev_day, intraday_data = get_stock_data(ticker)
        
        if prev_day is None or intraday_data is None:
            st.warning("Could not fetch complete data. Skipping.")
            continue

        pivots = calculate_pivot_points(prev_day)
        intraday_data = calculate_emas(intraday_data)
        signal_info = get_ripster_signal(intraday_data)
        
        col1, col2 = st.columns([1, 2.5]) # Give more space to the chart
        with col1:
            st.metric(label="Current Price", value=f"${signal_info['current_price']:.2f}")
            st.metric(label="Signal", value=signal_info['signal'])
            with st.expander("Signal & Risk Details", expanded=True):
                st.write(f"**Reason:** {signal_info['reason']}")
                st.write(f"**Risk/Stop:** {signal_info['stop_loss']}")
            with st.expander("Daily Pivot Levels"):
                st.json(pivots)
        with col2:
            chart = create_fancy_trading_chart(intraday_data, pivots, ticker)
            st.plotly_chart(chart, use_container_width=True)
            
    status_message.success("✅ Analysis Complete!")

st.set_page_config(page_title="Trading Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("🚀 Advanced Trading Analysis Dashboard")
st.write("Combines Ripster's EMA Cloud strategy with Daily Pivot Points on interactive charts.")

try:
    with open('watchlist.txt', 'r') as f:
        watchlist = [""] + [line.strip().upper() for line in f if line.strip()]
except FileNotFoundError:
    st.error("`watchlist.txt` not found. Please create it.")
    st.stop()

# --- UI for Selecting Analysis Type ---
st.sidebar.header("Analysis Options")
selected_ticker = st.sidebar.selectbox("Analyze a Single Stock", watchlist)

if st.sidebar.button("Analyze Selected Stock"):
    if selected_ticker:
        status_message = st.empty()
        run_analysis_for_tickers([selected_ticker])
    else:
        st.sidebar.warning("Please select a stock from the dropdown.")

if st.sidebar.button("Analyze All Stocks", type="primary"):
    status_message = st.empty()
    run_analysis_for_tickers(watchlist[1:]) # Exclude the initial empty string