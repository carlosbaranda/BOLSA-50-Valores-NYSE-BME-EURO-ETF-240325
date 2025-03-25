
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Modelo Bolsa - Multimercado", layout="wide")
st.title("📊 Valores de NYSE, IBEX 35 (incluye INDRA), EuroStoxx y ETFs")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'WMT', 'UNH', 'KO', 'PEP', 'V', 'BAC', 'HD', 'DIS', 'MA', 'PYPL', 'INTC', 'IBM', 'CSCO', 'ORCL', 'NFLX', 'T', 'CVX', 'PFE', 'XOM', 'C', 'MCD', 'BA', 'ABT', 'CRM', 'MRK', 'QCOM', 'NKE', 'LOW', 'GE', 'TMO', 'AXP', 'COST', 'TXN', 'NEE', 'UPS', 'LIN', 'MDT', 'AMGN', 'GILD', 'SBUX', 'MO', 'DUK', 'ACS.MC', 'AENA.MC', 'AMS.MC', 'ANA.MC', 'BBVA.MC', 'CABK.MC', 'CLNX.MC', 'COL.MC', 'ENG.MC', 'FER.MC', 'GRF.MC', 'IBE.MC', 'IAG.MC', 'ITX.MC', 'LOG.MC', 'MAP.MC', 'MEL.MC', 'MRL.MC', 'MTB.MC', 'NHH.MC', 'NTGY.MC', 'PHM.MC', 'RED.MC', 'REP.MC', 'ROVI.MC', 'SAB.MC', 'SAN.MC', 'SGRE.MC', 'SLR.MC', 'SNT.MC', 'TEF.MC', 'TRE.MC', 'UNI.MC', 'VIS.MC', 'XME.MC', 'ZEL.MC', 'IDR.MC', 'AIR.PA', 'ADS.DE', 'ALV.DE', 'BN.PA', 'ENEL.MI', 'ENGI.PA', 'OR.PA', 'SAP.DE', 'SIE.DE', 'SU.PA', 'TTE.PA', 'VOW3.DE', 'DTE.DE', 'DPW.DE', 'BAS.DE', 'BAYN.DE', 'BMW.DE', 'CRH.L', 'DAI.DE', 'KER.PA', 'LVMH.PA', 'MC.PA', 'MT.AS', 'PHIA.AS', 'RWE.DE', 'SGO.PA', 'URW.AS', 'ZAL.DE', 'ATCO-A.ST', 'HEIA.AS', 'IFX.DE', 'LIN.DE', 'UCG.MI', 'STLA.MI', 'ENI.MI', 'ISP.MI', 'BNP.PA', 'ALFA.ST', 'FRE.DE', 'ABN.AS', 'FER.MC', 'AMS.MC', 'SDF.DE', 'MUV2.DE', 'ACA.PA', 'MBG.DE', 'MTX.DE', 'SKA-B.ST', 'VWS.CO', 'SGSN.SW', 'SPY', 'QQQ', 'DIA', 'VTI', 'IWM', 'EFA', 'EEM', 'VNQ', 'LQD', 'HYG', 'XLF', 'XLK', 'XLE', 'XLY', 'XLV', 'XLI', 'XLB', 'XLC', 'XLRE', 'ARKK', 'ARKW', 'ARKF', 'ARKG', 'ARKQ', 'ARKX', 'SOXX', 'SMH', 'IBB', 'VHT', 'IYZ', 'XRT', 'XHB', 'XME', 'ITA', 'IYT', 'MTUM', 'USMV', 'XOP', 'XBI', 'XTL', 'RWR', 'PSJ', 'KRE', 'FDN', 'VOO', 'SCHD', 'BND', 'TLT', 'TIP', 'SHY']

@st.cache_data(ttl=3600)
def obtener_datos(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="300d")
            info = stock.info

            if ".MC" in ticker:
                mercado = "España"
            elif ticker in ['SPY', 'QQQ', 'DIA', 'VTI', 'IWM', 'EFA', 'EEM', 'VNQ', 'LQD', 'HYG', 'XLF', 'XLK', 'XLE', 'XLY', 'XLV', 'XLI', 'XLB', 'XLC', 'XLRE', 'ARKK', 'ARKW', 'ARKF', 'ARKG', 'ARKQ', 'ARKX', 'SOXX', 'SMH', 'IBB', 'VHT', 'IYZ', 'XRT', 'XHB', 'XME', 'ITA', 'IYT', 'MTUM', 'USMV', 'XOP', 'XBI', 'XTL', 'RWR', 'PSJ', 'KRE', 'FDN', 'VOO', 'SCHD', 'BND', 'TLT', 'TIP', 'SHY']:
                mercado = "ETF"
            elif ticker.endswith((".PA", ".DE", ".MI", ".AS", ".ST", ".L", ".SW")):
                mercado = "EuroStoxx"
            else:
                mercado = "NYSE"

            if len(hist) >= 200:
                cambio_dia = (hist["Close"][-1] - hist["Open"][-1]) / hist["Open"][-1] * 100
                cambio_semana = (hist["Close"][-1] - hist["Close"][-6]) / hist["Close"][-6] * 100
                cambio_ytd = (hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0] * 100
                vol_diario = hist["Volume"][-1]
                vol_media_50 = hist["Volume"].tail(50).mean()
                vol_media_12 = hist["Volume"].tail(12).mean()
                dif_vol = ((vol_diario - vol_media_50) / vol_media_50) * 100
                data.append({
                    "Ticker": ticker,
                    "Nombre": info.get("shortName", ""),
                    "Sector": info.get("sector", ""),
                    "Mercado": mercado,
                    "PER": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else None,
                    "Último Precio": round(hist["Close"][-1], 2),
                    "Cambio Día (%)": round(cambio_dia, 2),
                    "Cambio Semana (%)": round(cambio_semana, 2),
                    "Cambio YTD (%)": round(cambio_ytd, 2),
                    "Volumen Diario": int(vol_diario),
                    "Volumen Medio (50)": int(vol_media_50),
                    "Volumen Medio (12)": int(vol_media_12),
                    "Diferencia Volumen (%)": round(dif_vol, 2)
                })
        except:
            continue
    return pd.DataFrame(data)

df = obtener_datos(tickers)

st.dataframe(df, use_container_width=True)
