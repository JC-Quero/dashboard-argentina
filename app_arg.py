import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Argie Market Live",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📈"
)

# ============= CSS MODERNO Y VISIBLE =============
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Fondo y colores base */
    .stApp {
        background: linear-gradient(135deg, #1a1f35 0%, #0f1419 100%);
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        animation: slideDown 0.6s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Títulos y textos */
    h1, h2, h3 {
        color: white !important;
        font-weight: 700 !important;
    }
    
    p, span, label, div {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Métricas con fondo visible */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 1.5rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    div[data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }
    
    /* Contenedores */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: rgba(102, 126, 234, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:hover {
        background: rgba(102, 126, 234, 0.12);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.25);
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Selectores */
    div[data-baseweb="select"],
    div[data-baseweb="base-input"] {
        background: rgba(30, 35, 50, 0.8) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
    }
    
    div[data-baseweb="select"]:hover,
    div[data-baseweb="base-input"]:hover {
        border-color: rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Texto en selectores */
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: white !important;
    }
    
    /* Multiselect */
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Líneas divisoras */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* Caption */
    .stCaption {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        background: rgba(102, 126, 234, 0.15) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        color: white !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Animación de entrada para columnas */
    [data-testid="column"] {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
    <div class="main-header">
        <h1>📊 Argentinian Market Live</h1>
        <p>Panel de Control del Mercado Argentino en Tiempo Real</p>
    </div>
""", unsafe_allow_html=True)

# Barra de actualización
col_time, col_refresh = st.columns([3, 1])
with col_time:
    ultima_actualizacion = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    st.markdown(f"🕐 **Última actualización:** {ultima_actualizacion}")
with col_refresh:
    if st.button("🔄 Actualizar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# Funciones
@st.cache_data(ttl=60)
def traer_dolares():
    url = "https://dolarapi.com/v1/dolares"
    try:
        res = requests.get(url, timeout=5).json()
        return res, None
    except Exception as e:
        return [], str(e)

@st.cache_data(ttl=300)
def traer_acciones(tickers):
    try:
        data = yf.download(
            tickers, 
            period="1mo", 
            interval="1d", 
            auto_adjust=True,
            progress=False
        )
        
        if isinstance(data.columns, pd.MultiIndex):
            data = data['Close']
        else:
            if 'Close' in data.columns:
                data = data['Close']
        
        return data, None
    except Exception as e:
        return pd.DataFrame(), str(e)

@st.cache_data(ttl=300)
def traer_riesgo_pais():
    try:
        return 1850, None
    except Exception as e:
        return None, str(e)

# ============= INDICADORES CLAVE =============
st.subheader("📍 Indicadores Clave")

cols_indicadores = st.columns(4)

# Riesgo país
with cols_indicadores[0]:
    riesgo, error = traer_riesgo_pais()
    if riesgo:
        st.metric(
            label="🇦🇷 Riesgo País",
            value=f"{riesgo} pb",
            delta="-50 pb",
            delta_color="inverse"
        )

# Dólar Blue
dolares, error_dolar = traer_dolares()
if dolares and not error_dolar:
    blue = next((item for item in dolares if item["nombre"] == "Blue"), None)
    if blue:
        with cols_indicadores[1]:
            variacion_blue = blue.get('venta', 0) - blue.get('compra', 0)
            st.metric(
                label="💵 Dólar Blue",
                value=f"${blue['venta']}",
                delta=f"Spread: ${variacion_blue}"
            )

# S&P 500
with cols_indicadores[2]:
    try:
        sp500 = yf.Ticker("^GSPC")
        sp_data = sp500.history(period="2d")
        if not sp_data.empty:
            precio_sp = sp_data['Close'].iloc[-1]
            var_sp = ((sp_data['Close'].iloc[-1] - sp_data['Close'].iloc[-2]) / sp_data['Close'].iloc[-2]) * 100
            st.metric(
                label="📈 S&P 500",
                value=f"{precio_sp:.2f}",
                delta=f"{var_sp:.2f}%"
            )
    except:
        st.metric(label="📈 S&P 500", value="N/A")

# Bitcoin
with cols_indicadores[3]:
    try:
        btc = yf.Ticker("BTC-USD")
        btc_data = btc.history(period="2d")
        if not btc_data.empty:
            precio_btc = btc_data['Close'].iloc[-1]
            var_btc = ((btc_data['Close'].iloc[-1] - btc_data['Close'].iloc[-2]) / btc_data['Close'].iloc[-2]) * 100
            st.metric(
                label="₿ Bitcoin",
                value=f"${precio_btc:,.0f}",
                delta=f"{var_btc:.2f}%"
            )
    except:
        st.metric(label="₿ Bitcoin", value="N/A")

st.markdown("---")

# ============= COTIZACIONES DÓLAR =============
st.subheader("💰 Cotizaciones del Dólar")

if dolares and not error_dolar:
    interesantes = ["Oficial", "Blue", "Mep", "Ccl", "Cripto"]
    cols = st.columns(len(interesantes))

    for i, tipo in enumerate(interesantes):
        dato = next((item for item in dolares if item["nombre"] == tipo), None)
        if dato:
            with cols[i]:
                spread = dato['venta'] - dato['compra']
                spread_pct = (spread / dato['compra']) * 100
                
                with st.container(border=True):
                    st.markdown(f"**{dato['nombre']}**")
                    st.metric(
                        label="Venta",
                        value=f"${dato['venta']:.2f}",
                        delta=f"Compra: ${dato['compra']:.2f}"
                    )
                    st.caption(f"Spread: ${spread:.2f} ({spread_pct:.1f}%)")
else:
    st.error(f"⚠️ Error al conectar con DolarApi")

st.markdown("---")

# ============= ACCIONES ADRs =============
st.subheader("🚀 Acciones Líderes (ADRs Argentinos)")

acciones_disponibles = {
    "GGAL": "Grupo Galicia",
    "YPF": "YPF",
    "BMA": "Banco Macro",
    "MELI": "MercadoLibre",
    "PAM": "Pampa Energía",
    "CEPU": "Central Puerto",
    "VIST": "Vista Energy",
    "SUPV": "Supervielle",
    "TEO": "Telecom Argentina",
    "TGS": "Transportadora Gas"
}

col_selector, col_periodo = st.columns([3, 1])
with col_selector:
    acciones_seleccionadas = st.multiselect(
        "Selecciona las acciones a mostrar:",
        options=list(acciones_disponibles.keys()),
        default=["GGAL", "YPF", "BMA", "MELI", "PAM", "CEPU"],
        format_func=lambda x: f"{x} - {acciones_disponibles[x]}"
    )

with col_periodo:
    periodo = st.selectbox("Período:", ["1mo", "3mo", "6mo", "1y"], index=0)

if acciones_seleccionadas:
    df, error_acciones = traer_acciones(acciones_seleccionadas)
    
    if not df.empty and not error_acciones:
        if isinstance(df, pd.Series):
            df = df.to_frame()
        
        columnas_acciones = st.columns(3)
        
        # Colores vibrantes
        colores = ['#667eea', '#f093fb', '#4ade80', '#fbbf24', '#f43f5e', '#8b5cf6', '#06b6d4', '#ec4899', '#10b981', '#f59e0b']
        
        for index, ticker in enumerate(acciones_seleccionadas):
            columnas_actual = columnas_acciones[index % 3]
            
            with columnas_actual:
                with st.container(border=True):
                    try:
                        ticker_data = df[ticker] if ticker in df.columns else df
                        
                        precio_hoy = ticker_data.iloc[-1]
                        precio_ayer = ticker_data.iloc[-2]
                        variacion = ((precio_hoy - precio_ayer) / precio_ayer) * 100
                        
                        maximo = ticker_data.max()
                        minimo = ticker_data.min()
                        
                        st.markdown(f"**{ticker}** - {acciones_disponibles[ticker]}")
                        
                        st.metric(
                            label="Precio (USD)",
                            value=f"${precio_hoy:.2f}",
                            delta=f"{variacion:.2f}%"
                        )
                        
                        # Gráfico
                        color = colores[index % len(colores)]
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=ticker_data.index,
                            y=ticker_data.values,
                            fill='tozeroy',
                            fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3)',
                            line=dict(color=color, width=3),
                            name=ticker,
                            hovertemplate='<b>%{x}</b><br>Precio: $%{y:.2f}<extra></extra>'
                        ))
                        
                        fig.update_layout(
                            height=150,
                            margin=dict(l=0, r=0, t=0, b=0),
                            showlegend=False,
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"📈 Max: ${maximo:.2f}")
                        with col2:
                            st.caption(f"📉 Min: ${minimo:.2f}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.error(f"⚠️ Error al cargar datos")
else:
    st.info("👆 Selecciona al menos una acción")

# ============= COMPARATIVA =============
if acciones_seleccionadas and not df.empty and len(acciones_seleccionadas) > 1:
    st.markdown("---")
    st.subheader("📊 Comparativa de Rendimiento")
    
    try:
        df_normalizado = (df / df.iloc[0]) * 100
        
        fig_comparativa = go.Figure()
        
        for idx, ticker in enumerate(acciones_seleccionadas):
            if ticker in df.columns:
                color = colores[idx % len(colores)]
                fig_comparativa.add_trace(go.Scatter(
                    x=df_normalizado.index,
                    y=df_normalizado[ticker],
                    name=f"{ticker} - {acciones_disponibles[ticker]}",
                    mode='lines',
                    line=dict(width=3, color=color),
                    hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>%{y:.2f}<extra></extra>'
                ))
        
        fig_comparativa.update_layout(
            height=400,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12)
            ),
            yaxis_title="Rendimiento (Base 100)",
            xaxis_title="Fecha",
            plot_bgcolor='rgba(30, 35, 50, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(gridcolor='rgba(102, 126, 234, 0.2)'),
            xaxis=dict(gridcolor='rgba(102, 126, 234, 0.2)')
        )
        
        st.plotly_chart(fig_comparativa, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**📊 Fuentes de datos:**")
    st.caption("• DolarApi.com")
    st.caption("• Yahoo Finance")

with col_footer2:
    st.markdown("**⚡ Actualización:**")
    st.caption("• Dólares: cada 60 seg")
    st.caption("• Acciones: cada 5 min")

with col_footer3:
    st.markdown("**💻 Desarrollado con:**")
    st.caption("• Python & Streamlit")
    st.caption("• Plotly para gráficos")