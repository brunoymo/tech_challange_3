import sqlite3
import os
import requests # Biblioteca para fazer requisições HTTP (chamar a API)
import time     # Biblioteca para trabalhar com tempo (útil para agendamento)

# --- Configuração ---
# Substitua pela sua chave de API da OpenWeatherMap
API_KEY = '4040620ba54d85718409b1f4c7e599e3' 
CITY = 'São Paulo' # Cidade para a qual queremos o clima
DB_PATH = 'data/raw/weather_data.db'
TABLE_NAME = 'climate_records'

def initialize_database():
    """
    Cria o banco de dados e a tabela se eles não existirem.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            city TEXT NOT NULL,
            temperature_celsius REAL,
            weather_condition TEXT,
            humidity INTEGER,
            wind_speed_kmh REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Banco de dados '{DB_PATH}' inicializado com sucesso.")

def fetch_weather_data(api_key, city):
    """
    Busca os dados do clima atual para uma cidade específica usando a API OpenWeatherMap.
    """
    # URL da API. Usamos 'units=metric' para obter temperatura em Celsius e 'lang=pt_br' para descrição em português.
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br'
    
    try:
        response = requests.get(api_url)
        # Levanta um erro se a requisição falhou (ex: status 404 ou 500)
        response.raise_for_status() 
        
        data = response.json()
        
        # Extrai os dados que nos interessam
        weather_info = {
            "city": city,
            "temperature_celsius": data['main']['temp'],
            "weather_condition": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind_speed_kmh": data['wind']['speed'] * 3.6 # Converte de m/s para km/h
        }
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar a API: {e}")
        return None

def save_data_to_db(data):
    """
    Salva um registro de dados do clima no banco de dados SQLite.
    """
    if data is None:
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
        INSERT INTO {TABLE_NAME} (city, temperature_celsius, weather_condition, humidity, wind_speed_kmh)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['city'],
        data['temperature_celsius'],
        data['weather_condition'],
        data['humidity'],
        data['wind_speed_kmh']
    ))
    
    conn.commit()
    conn.close()
    print(f"Dados salvos para a cidade de {data['city']}: {data['temperature_celsius']}°C, {data['weather_condition']}.")

# --- Execução Principal ---
if __name__ == '__main__':
    # Garante que o banco de dados e a tabela existam na primeira vez que rodar
    initialize_database()
    
    # Define o intervalo de coleta em segundos (ex: 600 segundos = 10 minutos)
    INTERVALO_DE_COLETA_EM_SEGUNDOS = 600 

    print("--- Iniciando Coletor de Dados do Clima ---")
    print(f"As informações para a cidade de '{CITY}' serão coletadas a cada {INTERVALO_DE_COLETA_EM_SEGUNDOS / 60} minutos.")
    print("Pressione Ctrl+C para parar a execução.")

    try:
        while True:
            # 1. Busca os dados atuais do clima
            print(f"\nBuscando dados... (Horário: {time.strftime('%Y-%m-%d %H:%M:%S')})")
            weather_data = fetch_weather_data(API_KEY, CITY)
            
            # 2. Salva os dados no banco
            if weather_data:
                save_data_to_db(weather_data)
            else:
                print("Não foi possível obter os dados do clima nesta tentativa.")
            
            # 3. Aguarda o próximo ciclo
            print(f"Aguardando {INTERVALO_DE_COLETA_EM_SEGUNDOS / 60} minutos para a próxima coleta...")
            time.sleep(INTERVALO_DE_COLETA_EM_SEGUNDOS)

    except KeyboardInterrupt:
        print("\n--- Coletor de dados interrompido pelo usuário. ---")