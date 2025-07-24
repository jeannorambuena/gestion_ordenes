"""Modelo de Permiso para el sistema de gestión de órdenes.

Define los permisos individuales del sistema, permitiendo asignar granularidad y control fino sobre las acciones que los roles o usuarios pueden realizar.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db


class Permiso(db.Model):
    """
    Representa un permiso o privilegio específico dentro del sistema.

    Atributos:
        id (int): Identificador único.
        nombre (str): Nombre único del permiso.
        descripcion (str): Descripción opcional del permiso.

    Ejemplo de uso:
        permiso = Permiso(nombre='ver_reportes', descripcion='Acceso a reportes')
        db.session.add(permiso)
        db.session.commit()
    """
    __tablename__ = 'permisos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Permiso {self.nombre}>"
