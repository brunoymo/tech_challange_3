import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega a URL do banco de dados da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Nenhuma DATABASE_URL encontrada. Verifique seu arquivo .env")

# --- ESSA É A PARTE CRUCIAL QUE RESOLVE O NOVO ERRO ---
# Adapta a URL para o novo driver 'psycopg' (v3)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
# ---------------------------------------------------------

# Engine de conexão com o banco
engine = create_engine(DATABASE_URL)

# Base para as classes de modelo (nossas tabelas)
Base = declarative_base()

# Define a classe do nosso modelo, que representa a tabela no banco
class ClimateRecord(Base):
    __tablename__ = 'climate_records' # Nome da tabela

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    city = Column(String, nullable=False)
    temperature_celsius = Column(Float)
    weather_condition = Column(String)
    humidity = Column(Integer)
    wind_speed_kmh = Column(Float)

# Função para criar a tabela no banco de dados
def init_db():
    """
    Cria a tabela no banco de dados se ela não existir.
    """
    Base.metadata.create_all(bind=engine)
    print("Tabela 'climate_records' criada com sucesso (se ainda não existia).")

# Cria uma sessão para interagir com o banco (usaremos isso na API)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)