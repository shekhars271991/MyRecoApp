import redis
import json
import os
import bcrypt

redis_client = None


def init_redis(app):
    global redis_client
    redis_client = redis.from_url(app.config['REDIS_URL'])

def get_all_products():
    products = []
    for key in redis_client.scan_iter("product:*"):
        product = redis_client.get(key)
        products.append(json.loads(product))
    return products

def add_product(product):
    product_id = product['sku']
    redis_client.json().set(f"product:{product_id}", '.',product)


def load_sample_products():
    sample_data_file = os.path.join(os.path.dirname(__file__), '../../data/products.json')
    if os.path.exists(sample_data_file):
        with open(sample_data_file, 'r') as f:
            products = json.load(f)
            for product in products:
                add_product(product)
        print("Sample products loaded into Redis.")

def get_product_by_sku(sku):
    product= redis_client.json().get(f"product:{sku}")    
    return product


def get_user(username):
    user_data = redis_client.get(f"user:{username}")
    return json.loads(user_data) if user_data else None

def check_key(key):
    return redis_client.exists(key)

def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {
        "username": username,
        "password": hashed_password,
    }
    redis_client.set(f"user:{username}", json.dumps(user_data))
