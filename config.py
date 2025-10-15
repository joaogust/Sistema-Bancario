import os
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do ambiente .env para dentro do sistema

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
    POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
    POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
    POSTGRESQL_DATABASE = os.getenv('POSTGRESQL_DATABASE')