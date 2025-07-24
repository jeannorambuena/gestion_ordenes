"""Modelo de TipoContrato para el sistema de gestión de órdenes.

Representa los distintos tipos de contrato que pueden estar asociados a funcionarios u órdenes de trabajo.
Incluye nombre descriptivo y observaciones adicionales.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, Integer, String, Text


class TipoContrato(db.Model):
    """
    Representa un tipo de contrato dentro del sistema.

    Atributos:
        id (int): Identificador único y autoincremental.
        nombre (str): Nombre descriptivo del tipo de contrato.
        observacion (str): Observaciones adicionales sobre el tipo de contrato.

    Ejemplo de uso:
        tipo = TipoContrato.query.filter_by(nombre="Planta").first()
        print(tipo.nombre, tipo.observacion)
    """
    __tablename__ = 'tipo_contrato'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    observacion = Column(Text, nullable=True)

    def __repr__(self):
        return f"<TipoContrato id={self.id} nombre={self.nombre}>"
