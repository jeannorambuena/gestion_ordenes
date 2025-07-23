from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import JefaturaDAEMForm
from app.models.models import JefaturaDAEM, Funcionarios
from app.extensions.extensions import db
from app.utils.roles_required import roles_required
from datetime import datetime

jefatura_daem_bp = Blueprint('jefatura_daem', __name__)

# ===================== RUTAS PARA JEFATURA DAEM =====================


@jefatura_daem_bp.route('/')
@login_required
@roles_required('administrador')
def listar_jefaturas_daem():
    jefaturas = JefaturaDAEM.query.all()
    datos = []

    for j in jefaturas:
        funcionario = Funcionarios.query.filter_by(
            rut_cuerpo=j.rut_cuerpo,
            rut_dv=j.rut_dv
        ).first()
        datos.append({
            "jefatura": j,
            "funcionario": funcionario
        })

    return render_template('jefatura_daem/list.html', datos=datos)


@jefatura_daem_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_jefatura_daem():
    form = JefaturaDAEMForm()

    # Detectar si ya existe un jefe titular
    ya_hay_titular = JefaturaDAEM.query.filter_by(
        es_titular=True).first() is not None

    if form.validate_on_submit():
        try:
            rut_completo = form.rut_funcionario.data.strip()
            if '-' not in rut_completo:
                flash("⚠️ RUT inválido: debe contener guion medio.", "warning")
                return redirect(url_for("jefatura_daem.nueva_jefatura_daem"))

            rut_cuerpo, rut_dv = rut_completo.split("-")

            funcionario = Funcionarios.query.filter_by(
                rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()
            if not funcionario:
                flash("⚠️ El funcionario no está registrado.", "warning")
                return redirect(url_for("funcionarios_bp.nuevo_funcionario", rut=rut_completo))

            if form.es_titular.data and ya_hay_titular:
                flash(
                    "❌ Ya existe un jefe DAEM titular registrado. No se puede asignar otro.", "danger")
                return redirect(url_for("jefatura_daem.nueva_jefatura_daem"))

            nueva_jefatura = JefaturaDAEM(
                rut_cuerpo=rut_cuerpo,
                rut_dv=rut_dv,
                id_cargo=form.id_cargo.data,
                fecha_inicio=form.fecha_inicio.data,
                fecha_termino=form.fecha_termino.data,
                es_titular=form.es_titular.data,
                es_activo=form.es_activo.data
            )

            db.session.add(nueva_jefatura)
            db.session.commit()
            flash("✅ Jefatura DAEM creada con éxito.", "success")
            return redirect(url_for("jefatura_daem.listar_jefaturas_daem"))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al guardar la jefatura: {str(e)}", "danger")

    return render_template("jefatura_daem/nuevo.html", form=form, ya_hay_titular=ya_hay_titular)


@jefatura_daem_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_jefatura_daem(id):
    jefatura = JefaturaDAEM.query.get_or_404(id)

    funcionario = Funcionarios.query.filter_by(
        rut_cuerpo=jefatura.rut_cuerpo,
        rut_dv=jefatura.rut_dv
    ).first()

    if not funcionario:
        flash("⚠️ Funcionario asociado no encontrado.", "warning")
        return redirect(url_for('jefatura_daem.listar_jefaturas_daem'))

    rut_formateado = f"{funcionario.rut_cuerpo}-{funcionario.rut_dv}"
    nombre_completo_funcionario = f"{funcionario.nombre} {funcionario.apellido}"

    form = JefaturaDAEMForm(
        rut_funcionario=rut_formateado,
        fecha_inicio=jefatura.fecha_inicio,
        fecha_termino=jefatura.fecha_termino,
        es_titular=jefatura.es_titular
    )

    if request.method == 'GET':
        form.id_cargo.data = jefatura.id_cargo
        form.es_activo.data = jefatura.es_activo

    if form.validate_on_submit():
        try:
            jefatura.fecha_inicio = form.fecha_inicio.data
            jefatura.fecha_termino = form.fecha_termino.data
            jefatura.id_cargo = form.id_cargo.data

            # ⚙️ Control de activación
            if form.es_activo.data:
                if not jefatura.es_titular:
                    titular = JefaturaDAEM.query.filter_by(
                        es_titular=True,
                        es_activo=True
                    ).first()

                    if titular and titular.id != jefatura.id:
                        titular.es_activo = False
                        titular.fecha_termino = datetime.now().date()

            jefatura.es_activo = form.es_activo.data

            db.session.commit()
            flash("✅ Jefatura DAEM actualizada con éxito.", "success")
            return redirect(url_for('jefatura_daem.listar_jefaturas_daem'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al actualizar la jefatura: {str(e)}", "danger")

    return render_template(
        'jefatura_daem/editar.html',
        form=form,
        jefatura=jefatura,
        nombre_completo_funcionario=nombre_completo_funcionario
    )


@jefatura_daem_bp.route('/desactivar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def desactivar_jefatura_daem(id):
    jefatura = JefaturaDAEM.query.get_or_404(id)
    try:
        jefatura.es_activo = False
        db.session.commit()
        flash('⚠️ Jefatura DAEM desactivada correctamente.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error al desactivar jefatura: {str(e)}', 'danger')
    return redirect(url_for('jefatura_daem.listar_jefaturas_daem'))
