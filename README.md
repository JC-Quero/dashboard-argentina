# 🇦🇷 Argie Market Live

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Status](https://img.shields.io/badge/Status-Live-success)

**Argie Market Live** es un dashboard financiero en tiempo real diseñado para monitorear la economía argentina. Combina datos del mercado cambiario (Dólar Blue, MEP, CCL) y el mercado bursátil (ADRs argentinos en Wall Street) en una interfaz unificada y estética.

🔗 **[Ver Demo en Vivo](https://TU-URL-DE-STREAMLIT.streamlit.app)** *(Reemplaza este link con tu URL real cuando la tengas)*

---

## 🚀 Características

* **Monitor de Dólar en Tiempo Real:** Conexión directa a la API `dolarapi.com` para obtener cotizaciones actualizadas de:
    * Dólar Oficial, Blue, MEP, CCL y Cripto.
* **Seguimiento de Acciones (ADRs):** Visualización de las principales empresas argentinas que cotizan en EE.UU. (GGAL, YPF, MELI, etc.).
* **Indicadores Visuales:**
    * 🟢 **Verde:** Tendencia alcista (Ganancia).
    * 🔴 **Rojo:** Tendencia bajista (Pérdida).
* **Gráficos Interactivos:** Gráficos de área para visualizar la tendencia de los últimos 30 días.
* **Interfaz Limpia:** Diseño "Single Page" optimizado para lectura rápida.

## 🛠️ Tecnologías Usadas

Este proyecto combina **Computer Science** con **Finanzas** utilizando:

* **Python:** Lenguaje principal.
* **Streamlit:** Framework para convertir scripts de datos en Web Apps.
* **Pandas:** Manipulación y análisis de datos financieros.
* **YFinance:** API de Yahoo Finance para datos históricos de acciones.
* **Requests:** Consumo de APIs REST.

## 💻 Instalación y Uso Local

Si quieres correr este proyecto en tu propia máquina:

1.  **Clonar el repositorio**
    ```bash
    git clone [https://github.com/TU_USUARIO/nombre-repo.git](https://github.com/TU_USUARIO/nombre-repo.git)
    cd nombre-repo
    ```

2.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación**
    ```bash
    streamlit run app_argentina.py
    ```

## 📂 Estructura del Proyecto

```text
├── app_argentina.py   # Lógica principal y UI
├── requirements.txt   # Librerías necesarias
├── README.md          # Documentación
└── .streamlit/
    └── config.toml    # Configuración de tema (Light Mode)
