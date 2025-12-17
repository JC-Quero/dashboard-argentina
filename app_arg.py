import streamlit as st
import pandas as pd
import requests
import yfinance as yf

st.set_page_config(page_title="Argie Dashboard 🇦🇷", layout="wide")
st.title("🧉 Monitor Financiero Argentino")

# --- FUNCIÓN 1: TRAER DÓLARES (API ARGENTINA) ---
@st.cache_data(ttl=60) # Actualiza cada 60 segs
def traer_dolares():
    url = "https://dolarapi.com/v1/dolares"
    try:
        res = requests.get(url).json()
        return res
    except:
        return []

# --- FUNCIÓN 2: TRAER ACCIONES (ADRs en Wall Street) ---
def traer_acciones(tickers):
    data = yf.download(tickers, period="1mo", interval="1d")['Close']
    return data

# --- UI: PESTAÑAS ---
tab1, tab2 = st.tabs(["💵 Dólar & Tipos de Cambio", "📈 Acciones (ADRs)"])

# --- PESTAÑA 1: DÓLARES ---
with tab1:
    st.header("Cotizaciones del Dólar")
    data_dolar = traer_dolares()
    
    if data_dolar:
        # Organizar en filas de 3 columnas
        cols = st.columns(3)
        for i, moneda in enumerate(data_dolar):
            nombre = moneda['nombre']
            compra = moneda['compra']
            venta = moneda['venta']
            fecha = moneda['fechaActualizacion']
            
            # Usamos el índice i % 3 para ir llenando las columnas
            with cols[i % 3]:
                st.container(border=True)
                st.metric(label=nombre, value=f"${venta}", delta=f"Compra: ${compra}")
                st.caption(f"Actualizado: {fecha}")
    else:
        st.error("No se pudo conectar con DolarApi.com")

# --- PESTAÑA 2: ACCIONES ARGENTINAS ---
with tab2:
    st.header("ADRs Argentinos en Wall Street (USD)")
    
    # Lista de empresas argentinas famosas
    tickers = ["GGAL", "YPF", "BMA", "PAM", "CRESY", "MELI"]
    opciones = st.multiselect("Elige empresas:", tickers, default=["GGAL", "YPF"])
    
    if opciones:
        with st.spinner('Bajando datos de Yahoo Finance...'):
            df_stocks = traer_acciones(opciones)
            
            # Mostrar gráfico lineal
            st.line_chart(df_stocks)
            
            # Mostrar último precio y cambio
            st.subheader("Último Cierre")
            ultimos_precios = df_stocks.iloc[-1]
            cols_stock = st.columns(len(opciones))
            
            for i, ticker in enumerate(opciones):
                precio = ultimos_precios[ticker]
                anterior = df_stocks.iloc[-2][ticker]
                variacion = ((precio - anterior) / anterior) * 100
                
                cols_stock[i].metric(
                    label=ticker, 
                    value=f"USD {precio:.2f}", 
                    delta=f"{variacion:.2f}%"
                )

# Footer
st.markdown("---")
st.caption("Datos cortesía de DolarApi.com y Yahoo Finance. Hecho con Python 🐍")