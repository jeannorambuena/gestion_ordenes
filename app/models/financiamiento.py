"""Modelo de Financiamiento para el sistema de gestión de órdenes.

Representa las fuentes o tipos de financiamiento posibles para contratos u órdenes de trabajo.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, Integer, String


class Financiamiento(db.Model):
    """
    Representa un tipo o fuente de financiamiento en el sistema.

    Atributos:
        id (int): Identificador único y autoincremental.
        nombre_financiamiento (str): Nombre descriptivo del financiamiento.

    Ejemplo de uso:
        financiamiento = Financiamiento.query.filter_by(nombre_financiamiento="PIE").first()
        print(financiamiento.nombre_financiamiento)
    """
    __tablename__ = 'financiamiento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_financiamiento = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Financiamiento id={self.id} nombre={self.nombre_financiamiento}>"
