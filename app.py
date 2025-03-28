
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bolsa Multimercado", layout="wide")
st.title("📊 Modelo Multimercado - Bolsa")

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
                cierre_inicio_ano = hist[hist.index >= "2025-01-01"]["Close"]
                if len(cierre_inicio_ano) > 0:
                    cambio_ytd = (hist["Close"][-1] - cierre_inicio_ano[0]) / cierre_inicio_ano[0] * 100
                else:
                    cambio_ytd = 0
                vol_diario = hist["Volume"][-1]
                vol_media_50 = hist["Volume"].tail(50).mean()
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
                    "Cambio Desde 1 Ene (%)": round(cambio_ytd, 2),
                    "YTD (%)": round((hist["Close"][-1] - hist["Close"][-252]) / hist["Close"][-252] * 100, 2),
                    "YTD (%)": round(cambio_ytd, 2),
                    "Volumen Diario": int(vol_diario),
                    "Volumen Medio (50)": int(vol_media_50),
                    "Diferencia Volumen (%)": round(dif_vol, 2)
                })
        except:
            continue
    return pd.DataFrame(data)

df = obtener_datos(tickers)

# Añadir íconos visuales a los cambios
def extraer_num(valor):
    try:
        return float(str(valor).replace("📈", "").replace("📉", "").strip())
    except:
        return 0

for col in ["Cambio Día (%)", "Cambio Semana (%)", "Cambio Desde 1 Ene (%)", "YTD (%)"]:
    df[col] = [f"📈 {v}" if extraer_num(v) > 3 else f"📉 {v}" if extraer_num(v) < -3 else f"{v}" for v in df[col]]

df = df.sort_values("Cambio Día (%)", ascending=False)

# Filtros por mercado y sector
mercado_sel = st.selectbox("Selecciona un mercado:", ["Todos"] + sorted(df["Mercado"].dropna().unique()))
if mercado_sel != "Todos":
    df = df[df["Mercado"] == mercado_sel]

sector_sel = st.selectbox("Selecciona un sector:", ["Todos"] + sorted(df["Sector"].dropna().unique()))
if sector_sel != "Todos":
    df = df[df["Sector"] == sector_sel]

# Estilo condicional de la tabla
def resaltar(val):
    try:
        num = float(str(val).replace("📈", "").replace("📉", "").strip())
        if num > 3:
            return 'color: green; font-weight: bold'
        elif num < -3:
            return 'color: red; font-weight: bold'
    except:
        return ''
    return ''

st.dataframe(df.style.applymap(resaltar, subset=["Cambio Día (%)", "Cambio Semana (%)", "Cambio Desde 1 Ene (%)", "YTD (%)"]), use_container_width=True)

# --- Tabla resumen de ganadores y perdedores con filtro de mercado

st.subheader("📊 Resumen Top 25 por YTD%")

mercado_resumen = st.selectbox("Filtrar resumen por mercado:", ["Todos"] + sorted(df["Mercado"].dropna().unique()), key="filtro_resumen_mercado")
df_resumen = df.copy()
sector_resumen = st.selectbox("Filtrar resumen por sector:", ["Todos"] + sorted(df["Sector"].dropna().unique()), key="filtro_resumen_sector")
df_resumen["YTD_valor"] = df_resumen["YTD (%)"].apply(lambda x: float(str(x).replace("📈", "").replace("📉", "").strip()) if isinstance(x, str) else x)

if mercado_resumen != "Todos":
    df_resumen = df_resumen[df_resumen["Mercado"] == mercado_resumen]
if sector_resumen != "Todos":
    df_resumen = df_resumen[df_resumen["Sector"] == sector_resumen]
    df_resumen = df_resumen[df_resumen["Mercado"] == mercado_resumen]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟢 Top 25 Ganadores")
    st.dataframe(df_resumen.sort_values("YTD_valor", ascending=False).head(25)[["Ticker", "Nombre", "YTD (%)"]], use_container_width=True)

with col2:
    st.markdown("### 🔴 Top 25 Perdedores")
    st.dataframe(df_resumen.sort_values("YTD_valor", ascending=True).head(25)[["Ticker", "Nombre", "YTD (%)"]], use_container_width=True)


# Gráfico del valor con medias móviles
st.subheader("📈 Gráfico del valor seleccionado")
seleccion = st.selectbox("Selecciona un ticker:", df["Ticker"].unique())
if seleccion:
    hist = yf.Ticker(seleccion).history(period="1y")
    hist["Media 12"] = hist["Close"].rolling(12).mean()
    hist["Media 50"] = hist["Close"].rolling(50).mean()
    hist["Media 200"] = hist["Close"].rolling(200).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    hist["Close"].plot(ax=ax, label="Cierre", color="black")
    hist["Media 12"].plot(ax=ax, label="Media 12", color="orange")
    hist["Media 50"].plot(ax=ax, label="Media 50", color="blue")
    hist["Media 200"].plot(ax=ax, label="Media 200", color="green")
    ax.set_title(f"Precio y medias móviles: {seleccion}")
    ax.set_ylabel("Precio")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📈 Gráfico 2 años")
    hist2 = yf.Ticker(seleccion).history(period="2y")
    hist2["Media 12"] = hist2["Close"].rolling(12).mean()
    hist2["Media 50"] = hist2["Close"].rolling(50).mean()
    hist2["Media 200"] = hist2["Close"].rolling(200).mean()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    hist2["Close"].plot(ax=ax2, label="Cierre", color="black")
    hist2["Media 12"].plot(ax=ax2, label="Media 12", color="orange")
    hist2["Media 50"].plot(ax=ax2, label="Media 50", color="blue")
    hist2["Media 200"].plot(ax=ax2, label="Media 200", color="green")
    ax2.set_title(f"Precio y medias móviles 2 años: {seleccion}")
    ax2.set_ylabel("Precio")
    ax2.legend()
    st.pyplot(fig2)



