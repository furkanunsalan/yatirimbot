"""
This module provides functions to fetch and send BIST100 (Istanbul Stock Exchange) data for opening and closing times.

It uses the yfinance library to fetch stock data and the matplotlib library to generate a 7-day graph.
"""
from datetime import datetime, timedelta
import yfinance as yf
from io import BytesIO
from matplotlib import pyplot as plt
from src.email_utils import send_email
from src.lib.utils import get_date, get_turkish_month, get_stock_emoji_and_text
import logging

# Configure logging
logger = logging.getLogger(__name__)

def generate_bist_graph():
    """Generate a 7-day graph with 3-hour intervals for BIST100 Stock Exchange."""
    try:
        logger.info("Generating 7-day graph for BIST100.")
        end_date = datetime.today().strftime("%Y-%m-%d")
        start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        stock_data = yf.download("XU100.IS", start=start_date, end=end_date, interval="15m")

        # Resample data to 3-hour intervals and interpolate missing values
        stock_data_3h = stock_data["Close"].resample("1h").mean().interpolate(method="time")

        # Plotting the graph
        plt.figure(figsize=(12, 6))
        plt.plot(stock_data_3h.index, stock_data_3h.values, linestyle="-")
        plt.title("BIST 100 7 Günlük Grafik")
        plt.xlabel("Tarih")
        plt.ylabel("Fiyat (TL)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot
        image_stream = BytesIO()
        plt.savefig(image_stream, format="png")
        # plt.show()
        image_stream.seek(0)
        logger.info("7-day graph generated successfully.")
        return image_stream
    except Exception as e:
        logger.error(f"Failed to generate BIST graph: {e}")
        raise


def get_bist_open():
    """Fetch the change of BIST100 between previous close and opening."""
    try:
        logger.info("Fetching BIST100 opening data.")
        xu100 = yf.Ticker("XU100.IS")
        xu100_open = xu100.info.get("open", 0)
        xu100_last_close = xu100.info.get("previousClose", 0)
        if xu100_open == 0 or xu100_last_close == 0:
            raise ValueError("Missing opening or previous close data.")
        xu100_change = ((xu100_open - xu100_last_close) / xu100_last_close) * 100
        logger.info(f"BIST100 opening data retrieved: Open: {xu100_open}, Change: {xu100_change}%")
        return round(xu100_open, 2), round(xu100_change, 2)
    except Exception as e:
        logger.error(f"Failed to retrieve BIST open data: {e}")
        raise


def send_bist_open():
    """Format the text and send them with a 7-day graph of BIST100."""
    try:
        logger.start("RUNNING send_bist_open")
        today_date = get_date()
        day = today_date.strftime("%d")
        day = day[1:] if day.startswith("0") else day
        month = get_turkish_month(today_date.strftime("%B"))
        bist_open, bist_change = get_bist_open()
        emo, text = get_stock_emoji_and_text(bist_change)
        subject = "send_bist100_open #bist"
        body = f"""🔴 #BIST100 {day} {month} tarihinde güne %{bist_change} {text} ile başladı.

{emo} Açılış Fiyatı: {bist_open}
        """
        image = generate_bist_graph()

        # Send email without additional logging
        # send_email(subject, body, image)
        print(body)
        logger.ok("send_bist_open worked successfully.")
    except Exception as e:
        logger.error(f"Failed to run send_bist_open: {e}")
        raise


def get_bist_close():
    """Fetch the current value and previous close value of the exchange and calculate daily change rate."""
    try:
        logger.info("Fetching BIST100 closing data.")
        xu100 = yf.Ticker("XU100.IS")
        xu100_data = xu100.history(period="max")
        xu100_current = xu100_data["Close"][-1]
        xu100_prev = xu100_data["Close"][-2]
        xu100_current_change = ((xu100_current - xu100_prev) / xu100_prev) * 100
        logger.info(f"BIST100 closing data retrieved: Current: {xu100_current}, Change: {xu100_current_change}%")
        return round(xu100_current, 2), round(xu100_current_change, 2)
    except Exception as e:
        logger.error(f"Failed to retrieve BIST closing data: {e}")
        raise


def send_bist_close():
    """Format the text and send them with a 7-day graph of BIST100."""
    try:
        logger.start("Running send_bist_close")
        today_date = get_date()
        day = today_date.strftime("%d")
        day = day[1:] if day.startswith("0") else day
        month = get_turkish_month(today_date.strftime("%B"))
        bist_close, bist_change = get_bist_close()
        emo, text = get_stock_emoji_and_text(bist_change)
        subject = "send_bist100_close #bist"
        body = f"""🔴 #BIST100 {day} {month} tarihinde günü %{bist_change} {text} ile kapattı.

{emo} Kapanış Fiyatı: {bist_close}
        """
        image = generate_bist_graph()

        send_email(subject, body, image)
        # print(body)
        logger.ok("send_bist_close worked successfully.")
    except Exception as e:
        logger.error(f"Failed to run send_bist_close: {e}")
        raise


if __name__ == "__main__":
    send_bist_open()
    send_bist_close()
