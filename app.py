import streamlit as st
import requests
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="Sistema de Recomendação",
    page_icon="🌤️",
    layout="centered"
)

# --- Título e Descrição ---
st.title("👕 Sistema de Recomendação de Produtos com Base no Clima")
st.write(
    "Este dashboard mostra o clima atual em tempo real e sugere produtos adequados para as condições."
)

# --- Comunicação com a API ---
API_URL = "http://localhost:5000/recommendation"

def get_data_from_api():
    """Busca dados da nossa API Flask."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lança um erro se a resposta não for 200 (OK)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Não foi possível conectar à API. Verifique se o servidor `api.py` está rodando. Erro: {e}")
        return None

# --- Layout do Dashboard ---
# Usamos um placeholder para poder atualizar o conteúdo sem recarregar a página inteira
placeholder = st.empty()

# --- Loop de Atualização Automática ---
while True:
    data = get_data_from_api()
    
    # Usa o container do placeholder para reescrever o conteúdo
    with placeholder.container():
        if data:
            weather_info = data.get('latest_weather_data', {})
            recommendation = data.get('recommendation', 'Nenhuma recomendação disponível.')
            
            st.header(f"Clima atual em: {weather_info.get('city', 'N/A')}")
            
            # Divide a tela em 2 colunas para melhor visualização
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🌡️ Temperatura", f"{weather_info.get('temperature_celsius', 0):.1f} °C")
            with col2:
                st.metric("🌦️ Condição", f"{weather_info.get('weather_condition', 'N/A').capitalize()}")

            st.success(f"💡 **Recomendação:** {recommendation}")
            
            st.info(f"Dados atualizados em: {weather_info.get('timestamp', 'N/A')}")
        else:
            st.warning("Aguardando dados da API...")
            
    # Define o intervalo de atualização em segundos
    time.sleep(10)