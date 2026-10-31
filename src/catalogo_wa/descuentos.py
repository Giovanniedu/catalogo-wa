"""Cupones y envio: calculo de totales con Decimal (sin floats)."""
from __future__ import annotations
from decimal import Decimal
from .dinero import a_decimal

def buscar_cupon(cupones, codigo: str):
    codigo = (codigo or "").strip().upper()
    for c in cupones or []:
        if c.codigo == codigo:
            return c
    return None

def aplicar_cupon(subtotal: Decimal, cupon) -> Decimal:
    """Devuelve el DESCUENTO (no el total). Nunca negativo ni mayor al subtotal."""
    if cupon is None:
        return a_decimal(0)
    subtotal = a_decimal(subtotal)
    if cupon.tipo == "porcentaje":
        d = (subtotal * a_decimal(cupon.valor) / Decimal("100"))
    else:
        d = a_decimal(cupon.valor)
    return max(a_decimal(0), min(d, subtotal))

def costo_envio(subtotal: Decimal, config) -> Decimal:
    subtotal = a_decimal(subtotal)
    if config.envio_gratis_desde is not None and subtotal >= config.envio_gratis_desde:
        return a_decimal(0)
    return a_decimal(config.envio_costo)

def total_pedido(items, config, codigo_cupon: str = "") -> dict:
    """items: (nombre, cantidad, precio_unitario) -> desglose completo"""
    subtotal = sum((a_decimal(p) * c for _, c, p in items), a_decimal(0))
    cupon = buscar_cupon(config.cupones, codigo_cupon)
    descuento = aplicar_cupon(subtotal, cupon)
    envio = costo_envio(subtotal - descuento, config)
    return {"subtotal": subtotal, "descuento": descuento, "envio": envio,
            "total": subtotal - descuento + envio, "cupon": cupon.codigo if cupon else ""}
