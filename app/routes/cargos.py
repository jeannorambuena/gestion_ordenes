from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import CargoForm
from app.models import Cargo
from app.extensions.extensions import db
from app.utils.roles_required import roles_required

cargo_bp = Blueprint('cargo', __name__)

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
