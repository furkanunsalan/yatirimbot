"""Utility functions for fetching and processing cryptocurrency data."""

import logging
from io import BytesIO
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import requests
import yfinance as yf

from src.email_utils import send_email

# Configure logger
logger = logging.getLogger(__name__)

def plot_bitcoin_graph() -> Optional[BytesIO]:
    """Generate a monthly Bitcoin price graph and return it as a BytesIO object."""
    try:
        logger.info("Generating Bitcoin monthly price graph.")
        btc = yf.Ticker("BTC-USD")
        btc_data = btc.history(period="1mo")
        plt.figure(figsize=(10, 5))
        plt.plot(btc_data["Close"], label="Son Fiyat")
        plt.title("Bitcoin Aylık Grafik")
        plt.ylabel("Dolar")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format="png")
        plt.close()
        image_buffer.seek(0)
        logger.info("Bitcoin graph generated successfully.")
        return image_buffer
    except Exception as e:
        logger.error(f"Failed to generate Bitcoin graph: {e}")
        return None

def format_price(price: float) -> str:
    """Format the given price with two decimal places and thousands separator."""
    formatted_price = f"{price:,.2f}"
    logger.info(f"Formatted price: {formatted_price}")
    return formatted_price

def format_market_cap(market_cap: float) -> str:
    """Format the market cap value with appropriate suffixes (Million, Billion, Trillion)."""
    if market_cap < 1_000_000:
        formatted_cap = f"${market_cap:,.0f}"
    elif market_cap < 1_000_000_000:
        formatted_cap = f"${market_cap / 1_000_000:.2f} Milyon"
    elif market_cap < 1_000_000_000_000:
        formatted_cap = f"${market_cap / 1_000_000_000:.2f} Milyar"
    else:
        formatted_cap = f"${market_cap / 1_000_000_000_000:.2f} Trilyon"
    logger.info(f"Formatted market cap: {formatted_cap}")
    return formatted_cap

def get_crypto_price(url: str) -> Optional[str]:
    """Fetch cryptocurrency price or market cap from the given URL."""
    try:
        logger.info(f"Fetching data from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Data fetched successfully from {url}")
        return response.text.strip()
    except requests.RequestException as e:
        logger.error(f"Request to {url} failed: {e}")
        return None

def crypto_send() -> None:
    """Fetch cryptocurrency data, format it, and send an email with the information."""
    logger.start("Running crypto_send")
    cryptos: Dict[str, List[str]] = {
        "BTC": ["https://cryptoprices.cc/BTC/", "https://cryptoprices.cc/BTC/MCAP/"],
        "ETH": ["https://cryptoprices.cc/ETH/", "https://cryptoprices.cc/ETH/MCAP/"],
        "SOL": ["https://cryptoprices.cc/SOL/", "https://cryptoprices.cc/SOL/MCAP/"],
    }

    body = "🚀 Anlık Kripto Verileri 🚀\n"

    for crypto, urls in cryptos.items():
        logger.info(f"Processing data for {crypto}")
        try:
            price, market_cap = map(get_crypto_price, urls)
            if price and market_cap:
                formatted_price = format_price(float(price))
                formatted_market_cap = format_market_cap(float(market_cap))
                body += f"\n🌟 #{crypto} Fiyatı: ${formatted_price}\n"
                body += f"💰 #{crypto} Piyasa Değeri: {formatted_market_cap}\n"
                logger.info(f"Data for {crypto} added to email body.")
            else:
                logger.warning(f"Data for {crypto} is incomplete, skipping.")
        except Exception as e:
            logger.error(f"Failed to process data for {crypto}: {e}")
            continue

    # Generate Bitcoin graph
    image_stream = plot_bitcoin_graph()
    if image_stream:
        try:
            send_email("Anlık Kripto Verileri #crypto_send", body, image_stream)
            logger.ok("Email sent successfully with cryptocurrency data.")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    else:
        logger.error("Bitcoin graph generation failed, email not sent.")

if __name__ == "__main__":
    crypto_send()
