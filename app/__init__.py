"""
Inicialización principal de la aplicación Flask.
Aquí se configuran extensiones, carga de usuario, registro de Blueprints y manejo global de errores.
"""

from flask import Flask, jsonify
from config import Config

# Importa extensiones (db, migrate, login_manager)
from app.extensions.extensions import db, migrate, login_manager

# Importa modelo de usuario para login
from app.models.models import Usuario

# Importa blueprint de autenticación
from app.auth import auth_bp

# Importa función central de registro de blueprints
from app.routes import registrar_blueprints


def create_app(config_class=Config):
    """
    Fábrica de la aplicación Flask.
    Configura la app, inicializa extensiones y registra blueprints.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # === Inicialización de extensiones ===
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # === Carga de usuario para Flask-Login ===
    @login_manager.user_loader
    def load_user(user_id):
        """Devuelve el usuario para la sesión dada su id."""
        return Usuario.query.get(int(user_id))

    # === Registro de Blueprints ===
    # Centraliza el registro usando la función del paquete routes
    registrar_blueprints(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # === Manejo global de errores ===
    @app.errorhandler(400)
    def bad_request(error):
        print(f"Error 400 capturado: {error}")
        return jsonify({'error': 'Bad request - revisa los datos enviados'}), 400

    @app.errorhandler(403)
    def forbidden(error):
        print(f"Error 403 capturado: {error}")
        return jsonify({'error': 'Forbidden: acceso no permitido'}), 403

    @app.errorhandler(500)
    def server_error(error):
        print(f"Error 500 capturado: {error}")
        return jsonify({'error': 'Internal server error'}), 500

    return app
