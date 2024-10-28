"""
This module retrieves stock information for Turkish companies and sends an email summary.

It uses the yfinance library to fetch stock data and a custom email utility to send the report.
"""

from datetime import datetime
import pytz
import yfinance as yf
from src.email_utils import send_email
from src.lib.utils import get_turkish_month
import logging

logger = logging.getLogger(__name__)

def format_day(day):
    """Remove leading zero from day if present."""
    return day[1:] if day.startswith("0") else day


def get_stock_data(stock_code):
    """Retrieve stock data for a given stock code."""
    hisse = yf.Ticker(stock_code + ".IS")
    logger.info(f"Fetching stock data for {stock_code}.")
    try:
        hisse_data = hisse.history(period="max")
        hisse_close_list = hisse_data["Close"][-3:].tolist()
        logger.info(f"Successfully fetched stock data for {stock_code}: {hisse_close_list}")
        return hisse_close_list
    except Exception as e:
        logger.error(f"Error fetching data for {stock_code}: {e}")
        return []


def calculate_change(current, previous):
    """Calculate percentage change between two values."""
    try:
        change = round(((current - previous) / previous) * 100, 2)
        logger.info(f"Calculated change: {change}% between {previous} and {current}")
        return change
    except ZeroDivisionError as e:
        logger.error(f"Error calculating change: {e}")
        return 0


def halka_arz():
    """
    Generate and send a daily report on Turkish stock performance.

    This function retrieves stock data for specified Turkish companies,
    calculates their daily performance, and sends an email summary.
    """
    logger.start("Running halka_arz")
    timezone = pytz.timezone("Europe/Istanbul")
    today_date = datetime.now(timezone)
    day = format_day(today_date.strftime("%d"))
    month = get_turkish_month(today_date.strftime("%B"))

    stocks = ["RGYAS", "ODINE", "MOGAN", "ARTMS", "ALVES", "LMKDC"]
    subject = "halka_arz_tablosu #test ##test"
    body = f"🔴 {day} {month} Halka Arz Tablosu \n\n"

    for stock in reversed(stocks):
        hisse_close_list = get_stock_data(stock)
        if len(hisse_close_list) < 3:
            logger.warning(f"Insufficient data for {stock}. Skipping...")
            body += f"⚠️ #{stock} Yeterli veri yok\n"
            continue

        hisse_current, hisse_prev = hisse_close_list[2], hisse_close_list[1]
        change_rate = calculate_change(hisse_current, hisse_prev)

        emoji = "📈" if change_rate > 0 else "📉"
        text = "yükseldi" if change_rate > 0 else "düştü"
        tavan_check = " - Hisse Tavanda" if change_rate > 9.5 else ""

        message = f"{emoji} #{stock} bugün %{change_rate} {text}{tavan_check}\n"
        body += message
        logger.info(f"Appended performance data for {stock}: {message.strip()}")

    try:
        # send_email(subject, body)
        print(body)
        logger.ok("halka_arz worked successfully")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")


if __name__ == "__main__":
    halka_arz()
