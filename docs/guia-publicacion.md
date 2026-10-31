# Guía: publica tu tienda en 10 minutos (gratis)

1. Prepara tu CSV de productos (parte de `examples/productos.csv`).
2. Valídalo: `catalogo-wa validar productos.csv` — corrige los errores por fila que reporte.
3. Crea tu `tienda.json` (parte de `examples/tienda.json`): negocio, WhatsApp, moneda, cupones y envío.
4. Genera: `catalogo-wa generar productos.csv --config tienda.json --salida sitio --url-base https://TU-USUARIO.github.io/TU-REPO`
5. Mírala: `catalogo-wa preview sitio`
6. Publícala gratis en GitHub Pages: sube el contenido de `sitio/` a un repo público y activa Settings → Pages → Deploy from branch (main, /root). En 1-2 minutos tu tienda está en línea.
7. Comparte el enlace en tu Instagram/WhatsApp: los pedidos llegan a tu WhatsApp ya armados.

Sin servidor, sin mensualidades, sin comisiones por venta.
