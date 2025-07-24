"""Modelo de Rol para el sistema de gestión de órdenes.

Define los distintos roles de usuario dentro del sistema, permitiendo una administración flexible de permisos y accesos.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, Integer, String, Text


class Rol(db.Model):
    """
    Representa un rol de usuario en el sistema.

    Atributos:
        id (int): Identificador único y autoincremental.
        nombre_rol (str): Nombre único del rol (ej: 'Administrador').
        descripcion (str): Descripción opcional del rol.

    Ejemplo de uso:
        rol = Rol(nombre_rol='Supervisor', descripcion='Acceso limitado')
        db.session.add(rol)
        db.session.commit()
    """
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Rol id={self.id} nombre={self.nombre_rol}>"
