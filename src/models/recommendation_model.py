def get_recommendation(weather_condition, temperature):
    """
    Gera uma recomendação de produto com base na condição do tempo e na temperatura.
    
    Args:
        weather_condition (str): A descrição do tempo (ex: 'chuva leve', 'céu limpo').
        temperature (float): A temperatura em graus Celsius.
        
    Returns:
        str: Uma string com a recomendação de produtos.
    """
    weather_condition = weather_condition.lower() # Converte para minúsculas para facilitar a comparação

    # Regra 1: Condições de Chuva
    if 'chuva' in weather_condition or 'chuvisco' in weather_condition:
        return "Para o dia de hoje, recomendamos: Guarda-chuva, capa de chuva e calçados impermeáveis."
        
    # Regra 2: Frio Intenso
    elif temperature < 15:
        return "Está frio! Recomendamos: Casaco, cachecol, luvas e bebidas quentes."

    # Regra 3: Calor Intenso e Céu Limpo
    elif temperature > 25 and ('céu limpo' in weather_condition or 'sol' in weather_condition):
        return "Dia de sol e calor! Recomendamos: Protetor solar, óculos de sol, boné e roupas leves."
        
    # Regra 4: Clima Ameno
    else:
        return "O tempo está agradável. Uma jaqueta leve pode ser uma boa ideia. Aproveite o dia!"

# --- Bloco de Teste ---
# Este código só roda quando executamos este arquivo diretamente
if __name__ == '__main__':
    print("--- Testando o Modelo de Recomendação ---")
    
    # Cenário 1: Dia chuvoso
    rec_1 = get_recommendation('chuva moderada', 18)
    print(f"Cenário: 'chuva moderada', 18°C -> Recomendação: {rec_1}")
    
    # Cenário 2: Dia frio
    rec_2 = get_recommendation('parcialmente nublado', 12)
    print(f"Cenário: 'parcialmente nublado', 12°C -> Recomendação: {rec_2}")
    
    # Cenário 3: Dia quente e ensolarado
    rec_3 = get_recommendation('céu limpo', 28)
    print(f"Cenário: 'céu limpo', 28°C -> Recomendação: {rec_3}")

    # Cenário 4: Dia ameno
    rec_4 = get_recommendation('nuvens dispersas', 21)
    print(f"Cenário: 'nuvens dispersas', 21°C -> Recomendação: {rec_4}")