from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.forms.forms import FuncionarioForm
from app.models import Funcionarios, Cargo
from app.extensions.extensions import db
from app.utils.roles_required import roles_required
# Importa también buscar_funcionarios si lo usas
from app.utils.busqueda_funcionario import buscar_funcionarios

funcionarios_bp = Blueprint('funcionarios', __name__)
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
            return redirect(url_for('funcionarios.listar_funcionarios'))
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
        funcionario.email = form.email.data  # ✅ ESTA LÍNEA FALTABA
        funcionario.id_cargo = form.id_cargo.data

        try:
            db.session.commit()
            flash('Funcionario actualizado con éxito', 'success')
            return redirect(url_for('funcionarios.listar_funcionarios'))
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
        return redirect(url_for('funcionarios.listar_funcionarios'))

    try:
        db.session.delete(funcionario)
        db.session.commit()
        flash('Funcionario eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(
            f'Ocurrió un error al eliminar el funcionario: {str(e)}', 'danger')

    return redirect(url_for('funcionarios.listar_funcionarios'))


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


@funcionarios_bp.route('/buscar', methods=['GET'])
@login_required
def buscar_funcionarios_ajax():
    # Obtener el texto de búsqueda desde el parámetro GET (?query=...)
    query = request.args.get('query', '').strip()

    # Validar que el usuario escribió al menos 3 caracteres
    if len(query) < 3:
        return jsonify([])  # Devolver lista vacía si no cumple

    # Usar la función auxiliar ya importada para buscar funcionarios
    resultados = buscar_funcionarios(query, db.session)

    # Retornar los resultados como JSON
    return jsonify(resultados)
