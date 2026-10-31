"""Carga y validacion de productos desde CSV, con errores por numero de fila."""
from __future__ import annotations
import csv, io, re
from dataclasses import dataclass, field
from decimal import Decimal
from .dinero import a_decimal

COLUMNAS = ["nombre", "precio", "descripcion", "categoria", "imagen_url", "stock", "descuento_pct", "variantes"]

def parsear_variantes(texto: str) -> list[dict]:
    """'Rojo:5|Azul:3' -> [{nombre: Rojo, stock: 5}, ...] (stock opcional)"""
    salida = []
    for parte in (texto or "").split("|"):
        parte = parte.strip()
        if not parte:
            continue
        if ":" in parte:
            nombre, stock = parte.rsplit(":", 1)
            try:
                stock_n = int(stock.strip())
            except ValueError:
                raise ValueError(f"Variante invalida: '{parte}' (usa Nombre:stock)")
            salida.append({"nombre": nombre.strip(), "stock": stock_n})
        else:
            salida.append({"nombre": parte, "stock": None})
    return salida

def slug(texto: str) -> str:
    t = re.sub(r"[^a-z0-9]+", "-", str(texto).lower().strip(), flags=re.I)
    return t.strip("-") or "producto"

@dataclass
class Producto:
    nombre: str
    precio: Decimal
    descripcion: str = ""
    categoria: str = "General"
    imagen_url: str = ""
    stock: int | None = None
    descuento_pct: int = 0
    variantes: list = field(default_factory=list)
    id: str = field(default="")
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacio")
        if self.precio < 0:
            raise ValueError(f"Precio negativo en '{self.nombre}'")
        if not (0 <= int(self.descuento_pct) <= 90):
            raise ValueError(f"descuento_pct fuera de rango (0-90) en '{self.nombre}'")
        if self.imagen_url and not self.imagen_url.startswith(("http://", "https://", "/", "data:image/")):
            raise ValueError(f"imagen_url invalida en '{self.nombre}': debe ser una URL")
        if not self.id:
            self.id = slug(self.nombre)
    @property
    def agotado(self) -> bool:
        if self.variantes:
            return all((v.get("stock") is not None and v["stock"] <= 0) for v in self.variantes)
        return self.stock is not None and self.stock <= 0

    @property
    def precio_final(self):
        from decimal import Decimal
        return (self.precio * (Decimal(100 - int(self.descuento_pct)) / Decimal(100))).quantize(Decimal("0.01"))

def cargar_csv(texto: str) -> list[Producto]:
    lector = csv.DictReader(io.StringIO(texto))
    if not lector.fieldnames:
        raise ValueError("CSV vacio o sin encabezados")
    faltan = [c for c in ("nombre", "precio") if c not in lector.fieldnames]
    if faltan:
        raise ValueError(f"Faltan columnas obligatorias: {', '.join(faltan)}")
    productos, vistos = [], set()
    for i, fila in enumerate(lector, start=2):
        try:
            stock_txt = (fila.get("stock") or "").strip()
            p = Producto(
                nombre=(fila.get("nombre") or "").strip(),
                precio=a_decimal((fila.get("precio") or "").strip()),
                descripcion=(fila.get("descripcion") or "").strip(),
                categoria=(fila.get("categoria") or "General").strip() or "General",
                imagen_url=(fila.get("imagen_url") or "").strip(),
                stock=int(stock_txt) if stock_txt else None,
                descuento_pct=int((fila.get("descuento_pct") or "0").strip() or 0),
                variantes=parsear_variantes(fila.get("variantes") or ""))
        except ValueError as e:
            raise ValueError(f"Fila {i}: {e}") from e
        if p.id in vistos:
            raise ValueError(f"Fila {i}: producto duplicado (mismo nombre/slug): '{p.nombre}'")
        vistos.add(p.id)
        productos.append(p)
    if not productos:
        raise ValueError("El CSV no tiene productos")
    return productos
