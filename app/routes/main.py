from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.models import Funcionarios, Cargo
from app.utils.validators import validar_rut

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def home():
    return render_template('index.html')


@main_bp.route('/validar_rut', methods=['POST'])
def validar_rut_endpoint():
    data = request.get_json()
    rut_cuerpo = data.get("rut_cuerpo", "").strip()
    rut_dv = data.get("rut_dv", "").strip().upper()

    es_valido, mensaje = validar_rut(rut_cuerpo, rut_dv)
    if not es_valido:
        return jsonify({"valid": False, "message": mensaje}), 200

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
            "email": getattr(funcionario, "email", "")
        }), 200
    else:
        return jsonify({
            "valid": True,
            "existe": False
        }), 200
