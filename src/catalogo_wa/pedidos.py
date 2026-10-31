"""Construye el mensaje de pedido y el enlace wa.me del carrito."""
from __future__ import annotations
from urllib.parse import quote
from .dinero import formato_precio, a_decimal

def normalizar_telefono(telefono: str) -> str:
    import re
    d = re.sub(r"\D", "", str(telefono or ""))
    if d.startswith("00"):
        d = d[2:]
    if len(d) == 9:
        d = "51" + d
    if not (8 <= len(d) <= 15):
        raise ValueError(f"Telefono invalido: {telefono!r}")
    return d

def mensaje_pedido(items, negocio: str, moneda: str = "PEN") -> str:
    """items: lista de (nombre, cantidad, precio_unitario)"""
    if not items:
        raise ValueError("El pedido esta vacio")
    lineas = [f"Hola {negocio}, quiero hacer un pedido:", ""]
    total = a_decimal(0)
    for nombre, cant, precio in items:
        if cant <= 0:
            raise ValueError(f"Cantidad invalida en '{nombre}'")
        sub = a_decimal(precio) * cant
        total += sub
        lineas.append(f"- {cant} x {nombre} = {formato_precio(sub, moneda)}")
    lineas += ["", f"Total: {formato_precio(total, moneda)}", "Gracias."]
    return "\n".join(lineas)

def enlace_pedido(telefono: str, items, negocio: str, moneda: str = "PEN") -> str:
    tel = normalizar_telefono(telefono)
    return f"https://wa.me/{tel}?text={quote(mensaje_pedido(items, negocio, moneda))}"
