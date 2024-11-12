"""
This module fetches and sends gold price data, including a historical price chart.

It uses the CollectAPI for current gold prices and yfinance for historical data.
"""

import http.client
import json
from io import BytesIO
from datetime import datetime

import pytz
import matplotlib.pyplot as plt
import yfinance as yf

from src.email_utils import send_email
from src.lib.utils import get_turkish_month
import logging

# Set up logger for debugging
logger = logging.getLogger(__name__)

def fetch_gold_data():
    """Fetch current gold price data from CollectAPI."""
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        "content-type": "application/json",
        "authorization": "apikey 1XxDAz4EtnKZ099rPKM8Jj:2se49tU9ttxzlhy1KGI5sW",
    }
    try:
        conn.request("GET", "/economy/goldPrice", headers=headers)
        res = conn.getresponse()
        if res.status != 200:
            logger.error(f"Failed to fetch gold data: HTTP {res.status}")
            return None

        data = res.read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        logger.error(f"Exception in fetching gold data: {e}")
        return None
    finally:
        conn.close()

def create_gold_chart():
    """Create a chart of historical gold prices."""
    try:
        gold = yf.Ticker("GC=F")
        hist_data = gold.history(period="1y")

        plt.figure(figsize=(12, 6))
        plt.plot(hist_data["Close"], label="Son Fiyat")
        plt.legend()
        plt.title("Ons Altın Grafiği")
        plt.ylabel("Fiyat Dolar")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        image_stream = BytesIO()
        plt.savefig(image_stream, format="png")
        plt.close()  # Close the plot to release memory
        image_stream.seek(0)
        return image_stream
    except Exception as e:
        logger.error(f"Error creating gold chart: {e}")
        return None

def gold_price():
    """Fetch gold price data, create a chart, and send an email."""
    logger.start("Running gold_price")
    try:
        turkey_tz = pytz.timezone("Europe/Istanbul")
        today_date = datetime.now(turkey_tz)
        day = today_date.strftime("%d").lstrip("0")
        month = get_turkish_month(today_date.strftime("%B"))

        # Fetching current gold price data
        parsed_data = fetch_gold_data()
        if not parsed_data or "result" not in parsed_data:
            logger.error("No valid gold data received from the API.")
            return

        # Create a chart of historical gold prices
        image_stream = create_gold_chart()
        if not image_stream:
            logger.error("Failed to create the gold price chart.")
            return

        subject = f"🔴 Altın Fiyatları {day} {month} #gold_price"
        body = "🔴 Altın Fiyatları:\n\n"
        for item in parsed_data["result"]:
            if item["name"] in ["Gram Altın", "ONS Altın", "Çeyrek Altın"]:
                body += f"💰 {item['name']}: Alış - {item['buying']}, Satış - {item['selling']}\n"

        send_email(subject, body, image_stream)
        logger.info("Gold price email sent successfully.")
        logger.ok('Gold Price Function Worked')
    except Exception as e:
        logger.error(f"An error occurred in the gold price function: {e}")

if __name__ == "__main__":
    gold_price()
