"""
This module provides functions to fetch and send US market data for opening and closing times.

It uses the yfinance library to fetch market data and a custom email utility to send the information.
"""
import logging
from datetime import datetime
import pytz
import yfinance as yf
from src.email_utils import send_email
from src.lib.utils import get_turkish_month

# Configure logger
logger = logging.getLogger(__name__)

def get_market_data(ticker):
    """Fetch market data for a given ticker."""
    try:
        logger.info(f"Fetching data for ticker: {ticker}")
        ticker_data = yf.Ticker(ticker)
        current = ticker_data.info.get('open', 0)
        previous = ticker_data.info.get('previousClose', 0)
        if previous == 0:
            logger.warning(f"Previous close price not available for {ticker}")
            return 0, 0, 0.0
        change = round(((current - previous) / previous) * 100, 2)
        logger.info(f"Data for {ticker} - Current: {current}, Previous: {previous}, Change: {change}%")
        return current, previous, change
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return 0, 0, 0.0

def format_market_data(name, change):
    """Format market data for email body."""
    emoji = "📈" if change > 0 else "📉"
    formatted_data = f"\n{emoji} {name}: %{change}"
    logger.info(f"Formatted data for {name}: {formatted_data}")
    return formatted_data

def us_open():
    """Fetch and send US market opening data."""
    logger.start("Running us_open")
    try:
        turkey_tz = pytz.timezone("Europe/Istanbul")
        today = datetime.now(turkey_tz)
        day = today.strftime("%d").lstrip("0")
        month = get_turkish_month(today.strftime("%B"))

        subject = "send_us_open #us"
        body = f"🔴 {day} {month} ABD Endeksleri Açılış Verileri 👇\n\n"

        for ticker, name in [("^IXIC", "NASDAQ"), ("^GSPC", "S&P 500"), ("^DJI", "Dow Jones")]:
            _, _, change = get_market_data(ticker)
            body += format_market_data(name, change)

        body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"
        send_email(subject, body)
    except Exception as e:
        logger.error(f"Failed to send US market opening data: {e}")
    finally:
        logger.ok("US market opening email sent successfully.")

def us_close():
    """Fetch and send US market closing data."""
    logger.start("Running us_close")
    try:
        turkey_tz = pytz.timezone("Europe/Istanbul")
        today = datetime.now(turkey_tz)
        day = today.strftime("%d").lstrip("0")
        month = get_turkish_month(today.strftime("%B"))

        subject = "send_us_close #us"
        body = f"🔴 {day} {month} ABD Endeksleri Kapanış Verileri 👇\n\n"

        for ticker, name in [("^IXIC", "NASDAQ"), ("^GSPC", "S&P 500"), ("^DJI", "Dow Jones")]:
            try:
                ticker_data = yf.Ticker(ticker).history(period="max")
                current = ticker_data["Close"].iloc[-1]
                previous = ticker_data["Close"].iloc[-2]
                change = round(((current - previous) / previous) * 100, 2)
                body += format_market_data(name, change)
                logger.info(f"Fetched closing data for {name} - Current: {current}, Previous: {previous}, Change: {change}%")
            except Exception as e:
                logger.error(f"Failed to fetch closing data for {ticker}: {e}")
                body += f"\n⚠️ {name} data could not be retrieved.\n"

        body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"
        send_email(subject, body)
        logger.info("US market closing email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send US market closing data: {e}")
    finally:
        logger.ok("US market closing email sent successfully.")

if __name__ == "__main__":
    us_open()
    us_close()
