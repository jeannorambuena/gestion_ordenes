from sqlalchemy.orm import foreign, remote
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates, relationship, backref, foreign
from sqlalchemy import Column, String, Integer, Date, Boolean, Text, Enum, ForeignKey, Float
from datetime import datetime
# from app import db
from app.extensions import db
# from app import login_manager
from app.extensions import login_manager


# Modelo: Alcaldia


class Alcaldia(db.Model):
    __tablename__ = 'alcaldia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Identificación del funcionario
    rut_cuerpo = db.Column(db.String(8), db.ForeignKey(
        'funcionarios.rut_cuerpo'), nullable=False)
    rut_dv = db.Column(db.String(1), nullable=False)

    # Datos de contacto heredados del funcionario
    email = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)

    # Fechas de vigencia
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_termino = db.Column(db.Date, nullable=True)

    # Futuro soporte para medias jornadas
    # hora_inicio = db.Column(db.Time, nullable=True)
    # hora_termino = db.Column(db.Time, nullable=True)

    # Cargo
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=True)

    # Estado activo para control de UI
    es_activo = db.Column(db.Boolean, default=False, nullable=False)

    # ✅ Nuevo: indica si es el alcalde titular de su periodo
    es_titular = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    funcionario = db.relationship(
        'Funcionarios',
        primaryjoin="and_(Alcaldia.rut_cuerpo==Funcionarios.rut_cuerpo, Alcaldia.rut_dv==Funcionarios.rut_dv)",
        backref='alcaldias'
    )

    cargo = db.relationship('Cargo', backref='alcaldias', lazy='joined')

# Modelo: Cargos


class Cargo(db.Model):
    __tablename__ = 'cargos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cargo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)

# Modelo: Colegios


class Colegios(db.Model):
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

# Modelo: Funcionarios


class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'

    id = Column(Integer, primary_key=True, autoincrement=True)  # NUEVO
    # Ya no es primary_key
    rut_cuerpo = Column(String(8), nullable=False)
    rut_dv = Column(String(1), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    titulo = Column(String(100), nullable=True)
    id_cargo = Column(Integer, ForeignKey('cargos.id'), nullable=True)

    cargo = relationship('Cargo', backref='funcionarios', lazy='joined')

# Modelo: Ordenes de Trabajo


class OrdenesTrabajo(db.Model):
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
        'funcionarios.id'), nullable=True)  # NUEVA CLAVE
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

# Modelo: Financiamiento


class Financiamiento(db.Model):
    __tablename__ = 'financiamiento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_financiamiento = Column(String(100), nullable=False)

# Modelo: Tipo de Contrato


class TipoContrato(db.Model):
    __tablename__ = 'tipo_contrato'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    observacion = Column(Text, nullable=True)

# Modelo: Historial de Cambios


class HistorialCambios(db.Model):
    __tablename__ = 'historial_cambios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tabla_afectada = Column(String(100), nullable=False)
    registro_id = Column(Integer, nullable=False)
    usuario_id = Column(Integer, nullable=False)
    tipo_cambio = Column(String(50), nullable=False)
    detalle_cambio = Column(Text, nullable=True)
    fecha_cambio = Column(Date, default=datetime.utcnow, nullable=False)

# Modelo: Usuario


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Modelo: Roles
class Rol(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)


class JefaturaDAEM(db.Model):
    __tablename__ = 'jefatura_daem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Identificación del funcionario asociado
    rut_cuerpo = db.Column(db.String(8), nullable=False)
    rut_dv = db.Column(db.String(1), nullable=False)

    # Cargo asignado
    id_cargo = db.Column(db.Integer, db.ForeignKey(
        'cargos.id'), nullable=False)

    # Fechas de vigencia del mandato
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_termino = db.Column(db.Date, nullable=True)

    # Estado actual
    es_activo = db.Column(db.Boolean, default=False, nullable=False)

    # ✅ Nuevo: indica si es el jefe DAEM titular
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


class Permiso(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Permiso {self.nombre}>"
