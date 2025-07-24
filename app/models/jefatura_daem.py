"""Modelo de JefaturaDAEM para el sistema de gestión de órdenes.

Representa la asignación de jefe DAEM (titular o suplente), vinculado a un funcionario y a un cargo, con control de vigencia y estado.

Autor: Jean Paul Norambuena
Fecha: 2025-07-23
"""

from app import db


class JefaturaDAEM(db.Model):
    """
    Representa una designación de jefe DAEM en el sistema.

    Atributos:
        id (int): Identificador único y autoincremental.
        rut_cuerpo (str): Parte numérica del RUT del funcionario.
        rut_dv (str): Dígito verificador.
        id_cargo (int): ID del cargo asignado.
        fecha_inicio (date): Inicio de vigencia.
        fecha_termino (date): Término de vigencia (puede ser nulo).
        es_activo (bool): Si el mandato está activo.
        es_titular (bool): Indica si es titular.

    Relaciones:
        cargo (Cargo): Cargo asociado.
        funcionario (Funcionarios): Funcionario designado como jefe DAEM.

    Ejemplo de uso:
        jefatura = JefaturaDAEM.query.filter_by(es_activo=True).first()
        print(jefatura.funcionario.nombre, jefatura.fecha_inicio)
    """
    __tablename__ = 'jefatura_daem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rut_cuerpo = db.Column(db.String(8), nullable=False)
    rut_dv = db.Column(db.String(1), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey(
        'cargos.id'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_termino = db.Column(db.Date, nullable=True)
    es_activo = db.Column(db.Boolean, default=False, nullable=False)
    es_titular = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    cargo = db.relationship('Cargo', backref='jefaturas_daem')
    funcionario = db.relationship(
        "Funcionarios",
        primaryjoin="and_(foreign(JefaturaDAEM.rut_cuerpo) == remote(Funcionarios.rut_cuerpo), "
                    "foreign(JefaturaDAEM.rut_dv) == remote(Funcionarios.rut_dv))",
        viewonly=True,
        uselist=False
    )

    def __repr__(self):
        return f"<JefaturaDAEM RUT={self.rut_cuerpo}-{self.rut_dv}>"
