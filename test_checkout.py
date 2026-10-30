"""Pruebas unitarias de CU-03 (envío) y CU-04 (resumen del pedido)."""
from decimal import Decimal

import pytest

from src.checkout import (
    ERROR_APELLIDO,
    ERROR_CODIGO_POSTAL,
    ERROR_NOMBRE,
    calcular_resumen,
    validar_datos_envio,
)


# CU-03 / RN-A5: camino válido y particiones inválidas.
def test_cu03_datos_de_envio_completos_son_validos():
    assert validar_datos_envio("Ana", "Pérez", "10001") == ""


@pytest.mark.parametrize(
    "nombre, apellido, codigo_postal, esperado",
    [
        ("", "Pérez", "10001", ERROR_NOMBRE),
        (None, "Pérez", "10001", ERROR_NOMBRE),
        ("   ", "Pérez", "10001", ERROR_NOMBRE),
        ("Ana", "", "10001", ERROR_APELLIDO),
        ("Ana", "   ", "10001", ERROR_APELLIDO),
        ("Ana", "Pérez", "", ERROR_CODIGO_POSTAL),
        ("Ana", "Pérez", "   ", ERROR_CODIGO_POSTAL),
        ("", "", "", ERROR_NOMBRE),
    ],
)
def test_cu03_campos_vacios_o_solo_espacios_devuelven_primer_error(
    nombre, apellido, codigo_postal, esperado
):
    assert validar_datos_envio(nombre, apellido, codigo_postal) == esperado


def test_cu03_prioriza_apellido_antes_que_codigo_postal():
    assert validar_datos_envio("Ana", " ", "") == ERROR_APELLIDO


def test_cu03_prioriza_nombre_si_todos_los_campos_estan_vacios():
    assert validar_datos_envio(" ", " ", " ") == ERROR_NOMBRE


# CU-04 / RN-A6: cálculo correcto, redondeo mitad hacia arriba y error de límite.
def test_cu04_calcula_impuesto_y_total_para_subtotal_valido():
    resultado = calcular_resumen(Decimal("50.00"))
    assert resultado == {
        "subtotal": Decimal("50.00"),
        "impuesto": Decimal("4.00"),
        "total": Decimal("54.00"),
    }


def test_cu04_redondea_impuesto_a_centavo_mas_cercano():
    resultado = calcular_resumen(Decimal("10.06"))
    assert resultado["impuesto"] == Decimal("0.80")
    assert resultado["total"] == Decimal("10.86")


def test_cu04_redondea_la_mitad_hacia_arriba():
    # 10.0625 × 8 % = 0.805; la regla RN-A6 exige redondear a 0.81.
    resultado = calcular_resumen(Decimal("10.0625"))
    assert resultado["impuesto"] == Decimal("0.81")
    assert resultado["total"] == Decimal("10.8725")


def test_cu04_subtotal_cero_produce_impuesto_y_total_cero():
    resultado = calcular_resumen(Decimal("0.00"))
    assert resultado["impuesto"] == Decimal("0.00")
    assert resultado["total"] == Decimal("0.00")


@pytest.mark.parametrize("subtotal", [Decimal("-0.01"), Decimal("-10.00")])
def test_cu04_subtotal_negativo_lanza_value_error(subtotal):
    with pytest.raises(ValueError):
        calcular_resumen(subtotal)
