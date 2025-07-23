from weasyprint import HTML
from babel.dates import format_date
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload
from datetime import datetime, date
from app.forms.forms import OrdenTrabajoForm
from app.models.models import (
    OrdenesTrabajo, Funcionarios, Colegios, TipoContrato,
    Financiamiento, Alcaldia, JefaturaDAEM
)
from app.utils.roles_required import roles_required
from app.extensions.extensions import db
from flask_login import login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response

ordenes_bp = Blueprint('ordenes_bp', __name__)

# ===================== RUTAS PARA ORDENES DE TRABAJO =====================


@ordenes_bp.route('/')
@login_required
@roles_required('administrador')
def listar_ordenes():
    ordenes = OrdenesTrabajo.query.options(
        joinedload(OrdenesTrabajo.funcionario),
        joinedload(OrdenesTrabajo.funcionario_directo),
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
    fecha_larga = format_date(
        fecha_actual, "d 'de' MMMM 'de' y", locale='es_CL')

    html = render_template('ordenes_trabajo/pdf.html',
                           orden=orden,
                           fecha_actual=fecha_actual,
                           fecha_larga=fecha_larga)

    pdf = HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=orden_{orden.numero_orden}.pdf'
    return response


@ordenes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_orden():
    form = OrdenTrabajoForm(anio=datetime.now().year)

    form.colegio_rbd.choices = [(c.rbd, c.nombre_colegio)
                                for c in Colegios.query.all()]
    form.tipo_contrato.choices = [(t.id, t.nombre)
                                  for t in TipoContrato.query.all()]
    form.financiamiento.choices = [
        (f.id, f.nombre_financiamiento) for f in Financiamiento.query.all()]

    alcalde_activo = Alcaldia.query.filter_by(es_activo=True).first()
    jefatura_activa = JefaturaDAEM.query.filter_by(es_activo=True).first()

    ultimo = OrdenesTrabajo.query.order_by(OrdenesTrabajo.id.desc()).first()
    numero_orden = int(ultimo.numero_orden) + 1 if ultimo else 1

    if form.validate_on_submit():
        rut_cuerpo = form.rut_cuerpo.data.strip()
        rut_dv = form.rut_dv.data.strip().upper()

        funcionario = Funcionarios.query.filter_by(
            rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).first()

        nueva_orden = OrdenesTrabajo(
            numero_orden=numero_orden,
            anio=form.anio.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_termino=form.fecha_termino.data,
            es_indefinido=form.es_indefinido.data,
            observaciones=form.observaciones.data,
            horas_disponibles=form.horas_disponibles.data,
            colegio_rbd=form.colegio_rbd.data,
            tipo_contrato_id=form.tipo_contrato.data,
            financiamiento_id=form.financiamiento.data,
            rut_cuerpo=rut_cuerpo,
            rut_dv=rut_dv,
            funcionario_id=funcionario.id if funcionario else None,
            alcalde_id=alcalde_activo.id if alcalde_activo else None,
            jefatura_daem_id=jefatura_activa.id if jefatura_activa else None
        )

        db.session.add(nueva_orden)
        db.session.commit()

        flash('Orden de trabajo creada con éxito', 'success')
        return redirect(url_for('ordenes_bp.listar_ordenes'))

    return render_template('ordenes_trabajo/nueva.html',
                           form=form,
                           numero_orden=numero_orden,
                           alcalde_activo=alcalde_activo,
                           jefatura_activa=jefatura_activa)


@ordenes_bp.route('/horas_disponibles/<rut_cuerpo>-<rut_dv>', methods=['GET'])
@login_required
def obtener_horas_disponibles(rut_cuerpo, rut_dv):
    try:
        hoy = date.today()
        MAX_HORAS_SEMANALES = 44

        ordenes = OrdenesTrabajo.query.filter_by(rut_cuerpo=rut_cuerpo, rut_dv=rut_dv).filter(
            and_(
                OrdenesTrabajo.fecha_inicio <= hoy,
                or_(
                    OrdenesTrabajo.fecha_termino >= hoy,
                    OrdenesTrabajo.es_indefinido == True
                )
            )
        ).options(
            joinedload(OrdenesTrabajo.colegio),
            joinedload(OrdenesTrabajo.financiamiento)
        ).all()

        total_horas_activas = sum(o.horas_disponibles or 0 for o in ordenes)
        horas_disponibles = max(0, MAX_HORAS_SEMANALES - total_horas_activas)

        detalle = []
        for orden in ordenes:
            detalle.append({
                "numero_orden": orden.numero_orden,
                "colegio": orden.colegio.nombre_colegio if orden.colegio else "No asignado",
                "financiamiento": orden.financiamiento.nombre_financiamiento if orden.financiamiento else "N/D",
                "fecha_inicio": orden.fecha_inicio.strftime('%d-%m-%Y') if orden.fecha_inicio else "—",
                "fecha_termino": orden.fecha_termino.strftime('%d-%m-%Y') if orden.fecha_termino else "—",
                "horas": orden.horas_disponibles or 0,
                "es_indefinido": orden.es_indefinido
            })

        return jsonify({
            "horas_disponibles": horas_disponibles,
            "detalle_ordenes": detalle
        })

    except Exception as e:
        return jsonify({
            "error": "Error al calcular horas disponibles.",
            "detalle": str(e)
        }), 500


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
        (a.id, f'{a.funcionario.nombre} {a.funcionario.apellido} ({a.cargo.nombre_cargo})')
        for a in Alcaldia.query.all() if a.funcionario and a.cargo
    ]
    form.jefatura_daem_id.choices = [
        (j.id, f'{j.funcionario.nombre} {j.funcionario.apellido} ({j.cargo.nombre_cargo})')
        for j in JefaturaDAEM.query.all() if j.funcionario and j.cargo
    ]

    if form.validate_on_submit():
        orden.anio = form.anio.data
        orden.fecha_inicio = form.fecha_inicio.data
        orden.fecha_termino = form.fecha_termino.data
        orden.es_indefinido = form.es_indefinido.data
        orden.observaciones = form.observaciones.data
        orden.horas_disponibles = form.horas_disponibles.data
        orden.colegio_rbd = form.colegio_rbd.data
        orden.tipo_contrato_id = form.tipo_contrato.data
        orden.financiamiento_id = form.financiamiento.data
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
