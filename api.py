import sqlite3
from flask import Flask, jsonify

# Importa nossa função de recomendação
from src.models.recommendation_model import get_recommendation

# Define o caminho para o banco de dados
DB_PATH = 'data/raw/weather_data.db'
TABLE_NAME = 'climate_records'

# Inicializa o aplicativo Flask
app = Flask(__name__)

@app.route('/recommendation', methods=['GET'])
def recommend():
    """
    Endpoint da API que retorna a recomendação mais recente.
    """
    conn = None
    try:
        # 1. Conecta ao banco de dados
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
        cursor = conn.cursor()
        
        # 2. Busca o registro de clima MAIS RECENTE
        cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC LIMIT 1")
        last_record = cursor.fetchone()
        
        if last_record is None:
            return jsonify({"error": "Nenhum dado encontrado no banco de dados."}), 404
            
        # 3. Extrai os dados do registro
        weather_condition = last_record['weather_condition']
        temperature = last_record['temperature_celsius']
        
        # 4. Gera a recomendação usando nosso modelo
        recommendation_text = get_recommendation(weather_condition, temperature)
        
        # 5. Prepara a resposta em formato JSON
        response_data = {
            'latest_weather_data': {
                'city': last_record['city'],
                'temperature_celsius': temperature,
                'weather_condition': weather_condition,
                'timestamp': last_record['timestamp']
            },
            'recommendation': recommendation_text
        }
        
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {e}"}), 500
    finally:
        if conn:
            conn.close()

# --- Bloco para rodar o servidor da API ---
if __name__ == '__main__':
    # host='0.0.0.0' permite que a API seja acessível na sua rede local
    # port=5000 define a porta
    app.run(host='0.0.0.0', port=5000, debug=True)