from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes.proyectos import proyectos_bp
from .routes.auth import auth_bp
from .routes.testimonios import testimonios_bp
from .routes.junta import junta_bp

def create_app():
    """
    Factory function para inicializar la aplicación Flask.
    Configura CORS, carga los parámetros del sistema y registra los blueprints de rutas.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Habilitar CORS para permitir solicitudes del Frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar rutas (Blueprints) del sistema modular
    app.register_blueprint(proyectos_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(testimonios_bp)
    app.register_blueprint(junta_bp)

    return app