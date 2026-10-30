
from decimal import Decimal, ROUND_HALF_UP


ERROR_NOMBRE = "Error: First Name is required"
ERROR_APELLIDO = "Error: Last Name is required"
ERROR_CODIGO_POSTAL = "Error: Postal Code is required"
CENTAVO = Decimal("0.01")
TASA_IMPUESTO = Decimal("0.08")


def validar_datos_envio(nombre, apellido, codigo_postal):
    """Devuelve el primer error de envío o una cadena vacía si todo es válido.

    El orden de validación es nombre, apellido y código postal. Los valores
    nulos, vacíos o compuestos únicamente por espacios se consideran vacíos.
    """
    if nombre is None or not str(nombre).strip():
        return ERROR_NOMBRE
    if apellido is None or not str(apellido).strip():
        return ERROR_APELLIDO
    if codigo_postal is None or not str(codigo_postal).strip():
        return ERROR_CODIGO_POSTAL
    return ""


def calcular_resumen(subtotal):
    """Calcula subtotal, impuesto del 8 % y total usando Decimal.

    El impuesto se redondea al centavo más cercano con la regla mitad hacia
    arriba. El total es la suma del subtotal original y el impuesto redondeado.
    Un subtotal negativo produce ValueError.
    """
    try:
        importe = subtotal if isinstance(subtotal, Decimal) else Decimal(str(subtotal))
    except (TypeError, ValueError, ArithmeticError) as exc:
        raise ValueError("El subtotal debe ser un importe numérico válido") from exc

    if not importe.is_finite():
        raise ValueError("El subtotal debe ser un importe finito")
    if importe < 0:
        raise ValueError("El subtotal no puede ser negativo")

    impuesto = (importe * TASA_IMPUESTO).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    total = importe + impuesto
    return {
        "subtotal": importe,
        "impuesto": impuesto,
        "total": total,
    }
