import re


def validar_rut(rut_cuerpo, rut_dv):
    """
    Valida que el RUT chileno sea correcto, incluyendo el dígito verificador.
    """
    print(
        # 👈 Depuración
        f"[VALIDADOR] Validando RUT -> cuerpo: {rut_cuerpo}, dv: {rut_dv}")
    # Validar que el cuerpo del RUT y el dígito verificador no estén vacíos
    if not rut_cuerpo or not rut_dv:
        return False, "RUT y dígito verificador son obligatorios."

    # Validar que el cuerpo del RUT contenga solo números
    if not rut_cuerpo.isdigit() or len(rut_cuerpo) < 7:
        return False, "El RUT solo debe contener números y tener al menos 7 dígitos."

    # Validar que el dígito verificador sea un número o la letra 'K'
    if not re.match(r'^[0-9Kk]$', rut_dv):
        return False, "El dígito verificador debe ser un número o la letra K."

    # Calcular el dígito verificador esperado
    dv_calculado = calcular_dv(rut_cuerpo)

    # Validar el dígito verificador ingresado contra el calculado
    if dv_calculado != rut_dv.upper():
        return False, f"RUT inválido. El dígito verificador debería ser {dv_calculado}."

    return True, "RUT válido."


def calcular_dv(rut):
    """
    Calcula el dígito verificador del RUT chileno usando el algoritmo Módulo 11.
    """
    suma = 0
    factor = 2

    # Invertimos el RUT para aplicar el factor desde el final hacia el inicio
    for digit in reversed(rut):
        suma += int(digit) * factor
        factor = 2 if factor == 7 else factor + 1

    # Calculamos el dígito verificador
    dv = 11 - (suma % 11)

    if dv == 11:
        return '0'
    elif dv == 10:
        return 'K'
    else:
        return str(dv)
