import os
from flask import Flask
from flask_cors import CORS
from .routes.health import blp as health_blp
from .routes.user import blp as user_blp
from .routes.post import blp as post_blp
from .routes.comment import blp as comment_blp
from .routes.like import blp as like_blp
from .routes.feed import blp as feed_blp
from flask_smorest import Api
from .models import db

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})

# --- Database setup ---
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_URL', 'localhost')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -- API documentation setup
app.config["API_TITLE"] = "My Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

db.init_app(app)

api = Api(app)
# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(user_blp)
api.register_blueprint(post_blp)
api.register_blueprint(comment_blp)
api.register_blueprint(like_blp)
api.register_blueprint(feed_blp)
