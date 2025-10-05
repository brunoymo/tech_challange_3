# 👕 Sistema de Recomendação de Produtos com Base no Clima

## 📄 Descrição do Projeto
Este projeto implementa um pipeline de Machine Learning de ponta a ponta que fornece recomendações de produtos com base em dados de clima coletados em tempo real. O objetivo é demonstrar o ciclo de vida completo de um projeto de MLOps, desde a coleta de dados até a visualização em um dashboard interativo.

## 🏛️ Arquitetura do Pipeline
O sistema segue um fluxo de dados claro e modular:
1.  **Coleta de Dados:** Um script Python (`data_collector.py`) consome a API da OpenWeatherMap para obter dados climáticos atuais.
2.  **Armazenamento:** Os dados coletados são armazenados em um banco de dados SQLite (`weather_data.db`).
3.  **Modelo de ML:** Um modelo baseado em regras (`recommendation_model.py`) gera recomendações com base na condição do tempo e na temperatura.
4.  **API do Modelo:** Uma API REST criada com Flask (`api.py`) serve as recomendações do modelo, lendo os dados mais recentes do banco de dados.
5.  **Dashboard:** Uma aplicação web interativa desenvolvida com Streamlit (`app.py`) consome a API Flask e exibe os dados e as recomendações para o usuário final.

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **Coleta de Dados:** Requests
- **Banco de Dados:** SQLite3
- **API do Modelo:** Flask
- **Dashboard:** Streamlit
- **Controle de Versão:** Git & GitHub

## 🚀 Como Executar o Projeto

**Pré-requisitos:** Python 3.8+ instalado.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/NOME-DO-SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-SEU-REPOSITORIO.git)
    cd NOME-DO-SEU-REPOSITORIO
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure sua API Key:**
    - Abra o arquivo `src/data/data_collector.py`.
    - Insira sua chave da API OpenWeatherMap na variável `API_KEY`.

5.  **Execute os componentes (cada um em um terminal separado):**
    - **Terminal 1: Coletor de Dados**
      ```bash
      python src/data/data_collector.py
      ```
    - **Terminal 2: API do Modelo**
      ```bash
      python api.py
      ```
    - **Terminal 3: Dashboard**
      ```bash
      streamlit run app.py
      ```
6.  Acesse o dashboard no seu navegador através do endereço fornecido pelo Streamlit (geralmente `http://localhost:8501`).