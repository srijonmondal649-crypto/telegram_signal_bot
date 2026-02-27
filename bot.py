import asyncio
import yfinance as yf
import pandas as pd
import ta
from telegram import Bot
from datetime import datetime
import os

TOKEN = os.getenv("8648454107:AAGhrPIzMSDOoGX5FxknWCd8smdkHI9P7qk")
CHAT_ID = os.getenv("7703438092")

                    
                    
                    
                  
bot = Bot(token=TOKEN)

markets = ["EURUSD=X"]
timeframes = ["5m"]

async def send_signal():
    while True:
        try:
            for symbol in markets:
                for interval in timeframes:
                    data = yf.download(symbol, interval=interval, period="5d")
                    data["rsi"] = ta.momentum.RSIIndicator(data["Close"]).rsi()
                    data["ema20"] = ta.trend.EMAIndicator(data["Close"], 20).ema_indicator()
                    data["ema50"] = ta.trend.EMAIndicator(data["Close"], 50).ema_indicator()
                    data["macd"] = ta.trend.MACD(data["Close"]).macd()

                    latest = data.iloc[-1]
                    confidence = 0
                    signal = "NO TRADE"

                    if latest["ema20"] > latest["ema50"] and latest["rsi"] < 35 and latest["macd"] > 0:
                        signal = "BUY"
                        confidence = 60
                    elif latest["ema20"] < latest["ema50"] and latest["rsi"] > 65 and latest["macd"] < 0:
                        signal = "SELL"
                        confidence = 60

                    message = f"{datetime.now()} | {symbol}\nSignal: {signal}\nConfidence: {confidence}%\nTimeframe: {interval}"
                    await bot.send_message(chat_id=CHAT_ID, text=message)

        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(300)

asyncio.run(send_signal())
