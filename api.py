import os
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (API_KEY e DATABASE_URL)
load_dotenv()

# Importa os componentes do nosso módulo de banco de dados
from src.database import SessionLocal, ClimateRecord
# Importa o modelo de recomendação
from src.models.recommendation_model import get_recommendation

# Inicializa o aplicativo Flask
app = Flask(__name__)

# --- Lógica de Coleta de Dados (Movida para cá) ---

def fetch_weather_data():
    """
    Busca os dados do clima atual para uma cidade usando a API OpenWeatherMap.
    Lê a API_KEY e a CIDADE das variáveis de ambiente.
    """
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    CITY = os.getenv("CITY", "São Paulo") # Usa São Paulo como padrão

    if not API_KEY:
        print("Erro: A variável de ambiente OPENWEATHER_API_KEY não foi definida.")
        return None

    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            "city": CITY,
            "temperature_celsius": data['main']['temp'],
            "weather_condition": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind_speed_kmh": data['wind']['speed'] * 3.6
        }
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar a API de clima: {e}")
        return None

# --- Novas Rotas da API ---

@app.route('/trigger-collection', methods=['POST'])
def trigger_collection():
    """
    Endpoint para ser chamado externamente (pelo Cron Job).
    Ele busca os dados do clima e os salva no banco PostgreSQL.
    """
    print("Coleta de dados acionada...")
    weather_data = fetch_weather_data()

    if not weather_data:
        return jsonify({"status": "error", "message": "Falha ao buscar dados do clima."}), 500

    # Salva no banco de dados usando SQLAlchemy
    db = SessionLocal()
    try:
        new_record = ClimateRecord(**weather_data)
        db.add(new_record)
        db.commit()
        print("Dados salvos com sucesso no banco de dados.")
        return jsonify({"status": "success", "message": "Dados coletados e salvos."})
    except Exception as e:
        db.rollback()
        print(f"Erro ao salvar no banco de dados: {e}")
        return jsonify({"status": "error", "message": f"Erro no banco: {e}"}), 500
    finally:
        db.close()


@app.route('/recommendation', methods=['GET'])
def recommend():
    """
    Endpoint que lê o dado mais recente do banco PostgreSQL,
    gera uma recomendação e a retorna.
    """
    db = SessionLocal()
    try:
        # 1. Busca o registro de clima MAIS RECENTE no banco
        last_record = db.query(ClimateRecord).order_by(ClimateRecord.timestamp.desc()).first()

        if not last_record:
            return jsonify({"error": "Nenhum dado encontrado no banco de dados."}), 404

        # 2. Extrai os dados do registro
        weather_condition = last_record.weather_condition
        temperature = last_record.temperature_celsius

        # 3. Gera a recomendação usando nosso modelo importado
        recommendation_text = get_recommendation(weather_condition, temperature)

        # 4. Prepara a resposta em formato JSON
        response_data = {
            'latest_weather_data': {
                'city': last_record.city,
                'temperature_celsius': temperature,
                'weather_condition': weather_condition,
                'timestamp': last_record.timestamp.isoformat()
            },
            'recommendation': recommendation_text
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Erro ao buscar recomendação: {e}")
        return jsonify({"error": f"Ocorreu um erro interno: {e}"}), 500
    finally:
        db.close()


# --- Bloco para rodar o servidor localmente ---
if __name__ == '__main__':
    # Adicione sua chave da API de clima no arquivo .env para testes locais
    # Ex: OPENWEATHER_API_KEY="sua_chave_aqui"
    app.run(host='0.0.0.0', port=5000, debug=True)