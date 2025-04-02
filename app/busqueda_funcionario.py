from app.models import Funcionarios
from sqlalchemy import or_


def buscar_funcionarios(criterio, session):
    criterio = criterio.lower()
    resultados = session.query(Funcionarios).filter(
        (Funcionarios.rut_cuerpo.like(f"%{criterio}%")) |
        (Funcionarios.nombre.ilike(f"%{criterio}%")) |
        (Funcionarios.apellido.ilike(f"%{criterio}%"))
    ).all()

    return [{'rut': f"{func.rut_cuerpo}-{func.rut_dv}", 'nombre': func.nombre, 'apellido': func.apellido}
            for func in resultados]
