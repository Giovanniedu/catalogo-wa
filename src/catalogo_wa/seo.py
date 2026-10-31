"""Artefactos SEO/PWA del sitio: sitemap, robots, manifest y JSON-LD."""
from __future__ import annotations
import json
from .dinero import formato_precio

def json_ld(productos, negocio: str, moneda: str) -> str:
    items = []
    for p in productos:
        items.append({"@type": "Product", "name": p.nombre, "description": p.descripcion,
                      "category": p.categoria,
                      "offers": {"@type": "Offer", "priceCurrency": moneda,
                                 "price": str(p.precio_final),
                                 "availability": "https://schema.org/OutOfStock" if p.agotado else "https://schema.org/InStock"}})
    data = {"@context": "https://schema.org", "@type": "ItemList", "name": negocio, "itemListElement": items}
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

def sitemap(url_base: str) -> str:
    base = (url_base or "").rstrip("/")
    loc = f"{base}/index.html" if base else "index.html"
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"<url><loc>{loc}</loc></url></urlset>\n")

def robots(url_base: str = "") -> str:
    base = (url_base or "").rstrip("/")
    linea = f"Sitemap: {base}/sitemap.xml\n" if base else ""
    return f"User-agent: *\nAllow: /\n{linea}"

def manifest(negocio: str, color: str) -> str:
    return json.dumps({"name": negocio, "short_name": negocio[:12], "display": "standalone",
                       "background_color": "#ffffff", "theme_color": color,
                       "start_url": "./index.html"}, ensure_ascii=False, indent=2)

def productos_json(productos, moneda: str) -> str:
    return json.dumps([{"id": p.id, "nombre": p.nombre, "precio": str(p.precio),
                        "precio_final": str(p.precio_final), "descuento_pct": p.descuento_pct,
                        "categoria": p.categoria, "descripcion": p.descripcion,
                        "imagen_url": p.imagen_url, "stock": p.stock, "agotado": p.agotado,
                        "variantes": p.variantes, "precio_formato": formato_precio(p.precio_final, moneda)}
                       for p in productos], ensure_ascii=False, indent=2)
