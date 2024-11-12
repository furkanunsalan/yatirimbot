"""
This module provides functionality to fetch, analyze, and report silver price data.

It includes functions to retrieve historical silver price data, plot the data,
calculate daily price changes, and send email reports with the analysis.
"""

import logging
from io import BytesIO
import yfinance as yf
from matplotlib import pyplot as plt
from src.email_utils import send_email

# Set up logging configuration
logger = logging.getLogger(__name__)

def get_silver_data():
    """
    Fetch historical silver price data.

    Returns:
        pandas.DataFrame: Historical silver price data.
    """
    try:
        logger.info("Fetching historical silver price data.")
        silver_ticker = yf.Ticker("SI=F")
        data = silver_ticker.history(period="max")
        if data.empty:
            logger.warning("No data returned for silver prices.")
        return data
    except Exception as e:
        logger.error(f"Failed to fetch silver price data: {e}")
        return None

def plot_silver_data(silver_data):
    """
    Create a plot of historical silver prices.

    Args:
        silver_data (pandas.DataFrame): Historical silver price data.

    Returns:
        BytesIO: The image stream of the plot.
    """
    try:
        logger.info("Generating plot for silver prices.")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(silver_data["Close"], label="Gümüş Son Fiyat ($)")
        ax.set_title("Tarihsel Gümüş Fiyatları")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("Fiyat ($)")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        image_stream = BytesIO()
        plt.savefig(image_stream, format="png")
        plt.close()
        image_stream.seek(0)
        logger.info("Silver price plot generated successfully.")
        return image_stream
    except Exception as e:
        logger.error(f"Failed to create plot for silver prices: {e}")
        return None

def calculate_daily_change(silver_data):
    """
    Calculate the daily percentage change in silver price.

    Args:
        silver_data (pandas.DataFrame): Historical silver price data.

    Returns:
        float: Daily percentage change in price, or 0 if data is insufficient.
    """
    try:
        if len(silver_data) > 1:
            last_close = silver_data["Close"].iloc[-1]
            prev_close = silver_data["Close"].iloc[-2]
            daily_change = (last_close - prev_close) / prev_close * 100
            logger.info(f"Calculated daily change: {daily_change:.2f}%")
            return daily_change
        logger.warning("Not enough data to calculate daily change.")
        return 0
    except Exception as e:
        logger.error(f"Failed to calculate daily change: {e}")
        return 0

def analyze_silver_prices():
    """Analyze silver prices, generate a report, and send it via email."""
    logger.start("Starting analyze_silver_prices")
    try:
        silver_data = get_silver_data()
        if silver_data is None or silver_data.empty:
            logger.error("No silver data available. Email report will not be sent.")
            return

        last_price = silver_data["Close"].iloc[-1]
        daily_change = calculate_daily_change(silver_data)

        email_body = (
            "🔴 #Gümüş:\n"
            f"Son Fiyat: ${last_price:.2f}\n"
            f"Günlük Değişim: {daily_change:.2f}%\n"
        )

        image_stream = plot_silver_data(silver_data)
        if image_stream is None:
            logger.error("Failed to generate plot image for email. Sending email without image.")
            send_email("Güncel Gümüş Fiyatları #silver", email_body)
        else:
            send_email("Güncel Gümüş Fiyatları #silver", email_body, image_stream)
        
        logger.ok("Silver price report email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to analyze and report silver prices: {e}")

if __name__ == "__main__":
    analyze_silver_prices()
