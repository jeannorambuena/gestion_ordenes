"""Modelo de Funcionarios para el sistema de gestión de órdenes.

Define la estructura, relaciones y atributos asociados a los funcionarios registrados.
Cada funcionario puede ser asignado a una orden de trabajo y tener vínculo con un usuario
(para autenticación y trazabilidad).

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Funcionarios(db.Model):
    """
    Representa a un funcionario registrado en el sistema.

    Atributos:
        id (int): Identificador único y autoincremental.
        rut_cuerpo (str): Parte numérica del RUT chileno.
        rut_dv (str): Dígito verificador del RUT chileno.
        nombre (str): Nombres del funcionario.
        apellido (str): Apellidos del funcionario.
        direccion (str): Dirección del funcionario.
        telefono (str): Teléfono de contacto.
        email (str): Correo electrónico.
        titulo (str): Título profesional u ocupacional.
        id_cargo (int): ID del cargo asociado (clave foránea a Cargo).

    Relaciones:
        cargo (Cargo): Cargo asociado al funcionario.

    Ejemplo de uso:
        funcionario = Funcionarios.query.filter_by(rut_cuerpo="12345678", rut_dv="9").first()
        print(funcionario.nombre, funcionario.cargo.nombre)
    """
    __tablename__ = 'funcionarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rut_cuerpo = Column(String(8), nullable=False)
    rut_dv = Column(String(1), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    titulo = Column(String(100), nullable=True)
    id_cargo = Column(Integer, ForeignKey('cargos.id'), nullable=True)

    # Relaciones
    cargo = relationship('Cargo', backref='funcionarios', lazy='joined')

    def __repr__(self):
        return f"<Funcionarios id={self.id} rut={self.rut_cuerpo}-{self.rut_dv} nombre={self.nombre}>"
