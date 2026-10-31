# Arquitectura

Pipeline de una sola pasada, sin dependencias (solo biblioteca estándar):

`CSV -> productos.py (validación por fila) + tienda.json -> config.py (validación) -> generador.py (escape anti-XSS + JSON seguro) -> plantilla.py (HTML/CSS/JS autocontenido) + seo.py (sitemap/robots/manifest/JSON-LD/productos.json)`

Decisiones:
- **Dinero con Decimal** (`dinero.py`): los precios nunca pasan por float en Python; el total del pedido se calcula igual en Python (`descuentos.py`) y en el navegador.
- **Seguridad**: todo dato de usuario se escapa (`html.escape`) y el JSON embebido neutraliza `</script>`; las URL de imagen se validan por esquema.
- **El sitio generado no llama a ningún servidor**: el carrito vive en localStorage y el pedido sale por `wa.me` con el mensaje codificado.
- **CLI** (`cli.py`): generar / validar / demo / preview (http.server local).
