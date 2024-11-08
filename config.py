import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG = True
