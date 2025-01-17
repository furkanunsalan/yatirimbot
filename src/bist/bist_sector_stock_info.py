"""
This module provides functionality to fetch and send performance data for stocks within specific sectors of Borsa İstanbul (BIST).

It utilizes the yfinance library to retrieve stock performance information and generates a formatted email report.
"""

import random
import yfinance as yf
from src.email_utils import send_email
from src.lib.utils import get_stock_emoji_and_text
from src.lib.constants import stocks_by_sector
import logging

logger = logging.getLogger(__name__)

def fetch_stock_performance(stock_code):
    """
    Fetch the stock performance data for a given stock code.

    Args:
        stock_code (str): The stock code in the format 'SYMBOL.IS'.

    Returns:
        dict: A dictionary containing the current price,
               day 5 close price, and any error messages if applicable.
    """
    stock_info = yf.Ticker(stock_code)

    try:
        logger.info(f"Fetching performance data for stock: {stock_code}")
        stock_data = stock_info.history(period="max")

        current_price = float(stock_info.info.get("currentPrice", "0"))
        if len(stock_data) >= 6:
            day_5_close = stock_data["Close"].iloc[-6]
            logger.info(f"Successfully fetched performance data for stock: {stock_code}")
            return {
                "current_price": current_price,
                "day_5_close": day_5_close,
                "error": None,
            }
        else:
            logger.warning(f"Insufficient data for stock: {stock_code}")
            return {
                "current_price": None,
                "day_5_close": None,
                "error": "Yeterli veri yok",
            }

    except (ValueError, KeyError, IndexError) as error:
        logger.error(f"Data retrieval error for {stock_code}: {error}")
        return {
            "current_price": None,
            "day_5_close": None,
            "error": f"Veri alınırken hata: {str(error)}",
        }
    except Exception as error:
        logger.error(f"Unexpected error for {stock_code}: {error}")
        return {
            "current_price": None,
            "day_5_close": None,
            "error": f"Beklenmeyen hata: {str(error)}",
        }


def bist_sector_stock_info(day):
    """
    Generate and send an email report on the performance of stocks in a specific sector of Borsa İstanbul based on the given day index.

    Args:
        day (int): Index corresponding to the desired sector in the predefined sectors list.
    """
    try:
        sectors = [
            "Banka",
            "Aracı Kurum",
            "Perakende Ticaret",
            "Bilişim",
            "Gayrimenkul Yatırım Ortaklığı",
        ]

        sector = sectors[day]
        logger.start(f"Running bist_sector_stock_info for sector: {sector}")

        subject = "sektor_hisse_bilgi #crypto ##crypto"
        body = f"🔴 {sector} Hisselerinin 5 Günlük Performansları 👇 \n\n"
        random_stocks = random.sample(stocks_by_sector[sector], 8)

        for stock in random_stocks:
            stock_code = f"{stock}.IS"
            performance = fetch_stock_performance(stock_code)

            current_price = performance["current_price"]
            day_5_close = performance["day_5_close"]
            error = performance["error"]

            if error:
                body += f"⚠️ #{stock} {error}\n"
            else:
                day_5_change_percent = ((current_price - day_5_close) / day_5_close) * 100
                day_5_change_percent = round(day_5_change_percent, 1)
                emo, text = get_stock_emoji_and_text(day_5_change_percent)
                body += f"{emo} #{stock} {yf.Ticker(stock_code).info.get('longName', '')} %{day_5_change_percent} {text}\n"

        body += "\n#yatırım #borsa #hisse #ekonomi #bist #bist100 #türkiye #faiz #enflasyon #endeks #finans #para #şirket"

        send_email(subject, body)
        # print(body)
        logger.ok(f"bist_sector_stock_info worked successfully")

    except Exception as e:
        logger.error(f"Failed to generate or send sector stock report for {sector}: {e}")
        raise


if __name__ == "__main__":
    # Example: Use index 4 for "Gayrimenkul Yatırım Ortaklığı"
    bist_sector_stock_info(4)
