Advanced Trading Analysis Dashboard

This project is an interactive web application built with Python and Streamlit that serves as a powerful analysis tool for day traders. It combines the Ripster EMA Cloud trend-following strategy with classic Daily Pivot Points to generate actionable trading signals and visualizes them on high-end, interactive charts.

The application allows users to analyze stocks from a personal watchlist, either individually or all at once, providing a comprehensive overview of potential trading opportunities.

(You can replace this with a screenshot of your own running application)

Features

Interactive Web Interface: A clean, professional dashboard built with Streamlit.
Flexible Analysis: Choose to analyze a single stock from a dropdown or all stocks from your watchlist with a single click.
Ripster EMA Cloud Strategy: Automatically calculates and displays the 5/12, 8/9, and 34/50 EMA clouds on a 15-minute chart.
Daily Pivot Point Analysis: Calculates and overlays key support (S1, S2), resistance (R1, R2), and the main pivot point (PP) based on the previous day's price action.
Actionable Trading Signals: Generates clear LONG, SHORT, or HOLD/NEUTRAL signals based on a confluence of the Ripster EMA rules.
High-End Interactive Charting: For each stock, a Plotly chart visualizes:
Candlestick price data.
Shaded, color-coded EMA clouds.
Labeled horizontal lines for all pivot levels.
An integrated volume subplot.
Detailed hover-over data points.
Debug Logging: Integrated Python logging provides detailed output in the terminal for easy troubleshooting.
Secure & Organized: Uses a .env file to securely manage API keys and a requirements.txt file for easy dependency management.

Technologies Used

Python 3.x
Streamlit: For building the interactive web application.
yfinance: To fetch historical stock price and volume data from Yahoo Finance.
Pandas: For data manipulation and analysis.
Plotly: For creating advanced, interactive visualizations and charts.
python-dotenv: For managing environment variables and API keys securely.

Setup and Installation

Follow these steps to set up and run the project on your local machine.

1. Clone the Repository

First, clone this repository to your local machine (or simply create a project folder and add the files).

```bash
git clone https://github.com/kranthik123/Advanced-Trading-Analysis.git
cd advanced-trading-dashboard
```

2. Create a Virtual Environment

It is highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install Dependencies

Install all the required Python packages using the requirements.txt file.

```bash
pip install -r requirements.txt
```

4. Create Your Watchlist

Create a file named watchlist.txt in the root directory of the project. Add the stock tickers you want to analyze, one per line.

Example watchlist.txt:

```
AAPL
MSFT
NVDA
AMD
TSLA
SPY
QQQ
```

5. Run the Application

Once the setup is complete, run the Streamlit application from your terminal.

```bash
streamlit run app.py
```

Your default web browser will automatically open a new tab with the running dashboard.

How to Use the Dashboard

Launch the application using the command above.
The application will open with a sidebar on the left.

To analyze a single stock:

Select a ticker from the "Analyze a Single Stock" dropdown menu.
Click the "Analyze Selected Stock" button.

To analyze all stocks:

Click the primary blue button "Analyze All Stocks".
The analysis will appear in the main window, with a detailed breakdown and an interactive chart for each stock. You can zoom, pan, and hover over the chart to inspect data points.

Project Structure

```
.
├── .gitignore         # Specifies files for Git to ignore
├── app.py             # The main Streamlit application script
├── README.md          # This file
├── requirements.txt   # List of Python dependencies
└── watchlist.txt      # Your personal list of stock tickers
