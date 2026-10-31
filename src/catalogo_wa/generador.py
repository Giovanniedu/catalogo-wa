"""Genera el paquete completo del sitio: index.html + sitemap.xml + robots.txt
+ manifest.webmanifest + productos.json. Todo dato de usuario va escapado."""
from __future__ import annotations
import html, json
from pathlib import Path
from .plantilla import PLANTILLA
from .pedidos import normalizar_telefono
from .config import TiendaConfig
from .idiomas import textos
from . import seo

def _json_seguro(obj) -> str:
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

def generar_sitio(productos, negocio: str = "", telefono: str = "", salida="sitio",
                  moneda: str = "PEN", config: TiendaConfig | None = None,
                  url_base: str = "") -> Path:
    if config is not None:
        negocio, telefono, moneda = config.negocio, config.telefono, config.moneda
    if not negocio or not negocio.strip():
        raise ValueError("Falta el nombre del negocio")
    tel = normalizar_telefono(telefono)
    idioma = config.idioma if config else "es"
    color = config.color if config else "#4a00e0"
    bienvenida = (config.bienvenida if config else "") or "Catalogo en linea — pide por WhatsApp, sin registro."
    datos = [{"id": p.id, "nombre": p.nombre, "precio": float(p.precio), "precio_final": float(p.precio_final),
              "descuento_pct": p.descuento_pct, "descripcion": p.descripcion, "categoria": p.categoria,
              "imagen_url": p.imagen_url, "agotado": p.agotado, "variantes": p.variantes} for p in productos]
    cupones = [{"codigo": c.codigo, "tipo": c.tipo, "valor": float(c.valor)} for c in (config.cupones if config else [])]
    envio = {"costo": float(config.envio_costo) if config else 0,
             "gratis_desde": (float(config.envio_gratis_desde) if config and config.envio_gratis_desde is not None else None)}
    pagina = (PLANTILLA
              .replace("__JSONLD__", seo.json_ld(productos, negocio.strip(), moneda))
              .replace("__I18N_JSON__", _json_seguro(textos(idioma)))
              .replace("__CUPONES_JSON__", _json_seguro(cupones))
              .replace("__ENVIO_JSON__", _json_seguro(envio))
              .replace("__NEGOCIO_JSON__", _json_seguro(negocio.strip()))
              .replace("__NEGOCIO__", html.escape(negocio.strip()))
              .replace("__BIENVENIDA__", html.escape(bienvenida))
              .replace("__TELEFONO__", tel)
              .replace("__MONEDA__", moneda.upper())
              .replace("__COLOR__", color)
              .replace("__LANG__", idioma)
              .replace("__PRODUCTOS_JSON__", _json_seguro(datos)))
    destino = Path(salida); destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(pagina, encoding="utf-8")
    (destino / "sitemap.xml").write_text(seo.sitemap(url_base), encoding="utf-8")
    (destino / "robots.txt").write_text(seo.robots(url_base), encoding="utf-8")
    (destino / "manifest.webmanifest").write_text(seo.manifest(negocio.strip(), color), encoding="utf-8")
    (destino / "productos.json").write_text(seo.productos_json(productos, moneda), encoding="utf-8")
    return destino / "index.html"
