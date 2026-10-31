"""CLI con subcomandos: generar | validar | demo | preview"""
import argparse, sys
from pathlib import Path
from .productos import cargar_csv
from .generador import generar_sitio
from .config import cargar_config

def _productos(ruta):
    return cargar_csv(Path(ruta).read_text(encoding="utf-8-sig"))

def cmd_generar(a):
    productos = _productos(a.csv)
    config = cargar_config(Path(a.config).read_text(encoding="utf-8")) if a.config else None
    if config is None and (not a.negocio or not a.telefono):
        print("Error: usa --config tienda.json o pasa --negocio y --telefono", file=sys.stderr); return 2
    f = generar_sitio(productos, a.negocio or "", a.telefono or "", a.salida, a.moneda, config=config, url_base=a.url_base or "")
    print(f"Listo: {f} + sitemap.xml, robots.txt, manifest.webmanifest, productos.json ({len(productos)} productos)")
    return 0

def cmd_validar(a):
    try:
        productos = _productos(a.csv)
    except ValueError as e:
        print(f"CSV con errores: {e}"); return 1
    cats = sorted({p.categoria for p in productos})
    agotados = sum(1 for p in productos if p.agotado)
    print(f"CSV valido: {len(productos)} productos, {len(cats)} categorias ({', '.join(cats)}), {agotados} agotados")
    return 0

def cmd_demo(a):
    base = Path(__file__).resolve().parents[2] / "examples"
    csv_demo = base / "productos.csv"
    if not csv_demo.exists():
        print("No se encontro examples/productos.csv (usa el repo completo)", file=sys.stderr); return 1
    productos = _productos(str(csv_demo))
    f = generar_sitio(productos, "Tienda Demo catalogo-wa", "51999999999", a.salida)
    print(f"Demo generada en {f}")
    return 0

def cmd_preview(a):
    import functools, http.server, socketserver, webbrowser
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=a.salida)
    with socketserver.TCPServer(("127.0.0.1", a.puerto), handler) as httpd:
        url = f"http://127.0.0.1:{a.puerto}/"
        print(f"Vista previa en {url} (Ctrl+C para salir)")
        try: webbrowser.open(url)
        except Exception: pass
        try: httpd.serve_forever()
        except KeyboardInterrupt: print("\nServidor detenido")
    return 0

def main(argv=None):
    p = argparse.ArgumentParser(prog="catalogo-wa", description="Tienda web estatica con pedidos por WhatsApp, desde un CSV.")
    sub = p.add_subparsers(dest="cmd")
    g = sub.add_parser("generar", help="Genera el sitio desde un CSV")
    g.add_argument("csv"); g.add_argument("--negocio"); g.add_argument("--telefono")
    g.add_argument("--moneda", default="PEN"); g.add_argument("--salida", default="sitio")
    g.add_argument("--config", help="Archivo tienda.json (alternativa a --negocio/--telefono)")
    g.add_argument("--url-base", help="URL publica del sitio, para sitemap/robots")
    v = sub.add_parser("validar", help="Valida un CSV sin generar nada"); v.add_argument("csv")
    d = sub.add_parser("demo", help="Genera la tienda demo con el CSV de ejemplo"); d.add_argument("--salida", default="sitio-demo")
    pr = sub.add_parser("preview", help="Sirve una carpeta generada en local"); pr.add_argument("salida"); pr.add_argument("--puerto", type=int, default=8000)
    a = p.parse_args(argv)
    fn = {"generar": cmd_generar, "validar": cmd_validar, "demo": cmd_demo, "preview": cmd_preview}.get(a.cmd or "")
    if fn is None:
        p.print_help(); return 2
    try:
        return fn(a)
    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr); return 1

if __name__ == "__main__":
    raise SystemExit(main())
