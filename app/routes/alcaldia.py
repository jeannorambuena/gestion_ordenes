from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import AlcaldiaForm
from app.models.models import Alcaldia, Funcionarios, Cargo
from app.extensions.extensions import db
from app.utils.roles_required import roles_required

alcaldia_bp = Blueprint('alcaldia', __name__)

# ===================== RUTAS PARA ALCALDÍA =====================


@alcaldia_bp.route('/')
@login_required
@roles_required('administrador')
def listar_alcaldias():
    alcaldias = Alcaldia.query.order_by(
        Alcaldia.es_activo.desc(), Alcaldia.fecha_inicio.desc()).all()
    return render_template('alcaldia/list.html', alcaldias=alcaldias)


# Extracto de routes.py para nueva alcaldía con validaciones robustas

@alcaldia_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_alcaldia():
    form = AlcaldiaForm()
    form.id_cargo.choices = [(c.id, c.nombre_cargo) for c in Cargo.query.order_by(
        Cargo.nombre_cargo.asc()).all()]

    # 🔎 Verificamos si ya hay un alcalde titular
    existe_titular = Alcaldia.query.filter_by(es_titular=True).first()

    if form.validate_on_submit():
        try:
            rut_completo = form.rut_alcalde.data.strip()
            if '-' not in rut_completo:
                flash("⚠️ RUT inválido: debe tener guion medio.", "warning")
                return redirect(url_for("alcaldia.nueva_alcaldia"))

            rut_cuerpo, rut_dv = rut_completo.split("-")
            funcionario = Funcionarios.query.filter_by(
                rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()
            if not funcionario:
                flash(
                    "⚠️ El funcionario no se encuentra en la base de datos.", "warning")
                return redirect(url_for("alcaldia.nueva_alcaldia"))

            # 🚫 Si ya existe titular y se intenta marcar otro
            if form.es_titular.data and existe_titular:
                flash(
                    "⚠️ Ya existe un alcalde titular registrado. Solo uno puede existir.", "warning")
                return redirect(url_for("alcaldia.nueva_alcaldia"))

            nueva_alcaldia = Alcaldia(
                rut_cuerpo=rut_cuerpo,
                rut_dv=rut_dv,
                email=funcionario.email,
                telefono=funcionario.telefono,
                fecha_inicio=form.fecha_inicio.data,
                fecha_termino=form.fecha_termino.data,
                id_cargo=form.id_cargo.data,
                es_activo=form.es_activo.data,
                es_titular=form.es_titular.data
            )

            db.session.add(nueva_alcaldia)
            db.session.commit()
            flash("✅ Alcaldía creada con éxito.", "success")
            return redirect(url_for("alcaldia.listar_alcaldias"))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al guardar la alcaldía: {str(e)}", "danger")

    return render_template("alcaldia/nuevo.html", form=form, existe_titular=existe_titular)


@alcaldia_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_alcaldia(id):
    alcaldia = Alcaldia.query.get_or_404(id)

    form = AlcaldiaForm(
        rut_alcalde=f"{alcaldia.rut_cuerpo}-{alcaldia.rut_dv}",
        nombre_alcalde=f"{alcaldia.funcionario.nombre} {alcaldia.funcionario.apellido}" if alcaldia.funcionario else "",
        fecha_inicio=alcaldia.fecha_inicio,
        fecha_termino=alcaldia.fecha_termino
    )

    form.id_cargo.choices = [(c.id, c.nombre_cargo) for c in Cargo.query.order_by(
        Cargo.nombre_cargo.asc()).all()]

    if request.method == 'GET':
        form.id_cargo.data = alcaldia.id_cargo
        form.es_activo.data = alcaldia.es_activo
        form.es_titular.data = alcaldia.es_titular  # ✅ NUEVO

    if form.validate_on_submit():
        try:
            rut_cuerpo, rut_dv = form.rut_alcalde.data.strip().split("-")

            funcionario = Funcionarios.query.filter_by(
                rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()
            if not funcionario:
                flash("❌ El funcionario no existe.", "danger")
                return redirect(url_for("alcaldia.editar_alcaldia", id=id))

            alcaldia.rut_cuerpo = rut_cuerpo
            alcaldia.rut_dv = rut_dv
            alcaldia.email = funcionario.email
            alcaldia.telefono = funcionario.telefono
            alcaldia.fecha_inicio = form.fecha_inicio.data
            alcaldia.fecha_termino = form.fecha_termino.data
            alcaldia.id_cargo = form.id_cargo.data
            alcaldia.es_activo = form.es_activo.data
            alcaldia.es_titular = form.es_titular.data  # ✅ NUEVO

            db.session.commit()

            flash("✅ Alcaldía actualizada correctamente.", "success")
            return redirect(url_for("alcaldia.listar_alcaldias"))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al actualizar la alcaldía: {str(e)}", "danger")

    return render_template("alcaldia/editar.html", form=form, alcaldia=alcaldia, funcionario=alcaldia.funcionario)


@alcaldia_bp.route('/desactivar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def desactivar_alcaldia(id):
    alcaldia = Alcaldia.query.get_or_404(id)
    try:
        alcaldia.es_activo = False  # 🔁 Desactivar en vez de eliminar
        db.session.commit()
        flash('⚠️ Alcaldía desactivada. Ya no está activa como firmante.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error al desactivar alcaldía: {str(e)}', 'danger')
    return redirect(url_for('alcaldia.listar_alcaldias'))
