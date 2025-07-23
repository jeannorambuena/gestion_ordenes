from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import TipoContratoForm, DeleteForm
from app.models.models import TipoContrato
from app.extensions.extensions import db
from app.utils.roles_required import roles_required

tipo_contrato_bp = Blueprint('tipo_contrato', __name__)

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
        return redirect(url_for('tipo_contrato.listar_tipo_contrato'))
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
        return redirect(url_for('tipo_contrato.listar_tipo_contrato'))
    return render_template('tipo_contrato/editar.html', form=form, tipo=tipo)


@tipo_contrato_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_tipo_contrato(id):
    tipo = TipoContrato.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    flash('Tipo de contrato eliminado con éxito', 'success')
    return redirect(url_for('tipo_contrato.listar_tipo_contrato'))
