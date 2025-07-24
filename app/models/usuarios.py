"""Modelo de Usuario para el sistema de gestión de órdenes.

Define los usuarios autenticados del sistema, sus credenciales y rol principal. Incluye integración con Flask-Login para la gestión de sesiones y autenticación segura.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String


class Usuario(UserMixin, db.Model):
    """
    Representa un usuario autenticado en el sistema.

    Atributos:
        id (int): Identificador único del usuario.
        nombre_usuario (str): Nombre de usuario único.
        contrasena_hash (str): Hash seguro de la contraseña.
        rol (str): Rol principal asignado al usuario.

    Métodos:
        set_password(password): Asigna y hashea la contraseña.
        check_password(password): Verifica la contraseña.

    Ejemplo de uso:
        user = Usuario(nombre_usuario='admin')
        user.set_password('secreto123')
        db.session.add(user)
        db.session.commit()
    """
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)

    def __repr__(self):
        return f"<Usuario id={self.id} nombre_usuario={self.nombre_usuario}>"
