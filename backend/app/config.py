import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env si existe localmente
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dale1mano_secret_key_prod_2026')

    # Configuración de MySQL adaptada para las variables del docker-compose
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'd1mcr_mysql_db')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'd1mcr_db')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
