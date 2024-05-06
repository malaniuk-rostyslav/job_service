import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRATION_TIME_IN_MINUTES = int(os.getenv('TOKEN_EXPIRATION_TIME_IN_MINUTES'))
