from functools import wraps
from flask import abort
from flask_login import current_user


def roles_required(*roles):
    """
    Decorador robusto que verifica si el usuario tiene uno de los roles permitidos (insensible a mayúsculas).
    """
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            # Comparamos roles ignorando mayúsculas/minúsculas
            user_role = current_user.rol.lower()
            allowed_roles = [role.lower() for role in roles]
            if user_role not in allowed_roles:
                abort(403)
            return func(*args, **kwargs)
        return decorated_view
    return decorator
