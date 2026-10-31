"""Configuracion de la tienda (tienda.json): validada, con valores seguros."""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field
from decimal import Decimal
from .dinero import a_decimal, SIMBOLOS

@dataclass
class Cupon:
    codigo: str
    tipo: str = "porcentaje"   # porcentaje | monto
    valor: Decimal = Decimal("0")

@dataclass
class TiendaConfig:
    negocio: str
    telefono: str
    moneda: str = "PEN"
    idioma: str = "es"
    color: str = "#4a00e0"
    bienvenida: str = ""
    envio_costo: Decimal = Decimal("0")
    envio_gratis_desde: Decimal | None = None
    cupones: list = field(default_factory=list)

    def __post_init__(self):
        if not self.negocio.strip():
            raise ValueError("config: falta 'negocio'")
        if self.moneda.upper() not in SIMBOLOS:
            raise ValueError(f"config: moneda no soportada '{self.moneda}'")
        self.moneda = self.moneda.upper()
        if self.idioma not in ("es", "en", "pt"):
            raise ValueError(f"config: idioma no soportado '{self.idioma}' (es/en/pt)")
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", self.color or ""):
            raise ValueError(f"config: color invalido '{self.color}' (usa #RRGGBB)")
        for c in self.cupones:
            if c.tipo not in ("porcentaje", "monto"):
                raise ValueError(f"cupon {c.codigo}: tipo invalido '{c.tipo}'")
            if c.tipo == "porcentaje" and not (0 < c.valor <= 100):
                raise ValueError(f"cupon {c.codigo}: porcentaje fuera de rango")
            if c.tipo == "monto" and c.valor <= 0:
                raise ValueError(f"cupon {c.codigo}: monto debe ser positivo")

def cargar_config(texto: str) -> TiendaConfig:
    try:
        d = json.loads(texto)
    except json.JSONDecodeError as e:
        raise ValueError(f"tienda.json invalido: {e}") from e
    cupones = [Cupon(codigo=str(c["codigo"]).strip().upper(), tipo=c.get("tipo", "porcentaje"),
                     valor=a_decimal(c.get("valor", 0))) for c in d.get("cupones", [])]
    return TiendaConfig(
        negocio=str(d.get("negocio", "")), telefono=str(d.get("telefono", "")),
        moneda=d.get("moneda", "PEN"), idioma=d.get("idioma", "es"),
        color=d.get("color", "#4a00e0"), bienvenida=str(d.get("bienvenida", "")),
        envio_costo=a_decimal(d.get("envio_costo", 0)),
        envio_gratis_desde=(a_decimal(d["envio_gratis_desde"]) if d.get("envio_gratis_desde") is not None else None),
        cupones=cupones)
