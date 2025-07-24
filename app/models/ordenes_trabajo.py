"""Modelo de OrdenesTrabajo para el sistema de gestión de órdenes.

Representa una orden de trabajo asociada a funcionarios, colegios, contratos y autoridades, permitiendo la trazabilidad completa de las asignaciones y sus relaciones clave.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db
from sqlalchemy import Column, Integer, Date, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class OrdenesTrabajo(db.Model):
    """
    Representa una orden de trabajo emitida a un funcionario.

    Atributos:
        id (int): Identificador único.
        numero_orden (int): Número correlativo de orden.
        anio (int): Año de emisión.
        fecha_inicio (date): Inicio de vigencia.
        fecha_termino (date): Fin de vigencia (opcional).
        es_indefinido (bool): Si la orden es indefinida.
        observaciones (str): Observaciones administrativas.
        horas_disponibles (int): Horas asignadas en esta orden.
        colegio_rbd (str): RBD del colegio asignado.
        tipo_contrato_id (int): Tipo de contrato asociado.
        financiamiento_id (int): Tipo de financiamiento.
        rut_cuerpo (str): Parte numérica del RUT del funcionario (relación).
        rut_dv (str): Dígito verificador del funcionario (relación).
        funcionario_id (int): ID directo del funcionario.
        alcalde_id (int): ID del alcalde que autoriza.
        jefatura_daem_id (int): ID de la jefatura DAEM responsable.

    Relaciones:
        funcionario (Funcionarios): Funcionario asociado (por RUT).
        funcionario_directo (Funcionarios): Funcionario (por ID directo).
        tipo_contrato (TipoContrato): Tipo de contrato.
        financiamiento (Financiamiento): Financiamiento asociado.
        colegio (Colegios): Colegio asignado.
        alcalde (Alcaldia): Alcalde responsable.
        jefatura_daem (JefaturaDAEM): Jefatura DAEM asociada.

    Ejemplo de uso:
        orden = OrdenesTrabajo.query.filter_by(numero_orden=42, anio=2025).first()
        print(orden.funcionario.nombres, orden.colegio.nombre_colegio)
    """
    __tablename__ = 'ordenes_trabajo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_orden = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False, default=datetime.now().year)
    fecha_inicio = Column(Date, nullable=False)
    fecha_termino = Column(Date, nullable=True)
    es_indefinido = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)
    horas_disponibles = Column(Integer, nullable=False, default=0)
    colegio_rbd = Column(String(20), ForeignKey('colegios.rbd'), nullable=True)
    tipo_contrato_id = Column(Integer, ForeignKey(
        'tipo_contrato.id'), nullable=True)
    financiamiento_id = Column(Integer, ForeignKey(
        'financiamiento.id'), nullable=True)
    rut_cuerpo = Column(String(8), nullable=False)
    rut_dv = Column(String(1), nullable=False)
    funcionario_id = Column(Integer, ForeignKey(
        'funcionarios.id'), nullable=True)
    alcalde_id = Column(Integer, ForeignKey('alcaldia.id'), nullable=False)
    jefatura_daem_id = Column(Integer, ForeignKey(
        'jefatura_daem.id'), nullable=False)

    # Relaciones
    funcionario = relationship(
        'Funcionarios',
        primaryjoin="and_(foreign(OrdenesTrabajo.rut_cuerpo) == Funcionarios.rut_cuerpo, "
                    "foreign(OrdenesTrabajo.rut_dv) == Funcionarios.rut_dv)",
        backref='ordenes_trabajo'
    )

    funcionario_directo = relationship(
        'Funcionarios',
        foreign_keys=[funcionario_id],
        backref='ordenes_directas'
    )

    tipo_contrato = relationship('TipoContrato', backref='ordenes_trabajo')
    financiamiento = relationship('Financiamiento', backref='ordenes_trabajo')
    colegio = relationship('Colegios', backref='ordenes_trabajo')
    alcalde = relationship('Alcaldia', backref='ordenes_trabajo')
    jefatura_daem = relationship('JefaturaDAEM', backref='ordenes_trabajo')

    def __repr__(self):
        return f"<OrdenesTrabajo id={self.id} numero={self.numero_orden}/{self.anio}>"
