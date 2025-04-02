from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from config import Config  # Asegúrate de importar Config

# Inicializar extensiones de Flask
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Asignar csrf.exempt para su uso en routes.py
    app.extensions['csrf_exempt'] = csrf.exempt

    # Registrar Blueprints
    from app.routes import (
        main_bp, cargo_bp, colegio_bp, funcionarios_colegios_bp, alcaldia_bp,
        jefatura_daem_bp, financiamiento_bp, roles_bp, historial_bp,
        ordenes_bp, funcionarios_bp, tipo_contrato_bp
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(cargo_bp, url_prefix='/cargos')
    app.register_blueprint(colegio_bp, url_prefix='/colegios')
    app.register_blueprint(funcionarios_colegios_bp,
                           url_prefix='/funcionarios_colegios')
    app.register_blueprint(alcaldia_bp, url_prefix='/alcaldia')
    app.register_blueprint(jefatura_daem_bp, url_prefix='/jefaturas_daem')
    app.register_blueprint(financiamiento_bp, url_prefix='/financiamiento')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(historial_bp, url_prefix='/historial_cambios')
    app.register_blueprint(ordenes_bp, url_prefix='/ordenes_trabajo')
    app.register_blueprint(funcionarios_bp, url_prefix='/funcionarios')
    app.register_blueprint(tipo_contrato_bp, url_prefix='/tipo_contrato')

    # Manejo de errores globales
    @app.errorhandler(400)
    def bad_request(error):
        print(f"Error 400 capturado: {error}")  # Para depuración
        return jsonify({'error': 'Bad request - revisa los datos enviados'}), 400

    @app.errorhandler(403)
    def forbidden(error):
        print(f"Error 403 capturado: {error}")  # Para depuración
        return jsonify({'error': 'Forbidden: CSRF token missing or incorrect'}), 403

    @app.errorhandler(500)
    def server_error(error):
        print(f"Error 500 capturado: {error}")  # Para depuración
        return jsonify({'error': 'Internal server error'}), 500

    return app
