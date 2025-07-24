"""Modelo de Cargo para el sistema de gestión de órdenes.

Define los diferentes cargos posibles para funcionarios y autoridades dentro del sistema.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, Integer, String


class Cargo(db.Model):
    """
    Representa un cargo o puesto dentro de la organización.

    Atributos:
        id (int): Identificador único y autoincremental.
        nombre_cargo (str): Nombre del cargo.
        descripcion (str): Descripción u observaciones sobre el cargo (opcional).

    Ejemplo de uso:
        cargo = Cargo.query.filter_by(nombre_cargo="Profesor").first()
        print(cargo.nombre_cargo, cargo.descripcion)
    """
    __tablename__ = 'cargos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cargo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Cargo id={self.id} nombre={self.nombre_cargo}>"
