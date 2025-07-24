from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import FinanciamientoForm
from app.models import Financiamiento
from app.extensions.extensions import db
from app.utils.roles_required import roles_required

financiamiento_bp = Blueprint('financiamiento', __name__)
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
