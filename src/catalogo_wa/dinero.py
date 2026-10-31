"""Formato de dinero seguro con Decimal (nada de floats para precios)."""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

SIMBOLOS = {"PEN": "S/", "USD": "$", "EUR": "€", "MXN": "$", "COP": "$", "CLP": "$", "ARS": "$"}

def a_decimal(valor) -> Decimal:
    try:
        return Decimal(str(valor).replace(",", ".")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Precio invalido: {valor!r}")

def formato_precio(valor, moneda: str = "PEN") -> str:
    moneda = (moneda or "PEN").upper()
    if moneda not in SIMBOLOS:
        raise ValueError(f"Moneda no soportada: {moneda}. Soportadas: {', '.join(sorted(SIMBOLOS))}")
    return f"{SIMBOLOS[moneda]} {a_decimal(valor):,.2f}"
