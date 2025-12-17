import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import datetime

st.set_page_config(
    page_title = "Argie Market live",
    layout = "wide",
    initial_sidebar_state="collapsed"
)

st.title("Argentinian Market Live")
st.markdown(f"*{datetime.datetime.now().strftime('%d/%m/%Y')} - Panel de Control Unificado*")
st.markdown("---")

#Carga de datos
@st.cache_data(ttl=60) # Actualiza cada 60 segs
def traer_dolares():
    url = "https://dolarapi.com/v1/dolares"
    try:
        res = requests.get(url).json()
        return res
    except:
        return []

@st.cache_data(ttl=300)
def traer_acciones(tickers):
    data = yf.download(tickers, period="1mo", interval="1d")['Close']
    return data

#dolares
st.subheader("Dolar Cotitation")
dolares = traer_dolares()
if dolares: 
    interesantes = ["Oficial", "Blue", "Mep", "Ccl", "Cripto"]
    cols = st.columns(len(interesantes))

    for i, tipo in enumerate(interesantes):
        dato = next((item for item in dolares if item["nombre"] == tipo), None)
        if dato:
            with cols[i]:
                st.container(border=True).metric(
                    label=dato["nombre"],
                    value=f"${dato['venta']}",
                    delta=f"C: ${dato['compra']}"
                )

else:
    st.warning("Waiting conection with DolarApi")

st.markdown("---")

#grid graficos
st.subheader("Leader Stocks (ADRs)")

acciones_principales = ["GGAL", "YPF", "BMA", "MELI", "PAM", "CEPU"]

df = traer_acciones(acciones_principales)

columnas_acciones = st.columns(3)

if not df.empty:
    for index, ticker in enumerate(acciones_principales):
        columnas_actual = columnas_acciones[index % 3]

        with columnas_actual:
            with st.container(border=True):
                # Calcular cambio porcentual
                precio_hoy = df[ticker].iloc[-1]
                precio_ayer = df[ticker].iloc[-2]
                variacion = ((precio_hoy - precio_ayer) / precio_ayer) * 100
                
                #Metricas
                st.metric(
                    label=f"{ticker} (USD)",
                    value=f"{precio_hoy:.2f}",
                    delta=f"{variacion:.2f}%"
                )
                
                #grafico
                st.area_chart(df[ticker], height=100, color="#29b5e8")


# Footer limpio
st.markdown("---")
st.caption("Dashboard desarrollado con Python & Streamlit.")
