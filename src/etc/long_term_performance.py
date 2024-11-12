"""
This module performs a long-term analysis of a randomly selected stock.

It fetches stock data, creates a chart, and sends an email report.
"""
import logging
from datetime import datetime, timedelta
from io import BytesIO
from secrets import randbelow

import matplotlib.pyplot as plt
import yfinance as yf

from src.email_utils import send_email
from src.lib.constants import us_stock_list

# Set up logging configuration
logger = logging.getLogger(__name__)

def format_value(value, currency):
    """Format numerical values with currency."""
    if value and isinstance(value, (int, float)):
        return f"{value:,.2f} {currency}".replace(",", ".")
    return ""

def analyze_long_term_stock():
    """Analyze a randomly selected stock and send a report via email."""
    logger.start("Running analyze_long_term_stock")
    try:
        selected_stock = us_stock_list[randbelow(len(us_stock_list))]
        logger.info(f"Selected stock for analysis: {selected_stock}")
        
        stock = yf.Ticker(selected_stock)
        stock_info = stock.info
        currency = stock_info.get("financialCurrency", "USD")

        # Compose the email body with stock information
        email_body = f"📈#{selected_stock} {stock_info.get('shortName', 'Stock')} hisse senedinin güncel ve uzun dönemli performansı 👇\n\n"
        current_price = stock_info.get("regularMarketPrice") or (stock_info.get("open", 0) + stock_info.get("dayHigh", 0)) / 2
        email_body += f"▪️ Anlık Fiyat: {format_value(current_price, currency)}\n"
        email_body += f"▪️ 52 Haftalık En Yüksek Değer: {format_value(stock_info.get('fiftyTwoWeekHigh'), currency)}\n"
        email_body += f"▪️ Ortalama Günlük İşlem Hacmi (Son 10 Gün): {format_value(stock_info.get('averageDailyVolume10Day'), 'hisse')}\n"
        email_body += f"▪️ Piyasa Değeri: {format_value(stock_info.get('marketCap'), currency)}\n"

        # Fetch stock historical data for the last year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        try:
            stock_data = yf.download(selected_stock, start=start_date, end=end_date)
            if stock_data.empty:
                logger.warning(f"No historical data found for {selected_stock}")
                return  # Exit if no data is available
        except Exception as e:
            logger.error(f"Failed to fetch historical data for {selected_stock}: {e}")
            return

        # Plotting the stock price history
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(stock_data["Close"], label="Son Fiyat")
            y_min, y_max = stock_data["Close"].min(), stock_data["Close"].max()
            y_ticks = range(int(y_min), int(y_max) + 1, max(1, int((y_max - y_min) / 10)))
            plt.yticks(y_ticks)
            plt.title(f'{stock_info.get("shortName", selected_stock)} Değişim Grafiği')
            plt.ylabel("Fiyat")
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.legend()

            image_stream = BytesIO()
            plt.savefig(image_stream, format="png")
            plt.close()
            image_stream.seek(0)
            logger.info(f"Plot created for {selected_stock}")
        except Exception as e:
            logger.error(f"Failed to create plot for {selected_stock}: {e}")
            return

        # Send the email with the generated plot
        subject = f"{stock_info.get('shortName', selected_stock)} Hissesi Performans Raporu #L_term_stock"
        try:
            send_email(subject, email_body, image_stream)
            logger.ok(f"Email sent successfully for {selected_stock}")
        except Exception as e:
            logger.error(f"Failed to send email for {selected_stock}: {e}")

    except Exception as e:
        logger.error(f"Error in analyze_long_term_stock: {e}")

if __name__ == "__main__":
    analyze_long_term_stock()
