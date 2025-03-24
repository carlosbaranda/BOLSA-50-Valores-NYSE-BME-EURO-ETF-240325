
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Modelo Bolsa - 200 Valores", layout="wide")
st.title("📊 Modelo de Bolsa - 50 valores por mercado")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'WMT', 'UNH', 'KO', 'PEP', 'V', 'BAC', 'HD', 'DIS', 'MA', 'PYPL', 'INTC', 'IBM', 'CSCO', 'ORCL', 'NFLX', 'T', 'CVX', 'PFE', 'XOM', 'C', 'MCD', 'BA', 'ABT', 'CRM', 'MRK', 'QCOM', 'NKE', 'LOW', 'GE', 'TMO', 'AXP', 'COST', 'TXN', 'NEE', 'UPS', 'LIN', 'MDT', 'AMGN', 'GILD', 'SBUX', 'MO', 'DUK', 'SAN.MC', 'BBVA.MC', 'ITX.MC', 'IBE.MC', 'REP.MC', 'CABK.MC', 'CLNX.MC', 'ENG.MC', 'FER.MC', 'GRF.MC', 'IAG.MC', 'MAP.MC', 'TEF.MC', 'ACX.MC', 'AENA.MC', 'ALM.MC', 'BKT.MC', 'COL.MC', 'ELE.MC', 'ENC.MC', 'EQT.MC', 'FCC.MC', 'LOG.MC', 'MEL.MC', 'NTGY.MC', 'PHM.MC', 'RED.MC', 'R4.MC', 'SAB.MC', 'SGRE.MC', 'SPS.MC', 'VIS.MC', 'ZOT.MC', 'DIA.MC', 'OHL.MC', 'REE.MC', 'ENAG.MC', 'ACS.MC', 'BME.MC', 'EDR.MC', 'NHH.MC', 'VID.MC', 'BVA.MC', 'TYT.MC', 'NAT.MC', 'QRT.MC', 'RMS.MC', 'SIX.MC', 'BIO.MC', 'ECO.MC', 'AIR.PA', 'ADS.DE', 'ALV.DE', 'BN.PA', 'ENEL.MI', 'ENGI.PA', 'OR.PA', 'SAP.DE', 'SIE.DE', 'SU.PA', 'TTE.PA', 'VOW3.DE', 'DTE.DE', 'DPW.DE', 'BAS.DE', 'BAYN.DE', 'BMW.DE', 'CRH.L', 'DAI.DE', 'KER.PA', 'LVMH.PA', 'MC.PA', 'MT.AS', 'PHIA.AS', 'RWE.DE', 'SGO.PA', 'URW.AS', 'ZAL.DE', 'ATCO-A.ST', 'HEIA.AS', 'IFX.DE', 'LIN.DE', 'UCG.MI', 'STLA.MI', 'ENI.MI', 'ISP.MI', 'BNP.PA', 'ALFA.ST', 'FRE.DE', 'ABN.AS', 'FER.MC', 'AMS.MC', 'SDF.DE', 'MUV2.DE', 'ACA.PA', 'MBG.DE', 'MTX.DE', 'SKA-B.ST', 'VWS.CO', 'SGSN.SW', 'SPY', 'QQQ', 'DIA', 'VTI', 'IWM', 'EFA', 'EEM', 'VNQ', 'LQD', 'HYG', 'XLF', 'XLK', 'XLE', 'XLY', 'XLV', 'XLI', 'XLB', 'XLC', 'XLRE', 'ARKK', 'ARKW', 'ARKF', 'ARKG', 'ARKQ', 'ARKX', 'SOXX', 'SMH', 'IBB', 'VHT', 'IYZ', 'XRT', 'XHB', 'XME', 'ITA', 'IYT', 'MTUM', 'USMV', 'XOP', 'XBI', 'XTL', 'RWR', 'PSJ', 'KRE', 'FDN', 'VOO', 'SCHD', 'BND', 'TLT', 'TIP', 'SHY']

@st.cache_data(ttl=3600)
def obtener_datos(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="300d")
            info = stock.info
            if len(hist) >= 200:
                cambio_dia = (hist["Close"][-1] - hist["Open"][-1]) / hist["Open"][-1] * 100
                cambio_semana = (hist["Close"][-1] - hist["Close"][-6]) / hist["Close"][-6] * 100
                cambio_ytd = (hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0] * 100
                vol_diario = hist["Volume"][-1]
                vol_media_70 = hist["Volume"].tail(70).mean()
                dif_vol = ((vol_diario - vol_media_70) / vol_media_70) * 100
                
    sector = info.get("sector", "")
    if ".MC" in ticker:
        mercado = "España"
    elif ticker.endswith((".PA", ".DE", ".MI", ".AS", ".ST", ".L", ".SW")):
        mercado = "EuroStoxx"
    elif ticker in {tickers_etf}:
        mercado = "ETF"
    else:
        mercado = "NYSE"

                data.append({
                    "Ticker": ticker,
                    "Nombre": info.get("shortName", ""),
                    "Sector": sector,
                    "Mercado": mercado,
                    "Cambio Día (%)": round(cambio_dia, 2),
                    "Cambio Semana (%)": round(cambio_semana, 2),
                    "Cambio YTD (%)": round(cambio_ytd, 2),
                    "Volumen Diario": int(vol_diario),
                    "Volumen Medio (70)": int(vol_media_70),
                    "Diferencia Volumen (%)": round(dif_vol, 2)
                })
        except:
            continue
    return pd.DataFrame(data)

df = obtener_datos(tickers)


# Filtro por mercado
mercado_sel = st.selectbox("Filtrar por mercado", ["Todos"] + sorted(df["Mercado"].unique()))
if mercado_sel != "Todos":
    df = df[df["Mercado"] == mercado_sel]


st.dataframe(df, use_container_width=True)

# Gráfico por ticker
st.subheader("📈 Gráfico del valor con medias móviles")
seleccion = st.selectbox("Selecciona un ticker:", df["Ticker"])
if seleccion:
    hist = yf.Ticker(seleccion).history(period="1y")
    hist["Media 60"] = hist["Close"].rolling(60).mean()
    hist["Media 200"] = hist["Close"].rolling(200).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    hist["Close"].plot(ax=ax, label="Cierre")
    hist["Media 60"].plot(ax=ax, label="Media 60")
    hist["Media 200"].plot(ax=ax, label="Media 200")
    ax.set_title(f"Precio y medias móviles: {seleccion}")
    ax.set_ylabel("Precio")
    ax.legend()
    st.pyplot(fig)
