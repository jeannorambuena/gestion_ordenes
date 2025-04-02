import os


class Config:
    # Clave secreta para sesiones y protección CSRF
    SECRET_KEY = 'Pascuala2013*'  # No olvides cambiar esto para producción

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/gestion_ordenes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Protección CSRF
    WTF_CSRF_ENABLED = False  # Habilita CSRF en formularios
    # Métodos HTTP que requieren CSRF
    # WTF_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    # WTF_CSRF_CHECK_DEFAULT = True  # Verifica CSRF en solicitudes AJAX
    # Deshabilita la expiración del token CSRF para formularios largos
    # WTF_CSRF_TIME_LIMIT = None

    # Configuraciones adicionales para manejo de JSON
    JSONIFY_PRETTYPRINT_REGULAR = False
    JSON_SORT_KEYS = False
