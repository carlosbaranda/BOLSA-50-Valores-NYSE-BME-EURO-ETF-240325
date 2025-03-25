
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bolsa Multimercado", layout="wide")
st.title("📊 Modelo Multimercado - Evolución desde 1 de enero")

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "WMT", "UNH", "IDR.MC"]

@st.cache_data(ttl=3600)
def obtener_datos(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="300d")
            info = stock.info

            if len(hist) >= 200:
                cierre_inicio_ano = hist[hist.index >= "2025-01-01"]["Close"]
                if len(cierre_inicio_ano) > 0:
                    cambio_ytd = (hist["Close"][-1] - cierre_inicio_ano[0]) / cierre_inicio_ano[0] * 100
                else:
                    cambio_ytd = 0
                data.append({
                    "Ticker": ticker,
                    "Nombre": info.get("shortName", ""),
                    "Último Precio": round(hist["Close"][-1], 2),
                    "Cambio Desde 1 Ene (%)": round(cambio_ytd, 2)
                })
        except:
            continue
    return pd.DataFrame(data)

df = obtener_datos(tickers)
st.dataframe(df, use_container_width=True)
