# 📌 Importaciones de Flask y Extensiones
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, jsonify, abort, make_response
)
from flask_login import login_user, login_required, logout_user, current_user
from weasyprint import HTML

# 📌 Herramientas de base de datos y SQLAlchemy
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import text

# 📌 Manejo de fechas y validaciones
from datetime import datetime
from wtforms import ValidationError

# 📌 Validadores y funciones auxiliares
from app.validators import validar_rut
from app.busqueda_funcionario import buscar_funcionarios

# 📌 Modelos
from app.models import (
    OrdenesTrabajo, Colegios, TipoContrato, Funcionarios,
    Financiamiento, Cargo, Alcaldia, JefaturaDAEM, Usuario, Rol, Permiso
)

# 📌 Formularios
from app.forms import (
    OrdenTrabajoForm, FuncionarioForm, CargoForm, RolForm,
    ColegioForm, FinanciamientoForm, JefaturaDAEMForm,
    UsuarioForm, AlcaldiaForm, DeleteForm, TipoContratoForm
)

# 📌 Decorador de roles
from app.utils.roles_required import roles_required

# 📌 Blueprints principales
main_bp = Blueprint('main', __name__)
cargo_bp = Blueprint('cargo', __name__)
colegio_bp = Blueprint('colegio', __name__)
funcionarios_bp = Blueprint('funcionarios_bp', __name__)
alcaldia_bp = Blueprint('alcaldia', __name__)
jefatura_daem_bp = Blueprint('jefatura_daem', __name__)
financiamiento_bp = Blueprint('financiamiento', __name__)
roles_bp = Blueprint('roles', __name__)
historial_bp = Blueprint('historial_bp', __name__)
ordenes_bp = Blueprint('ordenes_bp', __name__)
tipo_contrato_bp = Blueprint('tipo_contrato_bp', __name__)
usuarios_bp = Blueprint('usuarios_bp', __name__)

# Rutas principales


@main_bp.route('/')
@login_required
def home():
    return render_template('index.html')


@main_bp.route('/validar_rut', methods=['POST'])
def validar_rut_endpoint():
    data = request.get_json()
    rut_cuerpo = data.get("rut_cuerpo", "").strip()
    rut_dv = data.get("rut_dv", "").strip().upper()

    # Validar estructura del RUT usando tu función ya existente
    es_valido, mensaje = validar_rut(rut_cuerpo, rut_dv)
    if not es_valido:
        return jsonify({"valid": False, "message": mensaje}), 200

    # Buscar funcionario por RUT
    funcionario = Funcionarios.query.filter_by(
        rut_cuerpo=rut_cuerpo,
        rut_dv=rut_dv
    ).first()

    if funcionario:
        return jsonify({
            "valid": True,
            "existe": True,
            "nombre": funcionario.nombre,
            "apellido": funcionario.apellido,
            "telefono": funcionario.telefono,
            "email": getattr(funcionario, "email", "")  # si lo tienes
        }), 200
    else:
        return jsonify({
            "valid": True,
            "existe": False
        }), 200


# ===================== RUTAS PARA USUARIOS =====================


@usuarios_bp.route('/')
@login_required
@roles_required('administrador')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/list.html', usuarios=usuarios)


@usuarios_bp.route('/permisos/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def gestionar_permisos(id):
    usuario = Usuario.query.get_or_404(id)
    todos_los_permisos = Permiso.query.all()
    permisos_usuario = {p.id for p in usuario.permisos}

    if request.method == 'POST':
        permisos_seleccionados = request.form.getlist('permisos')
        usuario.permisos = Permiso.query.filter(
            Permiso.id.in_(permisos_seleccionados)).all()
        db.session.commit()
        flash('Permisos actualizados correctamente.', 'success')
        return redirect(url_for('usuarios_bp.listar_usuarios'))

    return render_template('usuarios/permisos.html', usuario=usuario, todos_los_permisos=todos_los_permisos, permisos_usuario=permisos_usuario)


@usuarios_bp.route('/usuarios/permisos/<int:id>', methods=['GET', 'POST'])
def asignar_permisos(id):
    usuario = Usuario.query.get_or_404(id)
    todos_permisos = Permiso.query.all()

    if request.method == 'POST':
        # Recibir permisos seleccionados desde el formulario
        seleccionados = request.form.getlist('permisos')

        # Limpiar los permisos actuales
        usuario.permisos.clear()

        # Asignar los nuevos
        for permiso_id in seleccionados:
            permiso = Permiso.query.get(int(permiso_id))
            if permiso:
                usuario.permisos.append(permiso)

        db.session.commit()
        flash('Permisos actualizados correctamente.', 'success')
        return redirect(url_for('usuarios_bp.listar_usuarios'))

    return render_template('usuarios/asignar_permisos.html', usuario=usuario, todos_permisos=todos_permisos)


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(
            nombre_usuario=form.nombre_usuario.data).first()
        if usuario_existente:
            flash('El nombre de usuario ya existe.', 'warning')
            return redirect(url_for('usuarios_bp.nuevo_usuario'))
        nuevo_usuario = Usuario(nombre_usuario=form.nombre_usuario.data)
        nuevo_usuario.set_password(form.contraseña.data)
        # Asignación de rol directamente desde el formulario
        nuevo_usuario.rol = form.rol.data
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('usuarios_bp.listar_usuarios'))
    return render_template('usuarios/nuevo.html', form=form)


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nombre_usuario = form.nombre_usuario.data
        usuario.rol = form.rol.data
        if form.contrasena.data:
            usuario.set_password(form.contrasena.data)
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('usuarios_bp.listar_usuarios'))
    return render_template('usuarios/editar.html', form=form, usuario=usuario)


@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('usuarios_bp.listar_usuarios'))


# ===================== RUTAS PARA ROLES =====================

@roles_bp.route('/', methods=['GET'])
@login_required
@roles_required('administrador')
def listar_roles():
    roles = Rol.query.all()
    return render_template('roles/list.html', roles=roles)


@roles_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
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
        return redirect(url_for('roles.listar_roles'))
    return render_template('roles/nuevo.html', form=form)


@roles_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_rol(id):
    rol = Rol.query.get_or_404(id)
    form = RolForm(obj=rol)
    if form.validate_on_submit():
        rol.nombre_rol = form.nombre_rol.data
        rol.descripcion = form.descripcion.data
        db.session.commit()
        flash('Rol actualizado con éxito', 'success')
        return redirect(url_for('roles.listar_roles'))
    return render_template('roles/editar.html', form=form, rol=rol)


@roles_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_rol(id):
    rol = Rol.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()
    flash('Rol eliminado con éxito', 'success')
    return redirect(url_for('roles.listar_roles'))

# ===================== RUTAS PARA FUNCIONARIOS =====================


@funcionarios_bp.route('/')
@login_required
@roles_required('administrador')
def listar_funcionarios():
    funcionarios = Funcionarios.query.all()
    return render_template('funcionarios/list.html', funcionarios=funcionarios)


@funcionarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_funcionario():
    # Capturar RUT desde la URL si viene como parámetro GET
    rut_param = request.args.get('rut')
    print(f"🔎 RUT recibido por URL: {rut_param}")
    rut_cuerpo = rut_dv = None

    if rut_param and '-' in rut_param:
        rut_cuerpo, rut_dv = rut_param.split('-')

    # Inicializar el formulario, con valores si vienen desde la URL
    if rut_cuerpo and rut_dv:
        form = FuncionarioForm(
            data={'rut_cuerpo': rut_cuerpo, 'rut_dv': rut_dv})
        form.rut_cuerpo.render_kw = {'readonly': True}
        form.rut_dv.render_kw = {'readonly': True}
    else:
        form = FuncionarioForm()

    # Cargar opciones de cargo
    form.id_cargo.choices = [(cargo.id, cargo.nombre_cargo)
                             for cargo in Cargo.query.all()]

    # Refrescar valores manualmente si no se reflejan en los campos readonly
    if rut_cuerpo and rut_dv and not form.rut_cuerpo.data:
        form.rut_cuerpo.data = rut_cuerpo
        form.rut_dv.data = rut_dv

    # Procesar envío del formulario
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
            flash(
                f'Ocurrió un error al agregar el funcionario: {str(e)}', 'danger')

    return render_template('funcionarios/nuevo.html', form=form)


@funcionarios_bp.route('/editar/<string:rut_cuerpo>/<string:rut_dv>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
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
            flash(
                f'Ocurrió un error al actualizar el funcionario: {str(e)}', 'danger')

    return render_template('funcionarios/editar.html', form=form, funcionario=funcionario)


@funcionarios_bp.route('/eliminar/<string:rut_cuerpo>/<string:rut_dv>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_funcionario(rut_cuerpo, rut_dv):
    funcionario = Funcionarios.query.filter_by(
        rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()
    if not funcionario:
        flash("Funcionario no encontrado", "danger")
        return redirect(url_for('funcionarios_bp.listar_funcionarios'))

    try:
        db.session.delete(funcionario)
        db.session.commit()
        flash('Funcionario eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(
            f'Ocurrió un error al eliminar el funcionario: {str(e)}', 'danger')

    return redirect(url_for('funcionarios_bp.listar_funcionarios'))


@funcionarios_bp.route('/detalle/<rut>')
@login_required
def detalle_funcionario(rut):
    try:
        rut_cuerpo, rut_dv = rut.split("-")
        funcionario = Funcionarios.query.filter_by(
            rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()

        if not funcionario:
            return jsonify({"error": "Funcionario no encontrado"}), 404

        return jsonify({
            "email": funcionario.email,
            "telefono": funcionario.telefono,
            "cargo": funcionario.cargo.nombre_cargo if funcionario.cargo else "Sin cargo"
        })

    except Exception as e:
        return jsonify({"error": f"Error al procesar RUT: {str(e)}"}), 500


# ===================== RUTAS PARA CARGOS =====================

@cargo_bp.route('/')
@login_required
@roles_required('administrador')
def listar_cargos():
    cargos = Cargo.query.all()
    return render_template('cargos/list.html', cargos=cargos)


@cargo_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_cargo():
    form = CargoForm()
    if form.validate_on_submit():
        nuevo_cargo = Cargo(
            nombre_cargo=form.nombre_cargo.data,
            descripcion=form.descripcion.data
        )
        db.session.add(nuevo_cargo)
        db.session.commit()
        flash('Cargo creado con éxito', 'success')
        return redirect(url_for('cargo.listar_cargos'))
    return render_template('cargos/nuevo.html', form=form)


@cargo_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    form = CargoForm(obj=cargo)
    if form.validate_on_submit():
        cargo.nombre_cargo = form.nombre_cargo.data
        cargo.descripcion = form.descripcion.data
        db.session.commit()
        flash('Cargo actualizado con éxito', 'success')
        return redirect(url_for('cargo.listar_cargos'))
    return render_template('cargos/editar.html', form=form, cargo=cargo)


@cargo_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    db.session.delete(cargo)
    db.session.commit()
    flash('Cargo eliminado con éxito', 'success')
    return redirect(url_for('cargo.listar_cargos'))


# ===================== RUTAS PARA COLEGIOS =====================

@colegio_bp.route('/')
@login_required
@roles_required('administrador')
def listar_colegios():
    colegios = Colegios.query.all()
    return render_template('colegios/list.html', colegios=colegios)


@colegio_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_colegio():
    form = ColegioForm()
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
        db.session.add(nuevo_colegio)
        db.session.commit()
        flash('Colegio creado con éxito', 'success')
        return redirect(url_for('colegio.listar_colegios'))
    return render_template('colegios/nuevo.html', form=form)


@colegio_bp.route('/editar/<string:rbd>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
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

        db.session.commit()
        flash('Colegio actualizado con éxito', 'success')
        return redirect(url_for('colegio.listar_colegios'))
    return render_template('colegios/editar.html', form=form, colegio=colegio)


@colegio_bp.route('/eliminar/<string:rbd>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_colegio(rbd):
    colegio = Colegios.query.get_or_404(rbd)
    db.session.delete(colegio)
    db.session.commit()
    flash('Colegio eliminado con éxito', 'success')
    return redirect(url_for('colegio.listar_colegios'))


# ===================== RUTAS PARA FINANCIAMIENTO =====================

@financiamiento_bp.route('/')
@login_required
@roles_required('administrador')
def listar_financiamientos():
    financiamientos = Financiamiento.query.all()
    return render_template('financiamiento/list.html', financiamientos=financiamientos)


@financiamiento_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_financiamiento():
    form = FinanciamientoForm()
    if form.validate_on_submit():
        nuevo_financiamiento = Financiamiento(
            nombre_financiamiento=form.nombre_financiamiento.data
        )
        db.session.add(nuevo_financiamiento)
        db.session.commit()
        flash('Financiamiento creado con éxito', 'success')
        return redirect(url_for('financiamiento.listar_financiamientos'))
    return render_template('financiamiento/nuevo.html', form=form)


@financiamiento_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_financiamiento(id):
    financiamiento = Financiamiento.query.get_or_404(id)
    form = FinanciamientoForm(obj=financiamiento)
    if form.validate_on_submit():
        financiamiento.nombre_financiamiento = form.nombre_financiamiento.data
        db.session.commit()
        flash('Financiamiento actualizado con éxito', 'success')
        return redirect(url_for('financiamiento.listar_financiamientos'))
    return render_template('financiamiento/editar.html', form=form, financiamiento=financiamiento)


@financiamiento_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_financiamiento(id):
    financiamiento = Financiamiento.query.get_or_404(id)
    db.session.delete(financiamiento)
    db.session.commit()
    flash('Financiamiento eliminado con éxito', 'success')
    return redirect(url_for('financiamiento.listar_financiamientos'))


# ===================== RUTAS PARA ORDENES DE TRABAJO =====================

@ordenes_bp.route('/')
@login_required
@roles_required('administrador')
def listar_ordenes():
    ordenes = OrdenesTrabajo.query.options(
        joinedload(OrdenesTrabajo.funcionario),
        joinedload(OrdenesTrabajo.colegio),
        joinedload(OrdenesTrabajo.tipo_contrato),
        joinedload(OrdenesTrabajo.financiamiento),
        joinedload(OrdenesTrabajo.alcalde),
        joinedload(OrdenesTrabajo.jefatura_daem)
    ).all()
    return render_template('ordenes_trabajo/list.html', ordenes=ordenes)


@ordenes_bp.route('/imprimir/<int:id>')
@login_required
@roles_required('administrador')
def imprimir_orden(id):
    orden = OrdenesTrabajo.query.get_or_404(id)
    fecha_actual = datetime.now()
    return render_template('ordenes_trabajo/pdf.html', orden=orden, fecha_actual=fecha_actual)


@ordenes_bp.route('/generar_pdf/<int:id>')
@login_required
@roles_required('administrador')
def generar_pdf_orden(id):
    orden = OrdenesTrabajo.query.get_or_404(id)
    fecha_actual = datetime.now()
    html = render_template('ordenes_trabajo/pdf.html',
                           orden=orden, fecha_actual=fecha_actual)
    pdf = HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=orden_{orden.numero_orden}.pdf'
    return response


@ordenes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_orden():
    form = OrdenTrabajoForm()

    # Cargar opciones de selección
    form.colegio_rbd.choices = [(c.rbd, c.nombre_colegio)
                                for c in Colegios.query.all()]
    form.tipo_contrato.choices = [(t.id, t.nombre)
                                  for t in TipoContrato.query.all()]
    form.financiamiento.choices = [
        (f.id, f.nombre_financiamiento) for f in Financiamiento.query.all()]
    form.alcalde_id.choices = [
        (a.id, f'{a.funcionario.nombre} {a.funcionario.apellido} ({a.cargo})')
        for a in Alcaldia.query.all() if a.funcionario is not None
    ]
    form.jefatura_daem_id.choices = [
        (j.id, f'{j.nombre} ({j.cargo_jefatura})')
        for j in JefaturaDAEM.query.all() if j.nombre and j.cargo_jefatura
    ]

    # Calcular número de orden siguiente
    ultimo = OrdenesTrabajo.query.order_by(OrdenesTrabajo.id.desc()).first()
    numero_orden = int(ultimo.numero_orden) + 1 if ultimo else 1

    # Procesar formulario
    if form.validate_on_submit():
        nueva_orden = OrdenesTrabajo(
            numero_orden=numero_orden,  # ← usa el número calculado
            anio=form.anio.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_termino=form.fecha_termino.data,
            es_indefinido=form.es_indefinido.data,
            observaciones=form.observaciones.data,
            horas_disponibles=form.horas_disponibles.data,
            colegio_rbd=form.colegio_rbd.data,
            tipo_contrato_id=form.tipo_contrato_id.data,
            financiamiento_id=form.financiamiento_id.data,
            rut_cuerpo=form.rut_cuerpo.data,
            rut_dv=form.rut_dv.data,
            alcalde_id=form.alcalde_id.data,
            jefatura_daem_id=form.jefatura_daem_id.data
        )
        db.session.add(nueva_orden)
        db.session.commit()
        flash('Orden de trabajo creada con éxito', 'success')
        return redirect(url_for('ordenes_bp.listar_ordenes'))

    # Renderizar formulario con número de orden prellenado
    return render_template('ordenes_trabajo/nueva.html', form=form, numero_orden=numero_orden)


@ordenes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_orden(id):
    orden = OrdenesTrabajo.query.get_or_404(id)
    form = OrdenTrabajoForm(obj=orden)

    form.colegio_rbd.choices = [(c.rbd, c.nombre_colegio)
                                for c in Colegios.query.all()]
    form.tipo_contrato.choices = [(t.id, t.nombre)
                                  for t in TipoContrato.query.all()]
    form.financiamiento.choices = [
        (f.id, f.nombre_financiamiento) for f in Financiamiento.query.all()]
    form.alcalde_id.choices = [
        (a.id, f'{a.nombre_alcalde} ({a.cargo})') for a in Alcaldia.query.all()]
    form.jefatura_daem_id.choices = [
        (j.id, f'{j.nombre} ({j.cargo_jefatura})') for j in JefaturaDAEM.query.all()]

    if form.validate_on_submit():
        orden.numero_orden = form.numero_orden.data
        orden.anio = form.anio.data
        orden.fecha_inicio = form.fecha_inicio.data
        orden.fecha_termino = form.fecha_termino.data
        orden.es_indefinido = form.es_indefinido.data
        orden.observaciones = form.observaciones.data
        orden.horas_disponibles = form.horas_disponibles.data
        orden.colegio_rbd = form.colegio_rbd.data
        orden.tipo_contrato_id = form.tipo_contrato_id.data
        orden.financiamiento_id = form.financiamiento_id.data
        orden.rut_cuerpo = form.rut_cuerpo.data
        orden.rut_dv = form.rut_dv.data
        orden.alcalde_id = form.alcalde_id.data
        orden.jefatura_daem_id = form.jefatura_daem_id.data

        db.session.commit()
        flash('Orden de trabajo actualizada con éxito', 'success')
        return redirect(url_for('ordenes_bp.listar_ordenes'))

    return render_template('ordenes_trabajo/editar.html', form=form, orden=orden)


@ordenes_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_orden(id):
    orden = OrdenesTrabajo.query.get_or_404(id)
    db.session.delete(orden)
    db.session.commit()
    flash('Orden de trabajo eliminada con éxito', 'success')
    return redirect(url_for('ordenes_bp.listar_ordenes'))

# ===================== RUTAS PARA JEFATURA DAEM =====================


@jefatura_daem_bp.route('/')
@login_required
@roles_required('administrador')
def listar_jefaturas_daem():
    jefaturas = JefaturaDAEM.query.all()
    return render_template('jefatura_daem/list.html', jefaturas=jefaturas)


@jefatura_daem_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_jefatura_daem():
    form = JefaturaDAEMForm()
    if form.validate_on_submit():
        nueva_jefatura = JefaturaDAEM(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_termino=form.fecha_termino.data,
            cargo_jefatura=form.cargo_jefatura.data,
            rut_cuerpo=form.rut_cuerpo.data,
            rut_dv=form.rut_dv.data
        )
        db.session.add(nueva_jefatura)
        db.session.commit()
        flash('Jefatura DAEM creada con éxito', 'success')
        return redirect(url_for('jefatura_daem.listar_jefaturas_daem'))
    return render_template('jefatura_daem/nuevo.html', form=form)


@jefatura_daem_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_jefatura_daem(id):
    jefatura = JefaturaDAEM.query.get_or_404(id)
    form = JefaturaDAEMForm(obj=jefatura)
    if form.validate_on_submit():
        jefatura.nombre = form.nombre.data
        jefatura.email = form.email.data
        jefatura.telefono = form.telefono.data
        jefatura.fecha_inicio = form.fecha_inicio.data
        jefatura.fecha_termino = form.fecha_termino.data
        jefatura.cargo_jefatura = form.cargo_jefatura.data
        jefatura.rut_cuerpo = form.rut_cuerpo.data
        jefatura.rut_dv = form.rut_dv.data

        db.session.commit()
        flash('Jefatura DAEM actualizada con éxito', 'success')
        return redirect(url_for('jefatura_daem.listar_jefaturas_daem'))
    return render_template('jefatura_daem/editar.html', form=form, jefatura=jefatura)


@jefatura_daem_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_jefatura_daem(id):
    jefatura = JefaturaDAEM.query.get_or_404(id)
    db.session.delete(jefatura)
    db.session.commit()
    flash('Jefatura DAEM eliminada con éxito', 'success')
    return redirect(url_for('jefatura_daem.listar_jefaturas_daem'))


# ===================== RUTAS PARA ALCALDÍA =====================

@alcaldia_bp.route('/')
@login_required
@roles_required('administrador')
def listar_alcaldias():
    alcaldias = Alcaldia.query.all()
    return render_template('alcaldia/list.html', alcaldias=alcaldias)


@alcaldia_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_alcaldia():
    form = AlcaldiaForm()
    form.cargar_funcionarios()  # Asegura que las opciones estén cargadas

    if form.validate_on_submit():
        try:
            rut_cuerpo, rut_dv = form.funcionario.data.split("-")

            funcionario = Funcionarios.query.filter_by(
                rut_cuerpo=rut_cuerpo,
                rut_dv=rut_dv
            ).first()

            if not funcionario:
                flash("El funcionario seleccionado no existe.", "danger")
                return redirect(url_for("alcaldia.nueva_alcaldia"))

            nueva_alcaldia = Alcaldia(
                rut_cuerpo=rut_cuerpo,
                rut_dv=rut_dv,
                fecha_inicio=form.fecha_inicio.data,
                fecha_termino=form.fecha_termino.data,
                cargo=form.cargo.data
            )

            db.session.add(nueva_alcaldia)
            db.session.commit()
            flash("✅ Alcaldía creada con éxito.", "success")
            return redirect(url_for("alcaldia.listar_alcaldias"))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al guardar la alcaldía: {str(e)}", "danger")

    return render_template("alcaldia/nuevo.html", form=form)


@alcaldia_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_alcaldia(id):
    alcaldia = Alcaldia.query.get_or_404(id)
    form = AlcaldiaForm(obj=alcaldia)
    form.rut_cuerpo.data = str(alcaldia.rut_cuerpo)
    form.rut_dv.data = alcaldia.rut_dv
    if form.validate_on_submit():
        alcaldia.nombre_alcalde = form.nombre_alcalde.data
        alcaldia.email = form.email.data
        alcaldia.telefono = form.telefono.data
        alcaldia.fecha_inicio = form.fecha_inicio.data
        alcaldia.fecha_termino = form.fecha_termino.data
        alcaldia.cargo = form.cargo.data

        db.session.commit()
        flash('Alcaldía actualizada con éxito', 'success')
        return redirect(url_for('alcaldia.listar_alcaldias'))
    return render_template('alcaldia/editar.html', form=form, alcaldia=alcaldia)


@alcaldia_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_alcaldia(id):
    alcaldia = Alcaldia.query.get_or_404(id)
    db.session.delete(alcaldia)
    db.session.commit()
    flash('Alcaldía eliminada con éxito', 'success')
    return redirect(url_for('alcaldia.listar_alcaldias'))


# ===================== RUTAS PARA TIPO DE CONTRATO =====================

@tipo_contrato_bp.route('/')
@login_required
@roles_required('administrador')
def listar_tipo_contrato():
    tipos_contrato = TipoContrato.query.all()
    delete_form = DeleteForm()
    return render_template('tipo_contrato/list.html', tipos_contrato=tipos_contrato, delete_form=delete_form)


@tipo_contrato_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_tipo_contrato():
    form = TipoContratoForm()
    if form.validate_on_submit():
        nuevo_tipo = TipoContrato(
            nombre=form.nombre.data,
            observacion=form.observacion.data
        )
        db.session.add(nuevo_tipo)
        db.session.commit()
        flash('Tipo de contrato creado con éxito', 'success')
        return redirect(url_for('tipo_contrato_bp.listar_tipo_contrato'))
    return render_template('tipo_contrato/nuevo.html', form=form)


@tipo_contrato_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_tipo_contrato(id):
    tipo = TipoContrato.query.get_or_404(id)
    form = TipoContratoForm(obj=tipo)
    if form.validate_on_submit():
        tipo.nombre = form.nombre.data
        tipo.observacion = form.observacion.data
        db.session.commit()
        flash('Tipo de contrato actualizado con éxito', 'success')
        return redirect(url_for('tipo_contrato_bp.listar_tipo_contrato'))
    return render_template('tipo_contrato/editar.html', form=form, tipo=tipo)


@tipo_contrato_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_tipo_contrato(id):
    tipo = TipoContrato.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    flash('Tipo de contrato eliminado con éxito', 'success')
    return redirect(url_for('tipo_contrato_bp.listar_tipo_contrato'))

# ===================== AUTENTICACIÓN SE MANTIENE EN AUTH_BLUEPRINT =====================

# 🚩 Importante: Las rutas de login, logout y register están dentro de tu Blueprint auth_bp,
# como ya habíamos estructurado profesionalmente en /app/auth/routes.py

# ===================== REGISTRO DE BLUEPRINTS =====================


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(cargo_bp, url_prefix='/cargos')
    app.register_blueprint(colegio_bp, url_prefix='/colegios')
    app.register_blueprint(funcionarios_bp, url_prefix='/funcionarios')
    app.register_blueprint(alcaldia_bp, url_prefix='/alcaldia')
    app.register_blueprint(jefatura_daem_bp, url_prefix='/jefaturas_daem')
    app.register_blueprint(financiamiento_bp, url_prefix='/financiamiento')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(historial_bp, url_prefix='/historial_cambios')
    app.register_blueprint(ordenes_bp, url_prefix='/ordenes_trabajo')
    app.register_blueprint(tipo_contrato_bp, url_prefix='/tipo_contrato')

# 🚩 Con esto routes.py queda completamente refactorizado, estable y profesionalizado.

# --- Asociación entre roles y permisos ---


class RolPermiso(db.Model):
    __tablename__ = 'roles_permisos'
    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(50), nullable=False)
    permiso_id = db.Column(db.Integer, db.ForeignKey(
        'permisos.id'), nullable=False)

    permiso = db.relationship('Permiso', backref='roles_asociados')
