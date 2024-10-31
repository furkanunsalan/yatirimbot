"""
This module provides functions for fetching and sharing current price and change of BIST30 stocks picked randomly.

It uses the yfinance library to fetch market data and a custom email utility to send the information.
"""

import random
import yfinance as yf
from src.email_utils import send_email
from src.lib.constants import bist30_stocks
from src.lib.utils import get_stock_emoji_and_text
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)
#test?

def get_stock_change(stock):
    """
    Calculate the current change of a BIST30 stock.

    Returns price, change of the chosen stock in order.
    """
    logger.info(f"Fetching stock change for: {stock}")
    try:
        hisse = yf.Ticker(stock)
        hisse_current = hisse.info.get("currentPrice", "0")
        hisse_prev = hisse.info.get("previousClose", "0")
        
        if hisse_prev == 0:
            logger.warning(f"Previous close price for {stock} is zero, cannot calculate change.")
            return hisse_current, 0.0
        
        hisse_current_change = ((hisse_current - hisse_prev) / hisse_prev) * 100
        hisse_current_change = round(hisse_current_change, 2)
        
        logger.info(f"Current price: {hisse_current}, Change: {hisse_current_change}% for {stock}")
        return hisse_current, hisse_current_change
    except Exception as e:
        logger.error(f"Error fetching stock data for {stock}: {e}")
        return None, None

def bist30_change():
    """Calculate and print the current change and current price of BIST30 stock today."""
    logger.start("Running bist30_change")
    chosen_stock = random.choice(bist30_stocks)
    stock_code = chosen_stock + ".IS"
    logger.info(f"Chosen stock: {chosen_stock} ({stock_code})")
    
    price, change = get_stock_change(stock_code)
    
    if price is None or change is None:
        logger.error("Failed to retrieve stock change data.")
        return
    
    emo, text = get_stock_emoji_and_text(change)
    subject = "send_bist30_stock #bist30_change"
    body = f"""🔴 #{chosen_stock} bugün %{change} {text}

{emo} Anlık Fiyatı: {price}

#yatırım #borsa #hisse #ekonomi #bist #bist100 #türkiye #faiz #enflasyon #endeks #finans #para #şirket
    """
    
    logger.info("Email body prepared for sending.")
    
    # print(body)
    send_email(subject, body)
    
    logger.ok("bist30_change worked successfully.")

if __name__ == "__main__":
    bist30_change()
