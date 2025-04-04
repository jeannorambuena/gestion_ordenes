# 📌 Importaciones de Flask y Extensiones
from app.forms import OrdenTrabajoForm
from app.models import OrdenesTrabajo, Funcionarios, Colegios, TipoContrato
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, jsonify
)
from app import db  # Base de datos
from sqlalchemy.exc import IntegrityError  # Manejo de errores de base de datos
from sqlalchemy.orm import joinedload  # Carga de relaciones
from sqlalchemy import text  # Ejecutar consultas SQL crudas
from datetime import datetime  # Manejo de fechas
from wtforms import ValidationError  # Manejo de errores de validación

# 📌 Importaciones de validadores y utilidades
from app.validators import validar_rut  # Validador de RUT
from app.busqueda_funcionario import buscar_funcionarios  # Búsqueda de funcionarios

# 📌 Importación de modelos agrupados
from app.models import (
    OrdenesTrabajo, Colegios, TipoContrato, Funcionarios, Financiamiento,
    Cargo, Alcaldia, JefaturaDAEM
)

# 📌 Importación de formularios agrupados
from app.forms import (
    OrdenTrabajoForm, FuncionarioForm, CargoForm, RolForm, ColegioForm,
    FinanciamientoForm, JefaturaDAEMForm, UsuarioForm, AlcaldiaForm,
    DeleteForm, TipoContratoForm
)

# Configuración del Blueprint
ordenes_bp = Blueprint('ordenes_bp', __name__, template_folder='templates')

# Crear el Blueprint primero
main_bp = Blueprint('main', __name__)

# app/routes.py

roles_bp = Blueprint('roles', __name__)  # Cambiado a 'roles'

# Listar roles


@roles_bp.route('/', methods=['GET'])
def listar_roles():
    roles = Rol.query.all()
    return render_template('roles/list.html', roles=roles)

# Crear un nuevo rol


@roles_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_rol():
    form = RolForm()
    if form.validate_on_submit():
        nuevo_rol = Rol(
            nombre_rol=form.nombre_rol.data,
            descripcion=form.descripcion.data
        )
        db.session.add(nuevo_rol)
        db.session.commit()
        flash('Rol creado con éxito', 'success')
        return redirect(url_for('roles.listar_roles'))  # Cambiado a 'roles'
    return render_template('roles/nuevo.html', form=form)

# Editar un rol


@roles_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_rol(id):
    rol = Rol.query.get_or_404(id)
    form = RolForm(obj=rol)
    if form.validate_on_submit():
        rol.nombre_rol = form.nombre_rol.data
        rol.descripcion = form.descripcion.data
        db.session.commit()
        flash('Rol actualizado con éxito', 'success')
        return redirect(url_for('roles.listar_roles'))  # Cambiado a 'roles'
    return render_template('roles/editar.html', form=form, rol=rol)

# Eliminar un rol


@roles_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_rol(id):
    rol = Rol.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()
    flash('Rol eliminado con éxito', 'success')
    return redirect(url_for('roles.listar_roles'))  # Cambiado a 'roles'


@main_bp.route('/')
def home():
    return render_template('index.html')

# Ruta para la sección de órdenes de trabajo


@main_bp.route('/ordenes')
def ordenes():
    return render_template('ordenes.html')

# Ruta para listar todos los funcionarios


# Crear el Blueprint para funcionarios
funcionarios_bp = Blueprint('funcionarios_bp', __name__)

# Ruta para listar todos los funcionarios


@funcionarios_bp.route('/')
def listar_funcionarios():
    funcionarios = Funcionarios.query.all()
    return render_template('funcionarios/list.html', funcionarios=funcionarios)

# Ruta para crear un nuevo funcionario


@funcionarios_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_funcionario():
    form = FuncionarioForm()
    form.id_cargo.choices = [(cargo.id, cargo.nombre_cargo)
                             for cargo in Cargo.query.all()]

    if form.validate_on_submit():
        nuevo_funcionario = Funcionarios(
            rut_cuerpo=form.rut_cuerpo.data,
            rut_dv=form.rut_dv.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            titulo=form.titulo.data,
            id_cargo=form.id_cargo.data
        )
        try:
            db.session.add(nuevo_funcionario)
            db.session.commit()
            flash('Funcionario agregado con éxito', 'success')
            return redirect(url_for('funcionarios_bp.listar_funcionarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al agregar el funcionario: {
                  str(e)}', 'danger')

    return render_template('funcionarios/nuevo.html', form=form)

# Ruta para editar un funcionario


@funcionarios_bp.route('/editar/<string:rut_cuerpo>/<string:rut_dv>', methods=['GET', 'POST'])
def editar_funcionario(rut_cuerpo, rut_dv):
    funcionario = Funcionarios.query.filter_by(
        rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first_or_404()
    form = FuncionarioForm(obj=funcionario)
    form.id_cargo.choices = [(cargo.id, cargo.nombre_cargo)
                             for cargo in Cargo.query.all()]

    if form.validate_on_submit():
        funcionario.nombre = form.nombre.data
        funcionario.apellido = form.apellido.data
        funcionario.direccion = form.direccion.data
        funcionario.telefono = form.telefono.data
        funcionario.titulo = form.titulo.data
        funcionario.id_cargo = form.id_cargo.data

        try:
            db.session.commit()
            flash('Funcionario actualizado con éxito', 'success')
            return redirect(url_for('funcionarios_bp.listar_funcionarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar el funcionario: {
                  str(e)}', 'danger')

    return render_template('funcionarios/editar.html', form=form, funcionario=funcionario)

# Ruta para eliminar un funcionario


@funcionarios_bp.route('/eliminar/<string:rut_cuerpo>/<string:rut_dv>', methods=['POST'])
def eliminar_funcionario(rut_cuerpo, rut_dv):
    print(f"Intentando eliminar funcionario con RUT: {rut_cuerpo}-{rut_dv}")
    funcionario = Funcionarios.query.filter_by(
        rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()
    if not funcionario:
        print("Funcionario no encontrado")
        flash("Funcionario no encontrado", "danger")
        return redirect(url_for('funcionarios_bp.listar_funcionarios'))

    try:
        db.session.delete(funcionario)
        db.session.commit()
        print("Funcionario eliminado")
        flash('Funcionario eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar funcionario: {e}")
        flash(f'Ocurrió un error al eliminar el funcionario: {
              str(e)}', 'danger')

    return redirect(url_for('funcionarios_bp.listar_funcionarios'))


# Crear el Blueprint para los cargos
cargo_bp = Blueprint('cargo', __name__, url_prefix='/cargos')

# Ruta para listar todos los cargos


@cargo_bp.route('/')
def listar_cargos():
    cargos = Cargo.query.all()
    return render_template('cargos/list.html', cargos=cargos)

# Ruta para crear un nuevo cargo


@cargo_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_cargo():
    form = CargoForm()  # Usar el formulario de cargo que crearemos
    if form.validate_on_submit():
        nuevo_cargo = Cargo(
            nombre_cargo=form.nombre_cargo.data,
            descripcion=form.descripcion.data
        )
        try:
            db.session.add(nuevo_cargo)
            db.session.commit()
            flash('Cargo creado con éxito', 'success')
            return redirect(url_for('cargo.listar_cargos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al crear el cargo: {str(e)}', 'danger')

    return render_template('cargos/nuevo.html', form=form)

# Ruta para editar un cargo existente


@cargo_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    # Cargar el formulario con los datos del cargo actual
    form = CargoForm(obj=cargo)
    if form.validate_on_submit():
        cargo.nombre_cargo = form.nombre_cargo.data
        cargo.descripcion = form.descripcion.data
        try:
            db.session.commit()
            flash('Cargo actualizado con éxito', 'success')
            return redirect(url_for('cargo.listar_cargos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar el cargo: {
                  str(e)}', 'danger')

    return render_template('cargos/editar.html', form=form, cargo=cargo)

# Ruta para eliminar un cargo


@cargo_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    try:
        db.session.delete(cargo)
        db.session.commit()
        flash('Cargo eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al eliminar el cargo: {str(e)}', 'danger')

    return redirect(url_for('cargo.listar_cargos'))


@main_bp.route('/test-db-connection')
def test_db_connection():
    try:
        result = db.session.execute(text('SELECT 1'))
        for row in result:
            print(row)
        return "Conexión a la base de datos exitosa."
    except Exception as e:
        return f"Error al conectar a la base de datos: {e}"


# Crear un nuevo Blueprint para gestionar la relación funcionarios-colegios
funcionarios_colegios_bp = Blueprint('funcionarios_colegios', __name__)

# Ruta para listar todas las asignaciones de horas


@funcionarios_colegios_bp.route('/funcionarios_colegios', methods=['GET'])
def list_funcionarios_colegios():
    asignaciones = FuncionarioColegios.query.all()
    return render_template('funcionarios_colegios/list.html', asignaciones=asignaciones)

# Ruta para crear una nueva asignación de horas


@funcionarios_colegios_bp.route('/funcionarios_colegios/nuevo', methods=['GET', 'POST'])
def nuevo_funcionario_colegio():
    form = FuncionarioColegiosForm()
    if form.validate_on_submit():
        nueva_asignacion = FuncionarioColegios(
            funcionario_id=form.funcionario_id.data,  # Corregido a funcionario_id
            colegio_rbd=form.colegio_rbd.data,
            horas_disponibles=form.horas_disponibles.data
        )
        try:
            db.session.add(nueva_asignacion)
            db.session.commit()
            flash('Asignación de horas creada con éxito', 'success')
            return redirect(url_for('funcionarios_colegios.list_funcionarios_colegios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al crear la asignación: {
                  str(e)}', 'danger')
    return render_template('funcionarios_colegios/nuevo.html', form=form)

# Ruta para editar una asignación de horas


@funcionarios_colegios_bp.route('/funcionarios_colegios/editar/<int:id>', methods=['GET', 'POST'])
def editar_funcionario_colegio(id):
    asignacion = FuncionarioColegios.query.get_or_404(id)
    form = FuncionarioColegiosForm(obj=asignacion)
    if form.validate_on_submit():
        asignacion.funcionario_id = form.funcionario_id.data  # Corregido a funcionario_id
        asignacion.colegio_rbd = form.colegio_rbd.data
        asignacion.horas_disponibles = form.horas_disponibles.data
        try:
            db.session.commit()
            flash('Asignación de horas actualizada con éxito', 'success')
            return redirect(url_for('funcionarios_colegios.list_funcionarios_colegios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar la asignación: {
                  str(e)}', 'danger')
    return render_template('funcionarios_colegios/editar.html', form=form, asignacion=asignacion)

# Ruta para eliminar una asignación de horas


@funcionarios_colegios_bp.route('/funcionarios_colegios/eliminar/<int:id>', methods=['POST'])
def eliminar_funcionario_colegio(id):
    asignacion = FuncionarioColegios.query.get_or_404(id)
    try:
        db.session.delete(asignacion)
        db.session.commit()
        flash('Asignación de horas eliminada con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al eliminar la asignación: {
              str(e)}', 'danger')
    return redirect(url_for('funcionarios_colegios.list_funcionarios_colegios'))


# Crear el Blueprint para los colegios
colegio_bp = Blueprint('colegio', __name__)

# Ruta para listar todos los colegios


@colegio_bp.route('/')
def listar_colegios():
    colegios = Colegios.query.all()
    print(colegios)  # Esto mostrará los objetos devueltos en la consola
    return render_template('colegios/list.html', colegios=colegios)

# Ruta para crear un nuevo colegio


@colegio_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_colegio():
    form = ColegioForm()  # Asegúrate de que el formulario esté configurado
    if form.validate_on_submit():
        nuevo_colegio = Colegios(
            rbd=form.rbd.data,
            nombre_colegio=form.nombre_colegio.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            director=form.director.data,
            email=form.email.data,
            tipo_ensenanza=form.tipo_ensenanza.data,
            latitud=form.latitud.data,
            longitud=form.longitud.data
        )
        try:
            db.session.add(nuevo_colegio)
            db.session.commit()
            flash('Colegio creado con éxito', 'success')
            return redirect(url_for('colegio.listar_colegios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al agregar el colegio: {
                  str(e)}', 'danger')

    return render_template('colegios/nuevo.html', form=form)

# Ruta para editar un colegio existente


@colegio_bp.route('/editar/<string:rbd>', methods=['GET', 'POST'])
def editar_colegio(rbd):
    colegio = Colegios.query.get_or_404(rbd)
    form = ColegioForm(obj=colegio)
    if form.validate_on_submit():
        colegio.nombre_colegio = form.nombre_colegio.data
        colegio.direccion = form.direccion.data
        colegio.telefono = form.telefono.data
        colegio.director = form.director.data
        colegio.email = form.email.data
        colegio.tipo_ensenanza = form.tipo_ensenanza.data
        colegio.latitud = form.latitud.data
        colegio.longitud = form.longitud.data
        try:
            db.session.commit()
            flash('Colegio actualizado con éxito', 'success')
            return redirect(url_for('colegio.listar_colegios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar el colegio: {
                  str(e)}', 'danger')

    return render_template('colegios/editar.html', form=form, colegio=colegio)

# Ruta para eliminar un colegio


@colegio_bp.route('/eliminar/<string:rbd>', methods=['POST'])
def eliminar_colegio(rbd):
    colegio = Colegios.query.get_or_404(rbd)
    try:
        db.session.delete(colegio)
        db.session.commit()
        flash('Colegio eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al eliminar el colegio: {str(e)}', 'danger')

    return redirect(url_for('colegio.listar_colegios'))


funcionarios_colegios_bp = Blueprint('funcionarios_colegios', __name__)

# Ruta para listar todas las asignaciones


@funcionarios_colegios_bp.route('/funcionarios_colegios', methods=['GET'])
def list_funcionarios_colegios():
    asignaciones = FuncionarioColegios.query.all()
    for asignacion in asignaciones:
        print(f"Funcionario: {asignacion.funcionario_relacion.nombre} {
              asignacion.funcionario_relacion.apellido}")
        print(f"Colegio: {asignacion.colegio.nombre_colegio}")
        print(f"Horas disponibles: {asignacion.horas_disponibles}")
    return render_template('funcionarios_colegios/list.html', asignaciones=asignaciones)


# Ruta para crear una nueva asignación


@funcionarios_colegios_bp.route('/funcionarios_colegios/nuevo', methods=['GET', 'POST'])
def nuevo_funcionario_colegio():
    form = FuncionarioColegiosForm()
    if form.validate_on_submit():
        nueva_asignacion = FuncionarioColegios(
            funcionario_id=form.rut_cuerpo.data.split(
                '-')[0],  # Extrae solo el `rut_cuerpo`
            colegio_rbd=form.colegio_rbd.data,
            horas_disponibles=form.horas_disponibles.data
        )
        try:
            db.session.add(nueva_asignacion)
            db.session.commit()
            flash('Asignación de horas creada con éxito', 'success')
            return redirect(url_for('funcionarios_colegios.list_funcionarios_colegios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al crear la asignación: {
                  str(e)}', 'danger')
    return render_template('funcionarios_colegios/nuevo.html', form=form)

# Ruta para editar una asignación


@funcionarios_colegios_bp.route('/funcionarios_colegios/editar/<int:id>', methods=['GET', 'POST'])
def editar_funcionario_colegio(id):
    """
    Ruta para editar una asignación de Funcionario a Colegio.
    """
    # Obtén la asignación o lanza un error 404 si no existe
    asignacion = FuncionarioColegios.query.get_or_404(id)

    # Inicializa el formulario con los datos actuales
    form = FuncionarioColegiosForm(
        # Funcionario actual
        current_funcionario=f"{asignacion.funcionario_id}",
        current_colegio=asignacion.colegio_rbd,  # Colegio actual
        obj=asignacion
    )

    # Si el formulario fue enviado y es válido
    if request.method == 'POST' and form.validate():
        try:
            # Actualiza los datos de la asignación
            asignacion.funcionario_id = form.rut_cuerpo.data  # Actualiza funcionario_id
            asignacion.colegio_rbd = form.colegio_rbd.data  # Actualiza colegio_rbd
            asignacion.horas_disponibles = form.horas_disponibles.data  # Actualiza horas

            # Guarda los cambios en la base de datos
            db.session.commit()
            flash('Asignación actualizada con éxito.', 'success')

            # Redirige al listado de asignaciones
            return redirect(url_for('funcionarios_colegios.list_funcionarios_colegios'))
        except Exception as e:
            # Maneja errores durante el guardado
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar la asignación: {
                  str(e)}', 'danger')

    # Renderiza el formulario de edición
    return render_template('funcionarios_colegios/editar.html', form=form, asignacion=asignacion)
# Ruta para eliminar una asignación


@funcionarios_colegios_bp.route('/funcionarios_colegios/eliminar/<int:id>', methods=['POST'])
def eliminar_funcionario_colegio(id):
    asignacion = FuncionarioColegios.query.get_or_404(id)
    try:
        db.session.delete(asignacion)
        db.session.commit()
        flash('Asignación eliminada con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la asignación: {str(e)}', 'danger')

    return redirect(url_for('funcionarios_colegios.list_funcionarios_colegios'))


# Crear el Blueprint
alcaldia_bp = Blueprint('alcaldia', __name__)


# Ruta para listar todos los registros de alcaldía
@alcaldia_bp.route('/')
def listar_alcaldia():
    alcaldias = Alcaldia.query.all()
    return render_template('alcaldia/list.html', alcaldias=alcaldias)

# Ruta para crear un nuevo registro de alcaldía


@alcaldia_bp.route('/nuevo', methods=['GET', 'POST'])
def nueva_alcaldia():
    form = AlcaldiaForm()

    # DEPURACIÓN: imprimir estado del formulario
    print("¿Formulario enviado y válido?", form.validate_on_submit())
    print("Errores en rut_cuerpo:", form.rut_cuerpo.errors)
    print("Errores en rut_dv:", form.rut_dv.errors)

    if form.validate_on_submit():
        nueva_alcaldia = Alcaldia(
            nombre_alcalde=form.nombre_alcalde.data,
            cedula_identidad=f"{form.rut_cuerpo.data}-{form.rut_dv.data}",
            email=form.email.data,
            telefono=form.telefono.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_termino=form.fecha_termino.data,
            cargo=form.cargo.data
        )

        try:
            db.session.add(nueva_alcaldia)
            db.session.commit()
            flash('Alcaldía agregada con éxito', 'success')
            return redirect(url_for('alcaldia.listar_alcaldia'))
        except Exception as e:
            db.session.rollback()
            print("ERROR EN BD:", e)
            flash(
                f'Ocurrió un error al agregar la alcaldía: {str(e)}', 'danger')

    return render_template('alcaldia/nuevo.html', form=form)
# Ruta para editar un registro existente de alcaldía


@alcaldia_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_alcaldia(id):  # Cambiado de 'editar_alcalde' a 'editar_alcaldia'
    # Obtener el registro de alcaldía o devolver 404 si no existe
    alcaldia = Alcaldia.query.get_or_404(id)

    # Inicializar el formulario con los datos de la alcaldía
    form = AlcaldiaForm(obj=alcaldia)

    # Validar si el formulario fue enviado y es válido
    if form.validate_on_submit():
        # Actualizar los campos de la alcaldía con los datos del formulario
        alcaldia.nombre_alcalde = form.nombre_alcalde.data
        alcaldia.cedula_identidad = form.cedula_identidad.data
        alcaldia.email = form.email.data
        alcaldia.telefono = form.telefono.data
        alcaldia.fecha_inicio = form.fecha_inicio.data
        alcaldia.fecha_termino = form.fecha_termino.data
        alcaldia.cargo = form.cargo.data  # Asegúrate de guardar el valor del cargo
        db.session.commit()

        try:
            # Intentar guardar los cambios en la base de datos
            db.session.commit()
            flash('Alcaldía actualizada con éxito', 'success')
            return redirect(url_for('alcaldia.listar_alcaldia'))
        except Exception as e:
            # Si ocurre un error, revertir la transacción
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar la alcaldía: {
                  str(e)}', 'danger')
    else:
        # Si el formulario no es válido, imprimir los errores para depuración
        print("Errores en el formulario:", form.errors)

    # Renderizar la plantilla para editar con el formulario y los datos de la alcaldía
    # Cambiado 'alcalde' a 'alcaldia'
    return render_template('alcaldia/editar.html', form=form, alcaldia=alcaldia)

# Ruta para eliminar un registro de alcaldía


@alcaldia_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_alcaldia(id):  # Cambiado de 'eliminar_alcalde' a 'eliminar_alcaldia'
    # Cambiado de 'alcalde' a 'alcaldia'
    alcaldia = Alcaldia.query.get_or_404(id)
    try:
        db.session.delete(alcaldia)  # Cambiado de 'alcalde' a 'alcaldia'
        db.session.commit()
        flash('Alcaldía eliminada con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al eliminar la alcaldía: {str(e)}', 'danger')

    return redirect(url_for('alcaldia.listar_alcaldia'))

# Crear el Blueprint para las jefaturas DAEM


jefatura_daem_bp = Blueprint('jefatura_daem', __name__)

# Ruta para listar todas las jefaturas DAEM


@jefatura_daem_bp.route('/')
def listar_jefatura_daem():
    jefaturas = JefaturaDAEM.query.all()
    return render_template('jefatura_daem/list.html', jefaturas=jefaturas)

# Ruta para crear una nueva jefatura DAEM


@jefatura_daem_bp.route('/nuevo', methods=['GET', 'POST'])
def nueva_jefatura_daem():
    form = JefaturaDAEMForm()
    if form.validate_on_submit():
        nueva_jefatura = JefaturaDAEM(
            nombre=form.nombre.data,
            rut_cuerpo=form.rut_cuerpo.data,
            rut_dv=form.rut_dv.data,
            email=form.email.data,
            telefono=form.telefono.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_termino=form.fecha_termino.data,
            cargo_jefatura=form.cargo_jefatura.data
        )
        try:
            db.session.add(nueva_jefatura)
            db.session.commit()
            flash('Jefatura DAEM creada con éxito', 'success')
            return redirect(url_for('jefatura_daem.listar_jefatura_daem'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al crear la Jefatura DAEM: {
                  str(e)}', 'danger')

    return render_template('jefatura_daem/nuevo.html', form=form)


# Ruta para editar una jefatura DAEM existente

@jefatura_daem_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_jefatura_daem(id):
    jefatura = JefaturaDAEM.query.get_or_404(id)
    form = JefaturaDAEMForm(obj=jefatura)

    if form.validate_on_submit():
        jefatura.nombre = form.nombre.data
        # Usamos rut_cuerpo en lugar de cedula_identidad
        jefatura.rut_cuerpo = form.rut_cuerpo.data
        jefatura.rut_dv = form.rut_dv.data  # También rut_dv en lugar de cedula_identidad
        jefatura.email = form.email.data
        jefatura.telefono = form.telefono.data
        jefatura.fecha_inicio = form.fecha_inicio.data
        jefatura.fecha_termino = form.fecha_termino.data
        jefatura.cargo_jefatura = form.cargo_jefatura.data

        try:
            db.session.commit()
            flash('Jefatura DAEM actualizada con éxito', 'success')
            return redirect(url_for('jefatura_daem.listar_jefatura_daem'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar la Jefatura DAEM: {
                  str(e)}', 'danger')

    return render_template('jefatura_daem/editar.html', form=form, jefatura=jefatura)


# Ruta para eliminar una jefatura DAEM


@jefatura_daem_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_jefatura_daem(id):
    jefatura = JefaturaDAEM.query.get_or_404(id)
    try:
        db.session.delete(jefatura)
        db.session.commit()
        flash('Jefatura DAEM eliminada con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al eliminar la Jefatura DAEM: {
              str(e)}', 'danger')
    return redirect(url_for('jefatura_daem.listar_jefatura_daem'))


# Ruta para listar los financiamientos

# Definir el Blueprint para financiamiento
financiamiento_bp = Blueprint('financiamiento', __name__)

# Ruta para listar financiamientos


@financiamiento_bp.route('/', methods=['GET'])
def listar_financiamientos():
    financiamientos = Financiamiento.query.all()  # Obtener todos los financiamientos
    return render_template('financiamiento/list.html', financiamientos=financiamientos)

# Ruta para agregar un nuevo financiamiento


@financiamiento_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_financiamiento():
    form = FinanciamientoForm()
    if form.validate_on_submit():
        nuevo_financiamiento = Financiamiento(
            nombre_financiamiento=form.nombre_financiamiento.data)
        try:
            db.session.add(nuevo_financiamiento)
            db.session.commit()
            flash('Financiamiento agregado correctamente', 'success')
            return redirect(url_for('financiamiento.listar_financiamientos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar el financiamiento: {str(e)}', 'danger')
    return render_template('financiamiento/nuevo.html', form=form)

# Ruta para editar un financiamiento existente


@financiamiento_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_financiamiento(id):
    financiamiento = Financiamiento.query.get_or_404(id)
    form = FinanciamientoForm(obj=financiamiento)
    if form.validate_on_submit():
        financiamiento.nombre_financiamiento = form.nombre_financiamiento.data
        try:
            db.session.commit()
            flash('Financiamiento actualizado correctamente', 'success')
            return redirect(url_for('financiamiento.listar_financiamientos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el financiamiento: {str(e)}', 'danger')
    return render_template('financiamiento/editar.html', form=form, financiamiento=financiamiento)

# Ruta para eliminar un financiamiento


@financiamiento_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_financiamiento(id):
    financiamiento = Financiamiento.query.get_or_404(id)
    try:
        db.session.delete(financiamiento)
        db.session.commit()
        flash('Financiamiento eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el financiamiento: {str(e)}', 'danger')
    return redirect(url_for('financiamiento.listar_financiamientos'))

# Ruta para listar usuarios


@main_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/list.html', usuarios=usuarios)

# Si tienes una segunda función con el mismo nombre de endpoint, cámbiala
# Verifica si hay rutas duplicadas


@main_bp.route('/usuarios/listar', methods=['GET'])
def listar_usuarios_extra():
    # Otra función que usa una ruta diferente, pero no debe usar el mismo endpoint
    usuarios = Usuario.query.all()
    return render_template('usuarios/list_extra.html', usuarios=usuarios)

# Crear un nuevo usuario


@main_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        nuevo_usuario = Usuario(
            nombre_usuario=form.nombre_usuario.data,
            contraseña=form.contraseña.data,  # Asegúrate de aplicar un hash a la contraseña
            rol=form.rol.data
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado con éxito', 'success')
        return redirect(url_for('main.listar_usuarios'))
    return render_template('usuarios/nuevo.html', form=form)

# Editar un usuario


@main_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nombre_usuario = form.nombre_usuario.data
        # Asegúrate de aplicar un hash a la contraseña
        usuario.contraseña = form.contraseña.data
        usuario.rol = form.rol.data
        db.session.commit()
        flash('Usuario actualizado con éxito', 'success')
        return redirect(url_for('main.listar_usuarios'))
    return render_template('usuarios/editar.html', form=form, usuario=usuario)

# Eliminar un usuario


@main_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado con éxito', 'success')
    return redirect(url_for('main.listar_usuarios'))


# Definir el Blueprint para historial de cambios
historial_bp = Blueprint('historial_bp', __name__)

# Rutas del historial de cambios


@historial_bp.route('/')
def listar_historial():
    cambios = HistorialCambios.query.all()
    return render_template('historial_cambios/list.html', cambios=cambios)


@historial_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_historial():
    form = HistorialCambiosForm()
    if form.validate_on_submit():
        nuevo_cambio = HistorialCambios(
            tabla_afectada=form.tabla_afectada.data,
            registro_id=form.registro_id.data,
            usuario_id=form.usuario_id.data,
            tipo_cambio=form.tipo_cambio.data,
            detalle_cambio=form.detalle_cambio.data
        )
        try:
            db.session.add(nuevo_cambio)
            db.session.commit()
            flash('Registro creado con éxito', 'success')
            # Asegúrate de usar historial_bp aquí
            return redirect(url_for('historial_bp.listar_historial'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el registro: {str(e)}', 'danger')
    return render_template('historial_cambios/nuevo.html', form=form)

# Crear el Blueprint para órdenes de trabajo


# Crear el Blueprint


ordenes_bp = Blueprint('ordenes_bp', __name__, template_folder='templates')

# ✅ Ruta corregida: Búsqueda de Funcionarios


@ordenes_bp.route('/buscar_funcionario', methods=['GET'])
def buscar_funcionario():
    query = request.args.get('q', '').strip()
    print(f"🔍 Buscando funcionarios con el término: {query}")

    if not query:
        return jsonify([])

    funcionarios = Funcionarios.query.filter(
        (Funcionarios.nombre.ilike(f"%{query}%")) |
        (Funcionarios.apellido.ilike(f"%{query}%")) |
        (Funcionarios.rut_cuerpo.ilike(f"%{query}%")) |
        (Funcionarios.rut_dv.ilike(f"%{query}%"))
    ).all()

    print(f"📊 Funcionario(s) encontrado(s): {funcionarios}")

    resultados = [{
        "rut": f"{f.rut_cuerpo}-{f.rut_dv}",
        "nombre": f.nombre,
        "apellido": f.apellido
    } for f in funcionarios]

    return jsonify(resultados)


# ✅ Ruta corregida: Validación de RUT
@ordenes_bp.route('/validar_rut_endpoint', methods=['POST'])
def validar_rut_endpoint():
    try:
        data = request.get_json()
        print(f"Datos recibidos en el endpoint: {data}")

        if not data:
            return jsonify({'valid': False, 'message': 'No se recibieron datos en formato JSON'}), 400

        rut_cuerpo = data.get('rut_cuerpo', '').strip()
        rut_dv = data.get('rut_dv', '').strip().upper()

        if not rut_cuerpo or not rut_dv:
            return jsonify({'valid': False, 'message': 'RUT incompleto'}), 400

        from app.validators import validar_rut
        is_valid, message = validar_rut(rut_cuerpo, rut_dv)

        if not is_valid:
            return jsonify({'valid': False, 'message': message}), 200

        funcionario = Funcionarios.query.filter_by(
            rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()
        if funcionario:
            return jsonify({
                'valid': True,
                'existe': True,
                'nombre': funcionario.nombre,
                'apellido': funcionario.apellido
            }), 200
        else:
            return jsonify({'valid': True, 'existe': False, 'message': 'Funcionario no encontrado'}), 200

    except Exception as e:
        return jsonify({'valid': False, 'message': 'Error interno del servidor'}), 500


# ✅ Validación de horas activas del funcionario con detalle completo


@ordenes_bp.route('/validar_horas_funcionario', methods=['GET'])
def validar_horas_funcionario():
    rut_cuerpo = request.args.get('rut_cuerpo', '').strip()
    rut_dv = request.args.get('rut_dv', '').strip()
    anio_actual = datetime.now().year

    if not rut_cuerpo or not rut_dv:
        return jsonify({'error': 'RUT no proporcionado'}), 400

    # 🔄 Cargar órdenes activas con joinedload para evitar múltiples queries
    ordenes_activas = OrdenesTrabajo.query.options(
        joinedload(OrdenesTrabajo.colegio),
        joinedload(OrdenesTrabajo.financiamiento),
        joinedload(OrdenesTrabajo.tipo_contrato)
    ).filter(
        OrdenesTrabajo.rut_cuerpo == rut_cuerpo,
        OrdenesTrabajo.rut_dv == rut_dv,
        (OrdenesTrabajo.fecha_termino >= datetime.today()) | (
            OrdenesTrabajo.fecha_termino == None)
    ).all()

    # Calcular horas totales y disponibles
    horas_totales = sum(orden.horas_disponibles for orden in ordenes_activas)
    horas_disponibles = max(44 - horas_totales, 0)

    # 📦 Preparar respuesta JSON con detalle de cada orden activa
    detalle_ordenes = [{
        "numero_orden": orden.numero_orden,
        "colegio": orden.colegio.nombre_colegio if orden.colegio else "N/A",
        "horas": orden.horas_disponibles,
        "financiamiento": orden.financiamiento.nombre_financiamiento if orden.financiamiento else "N/A",
        "fecha_inicio": orden.fecha_inicio.strftime('%Y-%m-%d'),
        "fecha_termino": orden.fecha_termino.strftime('%Y-%m-%d') if orden.fecha_termino else "Indefinido",
        "tipo_contrato": orden.tipo_contrato.nombre if orden.tipo_contrato else "N/A"
    } for orden in ordenes_activas]

    return jsonify({
        "horas_totales": horas_totales,
        "horas_disponibles": horas_disponibles,
        "ordenes_activas": detalle_ordenes
    })


# ✅ Listado de órdenes de trabajo
@ordenes_bp.route('/', methods=['GET'])
def listar_ordenes():
    ordenes = db.session.query(OrdenesTrabajo).options(
        joinedload(OrdenesTrabajo.tipo_contrato),
        joinedload(OrdenesTrabajo.funcionario),
        joinedload(OrdenesTrabajo.colegio)
    ).all()

    return render_template('ordenes_trabajo/list.html', ordenes=ordenes)


# ✅ Creación de nueva orden con validación de horas
@ordenes_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_orden():
    form = OrdenTrabajoForm()
    anio_actual = datetime.now().year

    # Obtener último número de orden del año actual
    ultimo_numero = db.session.query(db.func.max(OrdenesTrabajo.numero_orden))\
        .filter(OrdenesTrabajo.anio == anio_actual).scalar()

    nuevo_numero = 1 if ultimo_numero is None else int(ultimo_numero) + 1
    numero_orden_formateado = f"{nuevo_numero:03d}-{anio_actual}"

    if request.method == 'POST' and form.validate_on_submit():
        rut_cuerpo = form.rut_cuerpo.data
        rut_dv = form.rut_dv.data
        horas_solicitadas = form.horas_disponibles.data or 0

        # Verificar si supera las 44 horas permitidas
        ordenes_activas = OrdenesTrabajo.query.filter(
            OrdenesTrabajo.rut_cuerpo == rut_cuerpo,
            OrdenesTrabajo.rut_dv == rut_dv,
            (OrdenesTrabajo.fecha_termino >= datetime.today()) | (
                OrdenesTrabajo.fecha_termino == None)
        ).all()

        horas_actuales = sum(
            orden.horas_disponibles for orden in ordenes_activas)
        if horas_actuales + horas_solicitadas > 44:
            flash(
                f"❌ Error: No puede asignar más de 44 horas. Actualmente tiene {horas_actuales} horas.", "danger")
            return redirect(url_for('ordenes_bp.nueva_orden'))

        try:
            nueva_orden = OrdenesTrabajo(
                numero_orden=nuevo_numero,
                anio=anio_actual,
                rut_cuerpo=rut_cuerpo,
                rut_dv=rut_dv,
                fecha_inicio=form.fecha_inicio.data,
                fecha_termino=form.fecha_termino.data or None,
                es_indefinido=form.es_indefinido.data,
                observaciones=form.observaciones.data,
                horas_disponibles=horas_solicitadas,
                colegio_rbd=form.colegio_rbd.data,
                tipo_contrato_id=form.tipo_contrato.data,
                financiamiento_id=form.financiamiento.data
            )

            # ✅ Agregar campos que estaban faltando
            nueva_orden.alcalde_id = form.alcalde_id.data
            nueva_orden.jefatura_daem_id = form.jefatura_daem_id.data

            db.session.add(nueva_orden)
            db.session.commit()

            flash(
                f"✅ Orden de trabajo creada exitosamente: {numero_orden_formateado}", "success")
            return redirect(url_for('ordenes_bp.listar_ordenes'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al guardar la orden: {str(e)}", "danger")

    return render_template('ordenes_trabajo/nueva.html', form=form, numero_orden=numero_orden_formateado)


# ✅ Edición de orden de trabajo
@ordenes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_orden(id):
    orden = OrdenesTrabajo.query.get_or_404(id)
    form = OrdenTrabajoForm(obj=orden)

    form.colegio_rbd.choices = [(col.rbd, col.nombre_colegio)
                                for col in Colegios.query.all()]
    form.tipo_contrato.choices = [(tc.id, tc.nombre)
                                  for tc in TipoContrato.query.all()]

    if form.validate_on_submit():
        try:
            orden.colegio_rbd = form.colegio_rbd.data
            orden.tipo_contrato_id = form.tipo_contrato.data
            orden.fecha_inicio = form.fecha_inicio.data
            orden.fecha_termino = form.fecha_termino.data
            orden.es_indefinido = form.es_indefinido.data
            orden.observaciones = form.observaciones.data
            orden.horas_disponibles = form.horas_disponibles.data

            db.session.commit()
            flash("Orden actualizada exitosamente", "success")
            return redirect(url_for('ordenes_bp.listar_ordenes'))
        except IntegrityError:
            db.session.rollback()
            flash("Error al actualizar la orden.", "danger")

    return render_template('ordenes_trabajo/editar.html', form=form, orden=orden)


tipo_contrato_bp = Blueprint(
    'tipo_contrato', __name__, url_prefix='/tipo_contrato')

# Ruta para listar los tipos de contrato


@tipo_contrato_bp.route('/listar', methods=['GET'])
def listar_tipo_contrato():
    tipos_contrato = TipoContrato.query.all()
    # Asegurarse de que el formulario está instanciado correctamente
    delete_form = DeleteForm()
    return render_template('tipo_contrato/list.html', tipos_contrato=tipos_contrato, delete_form=delete_form)

# Ruta para crear un nuevo tipo de contrato


@tipo_contrato_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_tipo_contrato():
    # Inicializa el formulario de tipo de contrato
    form = TipoContratoForm()

    # Verifica si el formulario es válido y procesable
    if form.validate_on_submit():
        # Crea una nueva instancia del tipo de contrato
        nuevo_tipo = TipoContrato(
            nombre=form.nombre.data,
            observacion=form.observacion.data
        )
        try:
            # Intenta añadir y guardar en la base de datos
            db.session.add(nuevo_tipo)
            db.session.commit()
            flash('Tipo de contrato creado con éxito', 'success')
            return redirect(url_for('tipo_contrato.listar_tipo_contrato'))
        except Exception as e:
            # En caso de error, revierte la sesión y muestra mensaje de error
            db.session.rollback()
            flash(f'Error al crear el tipo de contrato: {str(e)}', 'danger')

    # Renderiza la plantilla para un nuevo tipo de contrato con el formulario
    return render_template('tipo_contrato/nuevo.html', form=form)


# Ruta para editar un tipo de contrato existente


@tipo_contrato_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tipo_contrato(id):
    # Obtiene el tipo de contrato o lanza un 404 si no existe
    tipo_contrato = TipoContrato.query.get_or_404(id)

    # Inicializa el formulario con los datos actuales del tipo de contrato
    form = TipoContratoForm(obj=tipo_contrato)

    # Validación y actualización de los datos
    if form.validate_on_submit():
        tipo_contrato.nombre = form.nombre.data
        tipo_contrato.observacion = form.observacion.data
        try:
            db.session.commit()  # Guarda los cambios en la base de datos
            flash('Tipo de contrato actualizado con éxito', 'success')
            return redirect(url_for('tipo_contrato.listar_tipo_contrato'))
        except Exception as e:
            db.session.rollback()  # En caso de error, revierte los cambios
            flash(f'Error al actualizar el tipo de contrato: {
                  str(e)}', 'danger')

    # Renderiza la plantilla de edición con el formulario y el tipo de contrato
    return render_template('tipo_contrato/editar.html', form=form, tipo_contrato=tipo_contrato)

# Ruta para eliminar un tipo de contrato


@tipo_contrato_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_tipo_contrato(id):
    # Obtiene el tipo de contrato o lanza un 404 si no existe
    tipo_contrato = TipoContrato.query.get_or_404(id)
    try:
        db.session.delete(tipo_contrato)  # Elimina el tipo de contrato
        db.session.commit()  # Confirma la eliminación en la base de datos
        flash('Tipo de contrato eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()  # Revertir en caso de error
        flash(f'Error al eliminar el tipo de contrato: {str(e)}', 'danger')
    return redirect(url_for('tipo_contrato.listar_tipo_contrato'))


@ordenes_bp.route('/buscar_funcionarios', methods=['POST'])
def buscar_funcionarios_endpoint():
    data = request.get_json()
    criterio = data.get('criterio', '').strip()

    if not criterio:
        return jsonify({'error': 'Criterio de búsqueda vacío'}), 400

    resultados = buscar_funcionarios(criterio, db.session)
    if resultados:
        return jsonify({'exito': True, 'resultados': resultados}), 200
    return jsonify({'exito': False, 'message': 'No se encontraron coincidencias'}), 404


@ordenes_bp.route('/verificar_horas_disponibles', methods=['GET'])
def verificar_horas_disponibles():
    rut_cuerpo = request.args.get('rut_cuerpo')
    rut_dv = request.args.get('rut_dv')

    if not rut_cuerpo or not rut_dv:
        return jsonify({'error': 'RUT inválido'}), 400

    # Obtener todas las órdenes activas del funcionario
    ordenes_activas = OrdenesTrabajo.query.filter(
        OrdenesTrabajo.rut_cuerpo == rut_cuerpo,
        OrdenesTrabajo.rut_dv == rut_dv,
        or_(
            # Si no tiene fecha de término, sigue activa
            OrdenesTrabajo.fecha_termino == None,
            # Si la fecha de término es futura
            OrdenesTrabajo.fecha_termino >= datetime.now().date()
        )
    ).all()

    total_horas = sum(orden.horas_disponibles for orden in ordenes_activas)

    # Construcción de la respuesta con las órdenes activas
    ordenes_info = [{
        'numero_orden': orden.numero_orden,
        'colegio': orden.colegio.nombre_colegio if orden.colegio else 'No asignado',
        'horas': orden.horas_disponibles,
        'financiamiento': orden.financiamiento.nombre_financiamiento if orden.financiamiento else 'No asignado',
        'fecha_inicio': orden.fecha_inicio.strftime('%d-%m-%Y'),
        'fecha_termino': orden.fecha_termino.strftime('%d-%m-%Y') if orden.fecha_termino else 'Indefinido'
    } for orden in ordenes_activas]

    return jsonify({
        'total_horas': total_horas,
        'ordenes_activas': ordenes_info
    })
