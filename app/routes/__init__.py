# app/routes/__init__.py

# Importa los blueprints de cada módulo de rutas
from .ordenes_trabajo import ordenes_bp
from .funcionarios import funcionarios_bp
from .colegios import colegio_bp
from .cargos import cargo_bp
from .tipo_contrato import tipo_contrato_bp
from .financiamiento import financiamiento_bp
from .alcaldia import alcaldia_bp
from .jefatura_daem import jefatura_daem_bp
from .usuarios import usuarios_bp
from .roles import roles_bp

# Función que registra todos los blueprints en la aplicación Flask


def registrar_blueprints(app):
    app.register_blueprint(ordenes_bp, url_prefix='/ordenes_trabajo')
    app.register_blueprint(
        funcionarios_bp, url_prefix='/funcionarios')  #
    app.register_blueprint(colegio_bp, url_prefix='/colegios')
    app.register_blueprint(cargo_bp, url_prefix='/cargos')
    app.register_blueprint(tipo_contrato_bp, url_prefix='/tipo_contrato')
    app.register_blueprint(financiamiento_bp, url_prefix='/financiamiento')
    app.register_blueprint(alcaldia_bp, url_prefix='/alcaldia')
    app.register_blueprint(jefatura_daem_bp, url_prefix='/jefaturas_daem')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(roles_bp, url_prefix='/roles')
