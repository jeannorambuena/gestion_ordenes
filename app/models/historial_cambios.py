"""Modelo de HistorialCambios para el sistema de gestión de órdenes.

Permite registrar y auditar todas las modificaciones relevantes realizadas en las distintas tablas del sistema, facilitando la trazabilidad y la revisión de cambios.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, Integer, String, Text, Date
from datetime import datetime


class HistorialCambios(db.Model):
    """
    Representa un registro de cambio o auditoría en una tabla específica del sistema.

    Atributos:
        id (int): Identificador único del historial.
        tabla_afectada (str): Nombre de la tabla modificada.
        registro_id (int): ID del registro afectado.
        usuario_id (int): ID del usuario que realizó el cambio.
        tipo_cambio (str): Tipo de cambio ('INSERT', 'UPDATE', 'DELETE', etc.).
        detalle_cambio (str): Detalle u observación del cambio.
        fecha_cambio (date): Fecha y hora del cambio.

    Ejemplo de uso:
        log = HistorialCambios(
            tabla_afectada='ordenes_trabajo',
            registro_id=123,
            usuario_id=1,
            tipo_cambio='UPDATE',
            detalle_cambio='Cambio de fecha_termino',
        )
        db.session.add(log)
        db.session.commit()
    """
    __tablename__ = 'historial_cambios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tabla_afectada = Column(String(100), nullable=False)
    registro_id = Column(Integer, nullable=False)
    usuario_id = Column(Integer, nullable=False)
    tipo_cambio = Column(String(50), nullable=False)
    detalle_cambio = Column(Text, nullable=True)
    fecha_cambio = Column(Date, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<HistorialCambios id={self.id} tabla={self.tabla_afectada} tipo={self.tipo_cambio}>"
