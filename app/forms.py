# Importaciones necesarias para formularios, modelos, validadores y base de datos
from app.validators import validar_rut
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import StringField, DateField, SelectField, SubmitField
from app.validators import validar_rut  # 👈 Importante
from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateField, BooleanField, SelectField,
    TextAreaField, FloatField, PasswordField, SubmitField
)
from wtforms.validators import (
    DataRequired, Optional, NumberRange, ValidationError, Length, Email, EqualTo
)

from app import db
from app.models import (
    OrdenesTrabajo, TipoContrato, Funcionarios, Colegios,
    Financiamiento, Alcaldia, JefaturaDAEM  # 👈 aquí todo lo que necesitas
)
from app.validators import validar_rut  # 👈 solo una vez es suficiente


# -------------------------------------------------------------
# Formularios para "Ordenes de Trabajo"
# -------------------------------------------------------------
class OrdenTrabajoForm(FlaskForm):
    """
    Formulario para gestionar la creación y edición de órdenes de trabajo.
    """
    rut_cuerpo = StringField('RUT Cuerpo', validators=[DataRequired()])
    rut_dv = StringField('Dígito Verificador', validators=[
        DataRequired(), Length(min=1, max=1)])
    colegio_rbd = SelectField('Colegio', coerce=str,
                              choices=[], validators=[DataRequired()])
    tipo_contrato = SelectField(
        'Tipo de Contrato', coerce=int, choices=[], validators=[DataRequired()])
    financiamiento = SelectField(
        # 🔹 Nuevo campo agregado
        'Financiamiento', coerce=int, choices=[], validators=[DataRequired()])
    fecha_inicio = DateField(
        'Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_termino = DateField(
        'Fecha de Término', format='%Y-%m-%d', validators=[Optional()])
    horas_disponibles = IntegerField(
        'Horas Disponibles', validators=[DataRequired(), NumberRange(min=1, max=44)])
    alcalde_id = SelectField('Alcalde o Alcaldesa',
                             coerce=int, validators=[DataRequired()])
    jefatura_daem_id = SelectField(
        'Jefe(a) DAEM', coerce=int, validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[
        Optional(), Length(max=500)])
    es_indefinido = BooleanField('Es Indefinido', default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar dinámicamente los colegios disponibles
        self.colegio_rbd.choices = [(col.rbd, col.nombre_colegio)
                                    for col in Colegios.query.all()]
        if not self.colegio_rbd.choices:
            self.colegio_rbd.choices = [('', 'No hay colegios disponibles')]

        # Cargar dinámicamente los tipos de contrato disponibles
        self.tipo_contrato.choices = [(tc.id, tc.nombre)
                                      for tc in TipoContrato.query.all()]
        if not self.tipo_contrato.choices:
            self.tipo_contrato.choices = [
                ('', 'No hay tipos de contrato disponibles')]

        # 🔹 Cargar dinámicamente los tipos de financiamiento disponibles
        self.financiamiento.choices = [(f.id, f.nombre_financiamiento)
                                       for f in Financiamiento.query.all()]
        if not self.financiamiento.choices:
            self.financiamiento.choices = [
                ('', 'No hay financiamientos disponibles')]

            # Cargar alcaldes disponibles
        alcaldes = Alcaldia.query.order_by(Alcaldia.fecha_inicio.desc()).all()
        self.alcalde_id.choices = [
            (a.id, f"{a.nombre_alcalde} ({a.cargo})") for a in alcaldes]
        if alcaldes:
            actual = next(
                (a for a in alcaldes if a.fecha_termino is None), alcaldes[0])
            self.alcalde_id.data = actual.id

        # Cargar jefaturas DAEM disponibles
        jefaturas = JefaturaDAEM.query.order_by(
            JefaturaDAEM.fecha_inicio.desc()).all()
        self.jefatura_daem_id.choices = [
            (j.id, f"{j.nombre} ({j.cargo_jefatura})") for j in jefaturas]
        if jefaturas:
            actual = next(
                (j for j in jefaturas if j.fecha_termino is None), jefaturas[0])
            self.jefatura_daem_id.data = actual.id

    def validate_horas_disponibles(self, field):
        """
        Valida que las horas disponibles sean correctas y dentro del rango permitido.
        """
        if field.data < 1 or field.data > 44:
            raise ValidationError(
                "Las horas disponibles deben estar entre 1 y 44.")

    def validate_rut_cuerpo(self, field):
        """
        Valida que el RUT sea correcto según el validador `validar_rut`.
        """
        if not validar_rut(self.rut_cuerpo.data, self.rut_dv.data):
            raise ValidationError("El RUT ingresado es inválido.")

# -------------------------------------------------------------
# Formularios para "Funcionarios"
# -------------------------------------------------------------


class FuncionarioForm(FlaskForm):
    """
    Formulario para gestionar la creación y edición de funcionarios.
    """
    rut_cuerpo = StringField('Cuerpo del RUT', validators=[
        DataRequired(message="El cuerpo del RUT es obligatorio."),
        Length(min=7, max=8,
               message="El cuerpo del RUT debe tener entre 7 y 8 dígitos.")
    ])
    rut_dv = StringField('Dígito Verificador', validators=[
        DataRequired(message="El dígito verificador es obligatorio."),
        Length(min=1, max=1, message="El dígito verificador debe ser un carácter.")
    ])
    nombre = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(max=100, message="El nombre no puede exceder los 100 caracteres.")
    ])
    apellido = StringField('Apellido', validators=[
        DataRequired(message="El apellido es obligatorio."),
        Length(max=100, message="El apellido no puede exceder los 100 caracteres.")
    ])
    direccion = StringField('Dirección', validators=[Length(max=255)])
    telefono = StringField('Teléfono', validators=[
        DataRequired(), Length(min=9, max=9, message="El teléfono debe tener 9 dígitos.")
    ])
    titulo = StringField('Título', validators=[Length(max=100)])
    id_cargo = SelectField('Cargo', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        if edit_mode:
            self.rut_cuerpo.render_kw = {'readonly': True}
            self.rut_dv.render_kw = {'readonly': True}


class CargoForm(FlaskForm):
    nombre_cargo = StringField('Nombre del Cargo', validators=[
                               DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=255)])
    submit = SubmitField('Guardar')


class FuncionarioColegiosForm(FlaskForm):
    rut_cuerpo = SelectField('Funcionario', coerce=str,
                             validators=[DataRequired()])
    colegio_rbd = SelectField('Colegio', coerce=str,
                              validators=[DataRequired()])
    horas_disponibles = IntegerField('Horas Disponibles', validators=[
                                     DataRequired(), NumberRange(min=1, max=44)])
    submit = SubmitField('Guardar')

    def __init__(self, *args, current_funcionario=None, current_colegio=None, **kwargs):
        super(FuncionarioColegiosForm, self).__init__(*args, **kwargs)

        # Cargar opciones para los SelectField
        funcionarios = Funcionarios.query.all()
        self.rut_cuerpo.choices = [
            (func.rut_cuerpo, f"{func.nombre} {func.apellido}")
            for func in funcionarios
        ]
        if not self.rut_cuerpo.choices:
            self.rut_cuerpo.choices = [('', 'No hay funcionarios disponibles')]

        colegios = Colegios.query.all()
        self.colegio_rbd.choices = [
            (col.rbd, col.nombre_colegio) for col in colegios
        ]
        if not self.colegio_rbd.choices:
            self.colegio_rbd.choices = [('', 'No hay colegios disponibles')]

        # Validar y asignar valores actuales al formulario
        if current_funcionario and any(current_funcionario == choice[0] for choice in self.rut_cuerpo.choices):
            self.rut_cuerpo.data = current_funcionario
        else:
            self.rut_cuerpo.data = self.rut_cuerpo.choices[0][0] if self.rut_cuerpo.choices else ''

        if current_colegio and any(current_colegio == choice[0] for choice in self.colegio_rbd.choices):
            self.colegio_rbd.data = current_colegio
        else:
            self.colegio_rbd.data = self.colegio_rbd.choices[0][0] if self.colegio_rbd.choices else ''

# -------------------------------------------------------------
# Formularios para "Colegios"
# -------------------------------------------------------------


class ColegioForm(FlaskForm):
    """
    Formulario para gestionar la creación y edición de colegios.
    """
    rbd = StringField('RBD', validators=[DataRequired(), Length(max=20)])
    nombre_colegio = StringField('Nombre del Colegio', validators=[
        DataRequired(), Length(max=100)])
    direccion = StringField('Dirección', validators=[
        DataRequired(), Length(max=255)])
    telefono = StringField('Teléfono', validators=[
        DataRequired(), Length(max=20)])
    director = StringField('Director', validators=[
        DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[
        DataRequired(), Length(max=100), Email()])
    tipo_ensenanza = SelectField('Tipo de Enseñanza', choices=[
        ('BASICA', 'Básica'), ('MEDIA', 'Media')], validators=[DataRequired()])
    latitud = FloatField('Latitud', validators=[DataRequired()])
    longitud = FloatField('Longitud', validators=[DataRequired()])
    submit = SubmitField('Guardar')


# -------------------------------------------------------------
# Formularios para "Alcaldia"
# -------------------------------------------------------------


class AlcaldiaForm(FlaskForm):
    nombre_alcalde = StringField('Nombre del Alcalde', validators=[
        DataRequired(), Length(max=100)])
    rut_cuerpo = StringField('Cuerpo del RUT', validators=[DataRequired()])
    rut_dv = StringField('Dígito Verificador', validators=[
        DataRequired(), Length(min=1, max=1)])
    email = StringField('Email', validators=[Length(max=100), Email()])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    fecha_inicio = DateField(
        'Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_termino = DateField('Fecha de Término', format='%Y-%m-%d')
    cargo = SelectField('Cargo', choices=[
        ('Alcalde', 'Alcalde'),
        ('Alcaldesa', 'Alcaldesa'),
        ('Alcalde(S)', 'Alcalde(S)'),
        ('Alcaldesa(S)', 'Alcaldesa(S)')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def validate_rut_cuerpo(self, field):
        print(">>> Entró a validate_rut_cuerpo()")  # Depuración
        rut_valido, mensaje = validar_rut(
            self.rut_cuerpo.data, self.rut_dv.data)
        if not rut_valido:
            raise ValidationError(mensaje)


# -------------------------------------------------------------
# Formularios para "Jefatura DAEM"
# -------------------------------------------------------------
class JefaturaDAEMForm(FlaskForm):
    nombre = StringField('Nombre de la Jefatura DAEM', validators=[
        DataRequired(), Length(max=100)])
    rut_cuerpo = StringField('Cuerpo del RUT', validators=[DataRequired()])
    rut_dv = StringField('Dígito Verificador', validators=[DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=100)])
    telefono = StringField('Teléfono', validators=[
        DataRequired(), Length(max=20)])
    cargo_jefatura = SelectField('Cargo', choices=[
        ('Jefe DAEM', 'Jefe DAEM'),
        ('Jefe(a) DAEM (S)', 'Jefe(a) DAEM (S)')
    ], validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_termino = DateField('Fecha de Término')
    submit = SubmitField('Guardar')

    # ✅ Validar el RUT usando validators.py
    def validate_rut_cuerpo(self, field):
        if not validar_rut(self.rut_cuerpo.data, self.rut_dv.data)[0]:
            raise ValidationError('El RUT ingresado es inválido.')


# -------------------------------------------------------------
# Formularios para "Financiamiento"
# -------------------------------------------------------------
class FinanciamientoForm(FlaskForm):
    nombre_financiamiento = StringField(
        'Nombre del Financiamiento', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class UsuarioForm(FlaskForm):
    nombre_usuario = StringField('Nombre de Usuario', validators=[
                                 DataRequired(), Length(min=4, max=50)])
    contraseña = PasswordField('Contraseña', validators=[
                               DataRequired(), Length(min=6)])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[
                                         DataRequired(), EqualTo('contraseña')])
    rol = SelectField('Rol', choices=[
                      ('Administrador', 'Administrador'), ('Usuario', 'Usuario')], validators=[DataRequired()])
    submit = SubmitField('Guardar')


class RolForm(FlaskForm):
    nombre_rol = StringField('Nombre del Rol', validators=[
                             DataRequired(), Length(max=50)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=200)])
    submit = SubmitField('Guardar')


# -------------------------------------------------------------
# Formularios para "Historial de Cambios"
# -------------------------------------------------------------
class HistorialCambiosForm(FlaskForm):
    tabla_afectada = StringField('Tabla Afectada', validators=[DataRequired()])
    registro_id = IntegerField('ID del Registro', validators=[DataRequired()])
    usuario_id = IntegerField('ID del Usuario', validators=[DataRequired()])
    tipo_cambio = StringField('Tipo de Cambio', validators=[DataRequired()])
    detalle_cambio = TextAreaField('Detalle del Cambio')
    submit = SubmitField('Guardar')


class TipoContratoForm(FlaskForm):
    nombre = StringField('Nombre del Contrato', validators=[DataRequired()])
    observacion = TextAreaField('Observación')
    submit = SubmitField('Guardar')


class DeleteForm(FlaskForm):
    submit = SubmitField('Eliminar')
