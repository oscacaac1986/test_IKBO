from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
api = Api()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    api.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from app.routes.product_routes import blp as products_blp
    api.register_blueprint(products_blp)
    
    return app