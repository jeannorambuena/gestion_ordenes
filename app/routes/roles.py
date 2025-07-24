from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import RolForm
from app.models import Rol
from app.extensions.extensions import db
from app.utils.roles_required import roles_required

roles_bp = Blueprint('roles', __name__)


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
