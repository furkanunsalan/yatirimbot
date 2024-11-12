"""
Module for fetching currency data and sending email reports.
"""
import logging
from io import BytesIO
import yfinance as yf
from matplotlib import pyplot as plt
from src.email_utils import send_email

# Set up logging configuration
logger = logging.getLogger(__name__)

def get_currency_data(currency_pair: str) -> yf.Ticker.history:
    """
    Fetch the last 3 months of historical data for a given currency pair.

    Args:
        currency_pair (str): The currency pair to fetch data for (e.g., "USDTRY=X").

    Returns:
        yf.Ticker.history: Historical data for the currency pair.
    """
    try:
        logger.info(f"Fetching data for {currency_pair}.")
        data = yf.Ticker(currency_pair).history(period="3mo")
        if data.empty:
            logger.warning(f"No data returned for currency pair {currency_pair}.")
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {currency_pair}: {e}")
        return None

def plot_currency_data(currency_data: yf.Ticker.history, currency_pair: str) -> BytesIO:
    """
    Create a plot of the currency data.

    Args:
        currency_data (yf.Ticker.history): Historical data for the currency pair.
        currency_pair (str): The currency pair being plotted.

    Returns:
        BytesIO: The image buffer containing the plot.
    """
    try:
        logger.info(f"Creating plot for {currency_pair}.")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(currency_data["Close"], label=f"{currency_pair} Son Fiyat")
        ax.set_title(f"{currency_pair} - Son 3 Ay")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("Değer")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        
        image_buffer = BytesIO()
        fig.savefig(image_buffer, format="png")
        plt.close(fig)
        image_buffer.seek(0)
        
        logger.info(f"Plot for {currency_pair} created successfully.")
        return image_buffer
    except Exception as e:
        logger.error(f"Error creating plot for {currency_pair}: {e}")
        return None

def currency_send():
    """Fetch currency data, create plots, and send an email report."""
    logger.start("Running exchange_rates")
    try:
        currencies = ["USDTRY=X", "EURTRY=X", "GBPTRY=X"]
        email_body = "🌍 Döviz Kurları 🌍\n\n"
        image_buffer = None

        for currency in currencies:
            data = get_currency_data(currency)
            if data is None or data.empty:
                logger.warning(f"Skipping {currency} due to missing data.")
                continue
            
            last_price = data["Close"].iloc[-1]
            change = (data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0] * 100
            currency_label = currency.replace("=X", "")
            
            # Generate and save plot for the first currency
            if currency == "USDTRY=X":
                image_buffer = plot_currency_data(data, currency_label)
                if image_buffer is None:
                    logger.error("Failed to generate image for email; proceeding without an image.")
            
            email_body += f"{currency_label}:\nSon Fiyat: {last_price:.2f}\nDeğişim: {change:.2f}%\n\n"

        # Send the email with or without an image attachment
        send_email("Güncel Döviz Kurları #currency_send", email_body, image_buffer)
        logger.ok("Currency report email sent successfully.")
    except Exception as e:
        logger.error(f"Error in currency_send: {e}")

if __name__ == "__main__":
    currency_send()
