from flask import Flask
from flask_migrate import Migrate

from .extensions import db #, login_manager
from .routes.main_routes import main_routes
from .routes.dns_routes import dns_routes
from .routes.etcd_routes import etcd_routes
from .routes.docker_routes import docker_routes

from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)
    # login_manager.init_app(app)
    
    # Inicializa o Flask-Migrate
    migrate = Migrate(app, db)

    # Registra blueprints (rotas)
    app.register_blueprint(main_routes)
    app.register_blueprint(dns_routes)
    app.register_blueprint(etcd_routes)
    app.register_blueprint(docker_routes)

    return app
