from flask import Flask
from routes import api_bp
from config import Config
from service.db.redis import init_redis
from service.auth import auth_bp
from service.auth import init_jwt



app = Flask(__name__)
app.config.from_object(Config)
jwt = init_jwt(app)

# Initialize Redis client
init_redis(app)

app.register_blueprint(api_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
