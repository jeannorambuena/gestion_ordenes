# 📌 Extensiones Flask y base de datos
from flask_wtf import FlaskForm
from app.extensions.extensions import db

# 📌 Validadores y campos de WTForms
from wtforms import (
    StringField, IntegerField, DateField, BooleanField, SelectField,
    SelectMultipleField, TextAreaField, FloatField, PasswordField, SubmitField
)
from wtforms.validators import (
    DataRequired, Optional, NumberRange, ValidationError, Length,
    Email, EqualTo
)

# 📌 Validadores personalizados
from app.utils.validators import validar_rut

# 📌 Modelos del sistema
from app.models import (
    Funcionarios, TipoContrato, Colegios,
    Financiamiento, Alcaldia, JefaturaDAEM, Cargo
)

# -------------------------------------------------------------
# Formularios para "Ordenes de Trabajo"
# -------------------------------------------------------------


class OrdenTrabajoForm(FlaskForm):
    rut_cuerpo = StringField('RUT Cuerpo', validators=[DataRequired()])
    rut_dv = StringField('Dígito Verificador', validators=[
        DataRequired(), Length(min=1, max=1)])
    anio = IntegerField('Año', validators=[
        DataRequired(), NumberRange(min=2000, max=2100)])

    colegio_rbd = SelectField('Colegio', coerce=str,
                              choices=[], validators=[DataRequired()])
    tipo_contrato = SelectField(
        'Tipo de Contrato', coerce=int, choices=[], validators=[DataRequired()])
    financiamiento = SelectField(
        'Financiamiento', coerce=int, choices=[], validators=[DataRequired()])
    fecha_inicio = DateField(
        'Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_termino = DateField(
        'Fecha de Término', format='%Y-%m-%d', validators=[Optional()])
    horas_disponibles = IntegerField('Horas Disponibles', validators=[
        DataRequired(), NumberRange(min=1, max=44)])
    alcalde_id = SelectField('Alcalde o Alcaldesa',
                             coerce=int, validators=[DataRequired()])
    jefatura_daem_id = SelectField(
        'Jefe(a) DAEM', coerce=int, validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[
        Optional(), Length(max=500)])
    es_indefinido = BooleanField('Es Indefinido', default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Colegio
        self.colegio_rbd.choices = [(col.rbd, col.nombre_colegio)
                                    for col in Colegios.query.all()]
        if not self.colegio_rbd.choices:
            self.colegio_rbd.choices = [('', 'No hay colegios disponibles')]

        # Tipo de contrato
        self.tipo_contrato.choices = [(tc.id, tc.nombre)
                                      for tc in TipoContrato.query.all()]
        if not self.tipo_contrato.choices:
            self.tipo_contrato.choices = [
                ('', 'No hay tipos de contrato disponibles')]

        # Financiamiento
        self.financiamiento.choices = [
            (f.id, f.nombre_financiamiento) for f in Financiamiento.query.all()]
        if not self.financiamiento.choices:
            self.financiamiento.choices = [
                ('', 'No hay financiamientos disponibles')]

        # Alcalde activo
        alcaldes = Alcaldia.query.order_by(Alcaldia.fecha_inicio.desc()).all()
        self.alcalde_id.choices = [
            (a.id, f"{a.funcionario.nombre} {a.funcionario.apellido} ({a.cargo.nombre_cargo})")
            for a in alcaldes if a.funcionario and a.cargo
        ]
        actual_alcalde = next((a for a in alcaldes if a.es_activo), None)
        if actual_alcalde:
            self.alcalde_id.data = actual_alcalde.id

        # Jefatura DAEM activa
        jefaturas = JefaturaDAEM.query.order_by(
            JefaturaDAEM.fecha_inicio.desc()).all()
        self.jefatura_daem_id.choices = [
            (j.id, f"{j.funcionario.nombre} {j.funcionario.apellido} ({j.cargo.nombre_cargo})")
            for j in jefaturas if j.funcionario and j.cargo
        ]
        actual_jefatura = next((j for j in jefaturas if j.es_activo), None)
        if actual_jefatura:
            self.jefatura_daem_id.data = actual_jefatura.id

    def validate_horas_disponibles(self, field):
        if field.data < 1 or field.data > 44:
            raise ValidationError(
                "Las horas disponibles deben estar entre 1 y 44.")

    def validate_rut_cuerpo(self, field):
        if not validar_rut(self.rut_cuerpo.data, self.rut_dv.data):
            raise ValidationError("El RUT ingresado es inválido.")

# -------------------------------------------------------------
# Formularios para "Funcionarios"
# -------------------------------------------------------------


class FuncionarioForm(FlaskForm):
    rut_cuerpo = StringField('Cuerpo del RUT', validators=[
        DataRequired(), Length(min=7, max=8)])
    rut_dv = StringField('Dígito Verificador', validators=[
        DataRequired(), Length(min=1, max=1)])
    nombre = StringField('Nombre', validators=[
                         DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[
                           DataRequired(), Length(max=100)])
    direccion = StringField('Dirección', validators=[Length(max=255)])
    telefono = StringField('Teléfono', validators=[
                           DataRequired(), Length(min=9, max=9)])
    titulo = StringField('Título', validators=[Length(max=100)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(max=100)])
    id_cargo = SelectField('Cargo', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)
        self.id_cargo.choices = [(c.id, c.nombre_cargo) for c in Cargo.query.order_by(
            Cargo.nombre_cargo.asc()).all()]
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
        super().__init__(*args, **kwargs)
        funcionarios = Funcionarios.query.all()
        colegios = Colegios.query.all()
        self.rut_cuerpo.choices = [
            (f.rut_cuerpo, f"{f.nombre} {f.apellido}") for f in funcionarios]
        self.colegio_rbd.choices = [
            (c.rbd, c.nombre_colegio) for c in colegios]
        if current_funcionario:
            self.rut_cuerpo.data = current_funcionario
        if current_colegio:
            self.colegio_rbd.data = current_colegio


class ColegioForm(FlaskForm):
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
    tipo_ensenanza = SelectField('Tipo de Enseñanza', choices=[(
        'BASICA', 'Básica'), ('MEDIA', 'Media')], validators=[DataRequired()])
    latitud = FloatField('Latitud', validators=[DataRequired()])
    longitud = FloatField('Longitud', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class AlcaldiaForm(FlaskForm):
    rut_alcalde = StringField('RUT del Alcalde', validators=[
        DataRequired()], render_kw={"readonly": True})
    nombre_alcalde = StringField('Nombre del Alcalde', validators=[
        DataRequired()], render_kw={"readonly": True})
    id_cargo = SelectField('Cargo', coerce=int, validators=[DataRequired()])
    fecha_inicio = DateField(
        'Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_termino = DateField(
        'Fecha de Término', format='%Y-%m-%d', validators=[Optional()])

    # Nuevos campos agregados
    es_activo = BooleanField('¿Está en funciones actualmente?', default=True)
    es_titular = BooleanField('¿Es el alcalde titular?', default=False)

    submit = SubmitField('Asignar Alcaldía')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_cargo.choices = [(c.id, c.nombre_cargo) for c in Cargo.query.order_by(
            Cargo.nombre_cargo.asc()).all()]
        if not self.id_cargo.choices:
            self.id_cargo.choices = [('', 'No hay cargos disponibles')]


class JefaturaDAEMForm(FlaskForm):
    rut_funcionario = StringField(
        'RUT del Funcionario',
        validators=[
            DataRequired(),
            Length(min=9, max=10,
                   message="Debe ingresar el RUT completo, ej: 12345678-9")
        ]
    )

    id_cargo = SelectField('Cargo Asociado', coerce=int,
                           validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_termino = DateField('Fecha de Término')

    es_titular = BooleanField('¿Es el jefe DAEM titular?', default=False)
    es_activo = BooleanField('¿Está actualmente en funciones?', default=True)

    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_cargo.choices = [
            (c.id, c.nombre_cargo)
            for c in Cargo.query.order_by(Cargo.nombre_cargo.asc()).all()
        ]
        if not self.id_cargo.choices:
            self.id_cargo.choices = [('', 'No hay cargos disponibles')]

    def validate_rut_funcionario(self, field):
        if '-' not in field.data:
            raise ValidationError(
                'Debe ingresar el RUT con guion medio (ej: 12345678-9)')

        rut_cuerpo, rut_dv = field.data.strip().split('-')
        es_valido, mensaje = validar_rut(rut_cuerpo, rut_dv)

        if not es_valido:
            raise ValidationError(mensaje)


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


class UsuarioPermisosForm(FlaskForm):
    permisos = SelectMultipleField(
        'Permisos', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar Permisos')


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
