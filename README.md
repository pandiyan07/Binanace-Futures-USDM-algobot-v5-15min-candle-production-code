# Binance Futures Algorithmic Trading Bot (BTCUSDT)

## Table of Contents
- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Technologies Used (Prerequisites)](#technologies-used-prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Main Python Functions](#main-python-functions)
- [Output that can be expected](#output-that-can-be-expected)
- [Configuration](#configuration)
- [Version History (changes between each version)](#version-history-changes-between-each-version)
- [Future Roadmap](#future-roadmap)
- [License Description](#license-description)
- [Disclaimer](#disclaimer)

---

## About The Project
The **Binance Futures Algorithmic Trading Bot (BTCUSDT)** is an automated trading application built in Python and Flask for USD-M Futures trading on Binance 15 minute candle timeframe. It fetches `15m` candlestick data for `BTCUSDT`, computes technical indicators (`EMA`, `SMA`, and `ATR` on `oc2` / OHLC values), evaluates long and short entry/exit rules, and executes market orders alongside stop-loss and trailing stop-loss orders.

The application also runs a background scheduler (`APScheduler`) for periodic indicator updates, trade logic loops, and end-of-day reporting, paired with a Flask web interface for viewing current position status and trade logs, plus SMTP email alerts for order events, errors, and daily summaries.

---

## Built With
* [Python](https://www.python.org/) — Core application logic and automation
* [Flask](https://flask.palletsprojects.com/) — Web server and HTML dashboard rendering
* [APScheduler](https://apscheduler.readthedocs.io/) — Background interval and cron job scheduling (`Asia/Kolkata`)
* [Binance Futures Connector (`binance-futures-connector`)](https://github.com/binance/binance-futures-connector-python) — Binance USD-M Futures REST API client (`UMFutures`)
* [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) — DataFrame manipulation and trade log processing
* [pandas_ta](https://github.com/twopirllc/pandas-ta) — Technical analysis indicators (`ema`, `sma`, `atr`)
* [python-dotenv](https://github.com/theskumar/python-dotenv) — Environment variable loading from `.env`
* [OpenPyXL](https://openpyxl.readthedocs.io/) — Excel (`.xlsx`) export for daily trade reports

---

## Key Features
* **Automated Signal & Trade Execution:** Evaluates long and short entry conditions and exit crossovers (`ema_5` vs. `sma_34`, trailing stop thresholds, and `ATR` volatility filtering) to place `MARKET` orders (`0.002` `BTCUSDT` default).
* **Stop-Loss & Trailing Stop Management:** Automatically places a fallback `STOP_MARKET` order upon market order fill and a `TRAILING_STOP_MARKET` order with a configured callback rate.
* **Position & Order Cleanup:** Checks active positions and order statuses, cancels remaining open orders on exit, and provides startup cleanup (`UNWANTED_POSITION_CLOSER`) for pre-existing positions or open orders.
* **Scheduled Automation:** Uses `APScheduler` in `Asia/Kolkata` timezone to refresh market data and indicators every 900 seconds, run trading logic every 60 seconds, and trigger a daily report dump at `23:35`.
* **Flask Web Dashboard:** Serves status messages and HTML tables for today's trades and overall trade history via dedicated Jinja2 templates.
* **Email & Error Reporting:** Sends HTML emails with optional Excel/log attachments on bot start, order placement, order closure, pre-existing order cleanup, daily report dumps, and runtime exceptions.

---

## Getting Started

### Technologies Used (Prerequisites)
* **Python 3.9+** and `pip`
* **Binance USD-M Futures Account** with API Key and Secret Key enabled for Futures
* **SMTP Email Credentials** (such as a Gmail account with an App Password) for notifications
* **Packages listed in `requirements_2.txt`:** `flask`, `gunicorn`, `apscheduler`, `openpyxl`, `pandas`, `pandas_ta`, `numpy`, `requests`, `pytz`, `binance-futures-connector`, `python-dotenv`

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/pandiyan07/Binanace-Futures-USDM-algobot-v5-15min-candle-production-code
   cd Binanace-Futures-USDM-algobot-v5-15min-candle-production-code
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux / macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements_2.txt
   ```

4. **Configure environment variables:**
   Update `.env` with your Binance Futures API credentials (and SMTP settings if externalized):
   ```env
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_SECRET_KEY=your_binance_secret_key
   ```

### Usage
1. Ensure `.env` contains valid `BINANCE_API_KEY` and `BINANCE_SECRET_KEY` values and your trading parameters match your account settings.
2. Start the Flask application and scheduler:
   ```bash
   python MASTER__FILE_2.py
   ```
   *(Note: If you run the `*_2.py` files directly as uploaded, verify module import names match your filenames in the working directory.)*
3. Open `http://localhost:5000` (or `http://<server-ip>:5000`) in your browser to view the dashboard, which auto-refreshes every 60 seconds.

---

## Project Structure
This repository contains **18 files**:

```text
├── MASTER__FILE_2.py                          # Main Flask app, APScheduler setup, and TRADING_ALGO_BOT loop
├── misc_bin_func_2.py                         # Binance account, precision, position, order status, and trade helpers
├── new_order_placer_2.py                      # Basic market order placement and startup position/order cleanup
├── order_closer_2.py                          # Position exit logic and SL/TSL order cancellation helpers
├── order_placer_2.py                          # Market entry flow, fill price polling, and fallback STOP_MARKET placement
├── trading_journal_2.py                       # Trade record DataFrame formatting helper (TRADE_LOGGER)
├── trading_logic_2.py                         # Entry/exit state transitions and EMA/TSL exit evaluation
├── trading_rules_2.py                         # Long/short entry condition rules using EMA, SMA, and ATR
├── tsl_setter_2.py                            # Trailing stop-loss (`TRAILING_STOP_MARKET`) placement logic
├── data_fetcher_2.py                          # Fetches 40 `15m` klines for `BTCUSDT` via Binance UMFutures REST API
├── emailer_2.py                               # Logging/traceback setup (`ERROR_FLOWCHART`) and SMTP email sender (`EMAIL_SENDER`)
├── indicator_calculation_2.py                 # Computes `ema_5`, `sma_34`, and `atr` indicators using `pandas_ta`
├── requirements_2.txt                         # Pinned Python dependencies for the project
├── .env                                       # Environment variable file for API keys (ignored by Git)
├── .gitignore                                 # Git ignore rules (excludes `.env`)
├── btcusdt_binance_futures_dummy_homepage_2.html # Fallback template shown when no finished trade data exists yet
├── btcusdt_binance_futures_homepage_2.html    # Main dashboard template displaying today's and all executed trades
└── homepage_2.html                            # Minimal status-only HTML template with 60-second auto-reload
```

### Brief Content Briefing of Each Python File
* **`MASTER__FILE_2.py`**: Initializes the Flask app (`binance_btcusdt_futures_app`), loads `.env` API keys, creates the `UMFutures` client, configures `BackgroundScheduler` (`Asia/Kolkata`), runs `TRADING_ALGO_BOT()`, `SCHEDULED_TASKS()`, `FAST_SCHEDULED_TASKS()`, and `DATA_DUMPER()`, and defines the `/` web route.
* **`data_fetcher_2.py`**: Defines `REST_API_DATFET()`, which queries Binance `UMFutures` for the last 40 `15m` candles of `BTCUSDT` and returns a `pandas.DataFrame` with `open`, `high`, `low`, `close`, and formatted `close_time`.
* **`indicator_calculation_2.py`**: Uses `pandas_ta` to compute `oc2` (`(open + close) / 2`), `ema_5`, `sma_34`, and `atr`, returning the updated DataFrame via `INDICATOR_CALCULATOR()`.
* **`trading_rules_2.py`**: Implements `CONDITION_VERIFIER(df)` to check `ATR > 210` along with `ema_5` vs. `sma_34` spread and `sma_34` lookback movement thresholds for long and short entries.
* **`trading_logic_2.py`**: Implements `ENTRY_WORK()`, `EXITING_WORK()`, and `TRADING_LOGIC()` to set `LONG`/`SHORT` states, track `highest_price`/`lowest_price`, and detect EMA crossovers or trailing stop thresholds (`TSL_Long = 200`, `TSL_Short = 200`).
* **`order_placer_2.py`**: Implements `FALLBACK_PLACE_STOP_LOSS()` (`STOP_MARKET` with `reduceOnly=True`) and `OPEN_ORDER_PLACER()`, which fetches mark price, places the initial market order, polls fill price up to 10 times, and places the fallback stop-loss.
* **`tsl_setter_2.py`**: Implements `TSL_APPLIER()` and `TSL_ORDER_PLACER()` to submit a `TRAILING_STOP_MARKET` order (`callbackRate=1`) with retry attempts.
* **`order_closer_2.py`**: Implements `OC()` and `CLOSE_ORDER_PLACER()` to verify order statuses, place a closing order if SL/TSL hasn't already triggered, cancel open SL/TSL orders, and confirm positions are closed.
* **`new_order_placer_2.py`**: Provides `NEW_ODR_PLCR()` for rounded market orders and `UNWANTED_POSITION_CLOSER()` to close open positions and cancel `NEW` orders on startup or cleanup.
* **`misc_bin_func_2.py`**: Contains Binance Futures helper functions including `GET_ACCOUNT_BALANCE()`, `SET_LEVERAGE()`, `SET_MARGIN_TYPE()`, `GET_PRICE_PRECISION()`, `GET_QUANTITY_PRECISION()`, `CHECK_FOR_ACTIVE_POSITIONS()`, `CHECK_ORDER_STATUS()`, `FETCH_ORDER_FILL_PRICE()`, and `FETCH_ACCOUNT_TRADES()`.
* **`trading_journal_2.py`**: Defines `TRADE_LOGGER()` to format trade execution timestamps and append trade entries into a `pandas.DataFrame`.
* **`emailer_2.py`**: Configures logging (`binfut_trading_bot.log`), writes error tracebacks via `ERROR_FLOWCHART()`, and sends SMTP email notifications (`EMAIL_SENDER()`) for order events, errors, startup IP/position info, and daily Excel reports.

---

## How It Works
1. **Startup & Initialization (`HOME_PAGE` in `MASTER__FILE_2.py`):** On the first request to `/`, the bot checks USDT balance, fetches initial `15m` klines and indicators, retrieves price/quantity precision, sets leverage (`5x` on `BTCUSDT`), checks active positions and open orders, runs cleanup if needed, starts the `APScheduler` jobs, and loads account trade history.
2. **Scheduled Market & Indicator Refresh:** `SCHEDULED_TASKS` runs every 900 seconds to fetch fresh `BTCUSDT` `15m` candles and recalculate `ema_5`, `sma_34`, and `atr`.
3. **Trading Cycle:** `FAST_SCHEDULED_TASKS` runs every 60 seconds and calls `TRADING_ALGO_BOT()`, which evaluates `CONDITION_VERIFIER(df)` and `TRADING_LOGIC(...)`.
4. **Opening a Trade:** When `action == 'ENTER_TRADE'` and `Initital_trade_lock` is `False`, `OPEN_ORDER_PLACER` submits the market order, retrieves the fill price, places a fallback `STOP_MARKET` order, and `TSL_ORDER_PLACER` submits a `TRAILING_STOP_MARKET` order, followed by an `ORDER PLACED` email alert.
5. **Monitoring & Exiting:** While `action == 'POSITION_IS_LIVE'`, the bot checks for active positions and order statuses. Once no live position remains (`action == 'EXIT_TRADE'`), `CLOSE_ORDER_PLACER` cancels any still-open SL/TSL orders, resets trade state variables, refreshes account trades, and sends an `ORDER CLOSED` email alert.
6. **End-of-Day Report:** `DATA_DUMPER` is scheduled at `23:35` (`Asia/Kolkata`) to filter today's trades and email an Excel report (`daily_report.xlsx`) when no live position is active.

---

## Main Python Functions
* **`TRADING_ALGO_BOT()`** (`MASTER__FILE_2.py`): Main state machine coordinating signal checks, order entry, live position monitoring, trade exit, cleanup, and error handling.
* **`HOME_PAGE()`** (`MASTER__FILE_2.py`): Flask route handler for `/` that initializes the bot/scheduler on first load and renders the trade dashboard HTML templates.
* **`REST_API_DATFET()`** (`data_fetcher_2.py`): Fetches 40 `15m` candlesticks for `BTCUSDT` from Binance `UMFutures` and returns them as a formatted DataFrame.
* **`INDICATOR_CALCULATOR()`** (`indicator_calculation_2.py`): Computes `oc2`, `ema_5`, `sma_34`, and `atr` columns on the OHLC DataFrame.
* **`CONDITION_VERIFIER()`** (`trading_rules_2.py`): Evaluates long and short entry conditions based on `ema_5`, `sma_34`, and `atr`.
* **`TRADING_LOGIC()`** (`trading_logic_2.py`): Manages `LONG`/`SHORT` entry and exit decisions using EMA crossovers and trailing stop thresholds.
* **`OPEN_ORDER_PLACER()` & `FALLBACK_PLACE_STOP_LOSS()`** (`order_placer_2.py`): Places the initial market order, polls fill price, and attaches a `STOP_MARKET` fallback order.
* **`TSL_ORDER_PLACER()` & `TSL_APPLIER()`** (`tsl_setter_2.py`): Places a `TRAILING_STOP_MARKET` order with retry attempts.
* **`CLOSE_ORDER_PLACER()` & `OC()`** (`order_closer_2.py`): Handles order status checks, closing orders, and cancellation of open SL/TSL orders.
* **`UNWANTED_POSITION_CLOSER()` & `NEW_ODR_PLCR()`** (`new_order_placer_2.py`): Submits rounded market orders and closes open positions or cancels open orders.
* **`CHECK_FOR_ACTIVE_POSITIONS()`, `CHECK_ORDER_STATUS()`, & `FETCH_ACCOUNT_TRADES()`** (`misc_bin_func_2.py`): Queries live positions, order states, and executed account trades with `realizedPnl` and `commission` totals.
* **`EMAIL_SENDER()` & `ERROR_FLOWCHART()`** (`emailer_2.py`): Records error tracebacks to `error_log.txt` and sends HTML email alerts with optional attachments over SMTP.

---

## Output that can be expected
* **Console & Log File (`binfut_trading_bot.log`):** Timestamped `INFO` and `ERROR` logs showing scheduled task execution, indicator/position states, order IDs, and exception details, plus `error_log.txt` when tracebacks are captured.
* **Web Dashboard (`http://<host>:5000`):** Renders `btcusdt_binance_futures_dummy_homepage_2.html` when no finished trade data is available, or `btcusdt_binance_futures_homepage_2.html` showing position status and HTML tables (`class="data"`) for today's trades and all historical trades.
* **Email Notifications & Excel Export:** HTML emails for `START`, `ORDER PLACED`, `ORDER CLOSED`, `PRE-EXISTING ORDER CLOSED`, `ERROR`, and `DUMP` (including `daily_report.xlsx` when trades exist for the day).

---

## Configuration
Key parameters currently configured across the codebase:

| Parameter / Setting | Location | Current / Default Value | Purpose |
| :--- | :--- | :--- | :--- |
| `BINANCE_API_KEY` / `BINANCE_SECRET_KEY` | `.env`, `MASTER__FILE_2.py` | Loaded via `python-dotenv` | Authenticates the Binance `UMFutures` client |
| `input` tuple | `MASTER__FILE_2.py` | `("BTCUSDT", "MARKET", 0.002, 90, 70, 'ISOLATED', 5)` | Symbol, order type, quantity, long/short TSL values, margin mode, leverage |
| Interval & Candle Limit | `data_fetcher_2.py` | `"15m"`, `limit=40` | Timeframe and number of klines fetched for `BTCUSDT` |
| Indicator Lengths | `MASTER__FILE_2.py`, `indicator_calculation_2.py` | `atr_len=14`, `small_ema_len=5`, `large_ema_len=34` | Lookback periods for `ATR`, `EMA`, and `SMA` |
| Entry Thresholds | `trading_rules_2.py` | `ATR > 210`, MA deviations `150`/`100`, SMA diff `200` | Volatility and moving-average separation rules |
| Trailing Stop Parameters | `trading_logic_2.py`, `tsl_setter_2.py` | `TSL_Long = 200`, `TSL_Short = 200`, `callbackRate = 1` | Exit trailing thresholds and Binance trailing callback rate |
| Fallback Stop Distance | `order_placer_2.py` | `sl_distance = 500` | Price offset used for `STOP_MARKET` fallback order |
| Scheduler Intervals & Cron | `MASTER__FILE_2.py` | `900s`, `60s`, daily `23:35` (`Asia/Kolkata`) | Indicator refresh, trading bot loop, and daily report dump |
| Flask Host & Port | `MASTER__FILE_2.py` | `host='0.0.0.0'`, `port=5000` | Web server binding address and port |

---

## Version History (changes between each version)
* **v1.x (`*_2.py` / `*_2.html` Repository Snapshot):**
  * Modularized trading execution across `MASTER__FILE_2.py`, `misc_bin_func_2.py`, `new_order_placer_2.py`, `order_closer_2.py`, `order_placer_2.py`, `trading_journal_2.py`, `trading_logic_2.py`, `trading_rules_2.py`, `tsl_setter_2.py`, `data_fetcher_2.py`, `emailer_2.py`, and `indicator_calculation_2.py`.
  * Added `APScheduler` background jobs (`SCHEDULED_TASKS`, `FAST_SCHEDULED_TASKS`, and `DATA_DUMPER`) in `Asia/Kolkata`.
  * Added Flask dashboard templates (`btcusdt_binance_futures_dummy_homepage_2.html`, `btcusdt_binance_futures_homepage_2.html`, and `homepage_2.html`) with 60-second auto-refresh.
  * Added `requirements_2.txt`, `.env`, and `.gitignore` for dependency tracking and `.env` exclusion.

---

## Future Roadmap
- [ ] Move SMTP sender/receiver credentials and app passwords out of `emailer_2.py` into environment variables, and rotate any exposed credentials.
- [ ] Align module import names and filename conventions across the codebase (or package them cleanly) and add unit/integration tests.
- [ ] Serve the Flask app with a production WSGI server (such as `gunicorn` included in `requirements_2.txt`) and proper process supervision.
- [ ] Add paper-trading / testnet mode and historical backtesting support before live capital deployment.
- [ ] Centralize configuration constants and fix minor edge cases (such as CSS syntax in `btcusdt_binance_futures_homepage_2.html` and exception handling retries in `EMAIL_SENDER`).

---

## License Description
No `LICENSE` file is currently included in this repository. Until a license file is added, all rights are reserved by the repository owner by default. If you intend for others to view, fork, or modify the code, add a standard license file (such as the **MIT License**) and update this section accordingly.

---

## Disclaimer
Trading cryptocurrency futures involves substantial financial risk and can result in rapid and significant losses, including loss of your entire invested capital. This project is provided for educational and informational purposes only and does not constitute financial, investment, or legal advice. Automated trading bots can experience software bugs, network/API latency, exchange outages, slippage, or unexpected market volatility. Always test thoroughly on a testnet or with minimal risk capital, and use this software at your own risk.
