"""Modelo de Colegios para el sistema de gestión de órdenes.

Representa a los establecimientos educacionales registrados en el sistema, con información clave para asignación de funcionarios y trazabilidad geográfica.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, String, Enum, Float


class Colegios(db.Model):
    """
    Representa un colegio o establecimiento educacional.

    Atributos:
        rbd (str): Código RBD, identificador único y clave primaria.
        nombre_colegio (str): Nombre del colegio.
        direccion (str): Dirección física.
        telefono (str): Teléfono de contacto.
        director (str): Nombre del director.
        email (str): Correo de contacto.
        tipo_ensenanza (Enum): Tipo de enseñanza ('BASICA', 'MEDIA').
        latitud (float): Latitud geográfica (opcional).
        longitud (float): Longitud geográfica (opcional).

    Ejemplo de uso:
        colegio = Colegios.query.filter_by(rbd="12345").first()
        print(colegio.nombre_colegio, colegio.tipo_ensenanza)
    """
    __tablename__ = 'colegios'

    rbd = Column(String(20), primary_key=True)
    nombre_colegio = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    director = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    tipo_ensenanza = Column(
        Enum('BASICA', 'MEDIA', name='tipo_ensenanza'), nullable=False)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Colegios rbd={self.rbd} nombre={self.nombre_colegio}>"
