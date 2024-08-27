import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    LOAD_SAMPLE_PRODUCTS = os.environ.get('LOAD_SAMPLE_PRODUCTS', 'true').lower() in ['true', '1', 't']

