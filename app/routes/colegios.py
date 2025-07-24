from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import ColegioForm
from app.models import Colegios
from app.extensions.extensions import db
from app.utils.roles_required import roles_required

colegio_bp = Blueprint('colegio', __name__)
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
