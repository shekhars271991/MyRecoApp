from service.db.redis import get_all_products as redis_get_all_products
from service.db.redis import add_product as redis_add_product
from service.db.redis import get_product_by_sku as redis_get_product_by_sku

def get_all_products():
    return redis_get_all_products()

def add_product(product):
    redis_add_product(product)

def get_product_by_sku(sku):
    return redis_get_product_by_sku(sku)



