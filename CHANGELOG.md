# Changelog
## 0.2.1 — 2026-10-30
- Presentación nivel proyecto serio: banner e ilustración, logo, badges (CI, Python, 0 dependencias, versión, MIT, tests), tabla de contenido, imágenes demo de la tienda generada y de la terminal (patrón de los repos más populares: banner + badges + screenshot/GIF + quick start al inicio).

## 0.2.0 — 2026-10-30
- Configuracion completa de tienda (`tienda.json`): color, bienvenida, idioma, envio y cupones, todo validado.
- Cupones de descuento (porcentaje o monto fijo) y costo de envio con envio gratis desde un monto — calculo con Decimal y desglose en el pedido.
- Variantes por producto (tallas/colores con stock propio) y descuento % por producto con precio tachado.
- Sitio multilingue: interfaz en español, ingles y portugues.
- Paquete SEO/PWA: sitemap.xml, robots.txt, manifest.webmanifest, Open Graph y datos estructurados JSON-LD (Product/Offer).
- Carrito persistente (localStorage), ordenamiento por precio/nombre y desglose subtotal/descuento/envio/total.
- CLI con subcomandos: `generar`, `validar`, `demo` y `preview` (servidor local).
- `productos.json` publico generado para integraciones.
- Tests: 34 (dinero, productos, variantes, config, cupones, i18n, SEO, generador, pedidos).

## 0.1.0 — 2026-10-30
- Version inicial: CSV -> index.html con buscador, categorias, carrito y pedido por WhatsApp.
