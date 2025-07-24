"""Modelo de Alcaldia para el sistema de gestión de órdenes.

Representa la designación de alcaldes (titular o suplente) vinculados a funcionarios y cargos, con soporte para fechas de vigencia y control de estado.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db


class Alcaldia(db.Model):
    """
    Representa una asignación de alcalde en el sistema.

    Atributos:
        id (int): Identificador único y autoincremental.
        rut_cuerpo (str): Parte numérica del RUT del funcionario (FK a funcionarios).
        rut_dv (str): Dígito verificador del funcionario.
        email (str): Correo electrónico del alcalde (heredado del funcionario).
        telefono (str): Teléfono del alcalde.
        fecha_inicio (date): Fecha de inicio de vigencia.
        fecha_termino (date): Fecha de término (si aplica).
        id_cargo (int): ID del cargo asociado.
        es_activo (bool): Indica si la asignación está vigente.
        es_titular (bool): Indica si es el alcalde titular.

    Relaciones:
        funcionario (Funcionarios): Funcionario designado como alcalde.
        cargo (Cargo): Cargo asociado.

    Ejemplo de uso:
        alcaldia = Alcaldia.query.filter_by(es_activo=True).first()
        print(alcaldia.funcionario.nombre, alcaldia.fecha_inicio)
    """
    __tablename__ = 'alcaldia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rut_cuerpo = db.Column(db.String(8), db.ForeignKey(
        'funcionarios.rut_cuerpo'), nullable=False)
    rut_dv = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_termino = db.Column(db.Date, nullable=True)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=True)
    es_activo = db.Column(db.Boolean, default=False, nullable=False)
    es_titular = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    funcionario = db.relationship(
        'Funcionarios',
        primaryjoin="and_(Alcaldia.rut_cuerpo==Funcionarios.rut_cuerpo, Alcaldia.rut_dv==Funcionarios.rut_dv)",
        backref='alcaldias'
    )
    cargo = db.relationship('Cargo', backref='alcaldias', lazy='joined')

    def __repr__(self):
        return f"<Alcaldia id={self.id} rut={self.rut_cuerpo}-{self.rut_dv} activo={self.es_activo} titular={self.es_titular}>"
