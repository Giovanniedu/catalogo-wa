import sys, json, tempfile, pathlib
from decimal import Decimal
sys.path.insert(0, "src")
from catalogo_wa import cargar_config, total_pedido, aplicar_cupon, cargar_csv, generar_sitio
from catalogo_wa.config import TiendaConfig, Cupon
from catalogo_wa.productos import parsear_variantes
from catalogo_wa.idiomas import textos
from catalogo_wa import seo

CONF = {"negocio": "MiTienda", "telefono": "51987654321", "cupones": [{"codigo": "DIEZ", "tipo": "porcentaje", "valor": 10}, {"codigo": "MENOS20", "tipo": "monto", "valor": 20}], "envio_costo": 10, "envio_gratis_desde": 200}

class TestConfig:
    pass

import unittest
class TestConfigU(unittest.TestCase):
    def test_carga_ok(self):
        c = cargar_config(json.dumps(CONF)); self.assertEqual(c.negocio, "MiTienda"); self.assertEqual(len(c.cupones), 2)
    def test_color_invalido(self):
        d = dict(CONF, color="rojo")
        with self.assertRaises(ValueError): cargar_config(json.dumps(d))
    def test_idioma_invalido(self):
        d = dict(CONF, idioma="fr")
        with self.assertRaises(ValueError): cargar_config(json.dumps(d))
    def test_json_roto(self):
        with self.assertRaises(ValueError): cargar_config("{no json")
    def test_cupon_pct_fuera_rango(self):
        with self.assertRaises(ValueError):
            TiendaConfig(negocio="X", telefono="1", cupones=[Cupon("A", "porcentaje", Decimal("150"))])

class TestDescuentos(unittest.TestCase):
    def setUp(self): self.c = cargar_config(json.dumps(CONF))
    def test_cupon_porcentaje(self):
        t = total_pedido([("A", 1, "100")], self.c, "DIEZ")
        self.assertEqual(t["descuento"], Decimal("10.00")); self.assertEqual(t["total"], Decimal("100.00"))  # 100-10+10 envio
    def test_cupon_monto_no_supera_subtotal(self):
        t = total_pedido([("A", 1, "15")], self.c, "MENOS20")
        self.assertEqual(t["descuento"], Decimal("15.00"))
    def test_envio_gratis(self):
        t = total_pedido([("A", 1, "250")], self.c, "")
        self.assertEqual(t["envio"], Decimal("0.00")); self.assertEqual(t["total"], Decimal("250.00"))
    def test_cupon_inexistente(self):
        self.assertEqual(aplicar_cupon(Decimal("100"), None), Decimal("0.00"))

class TestVariantes(unittest.TestCase):
    def test_parseo(self):
        v = parsear_variantes("Rojo:5|Azul|Verde:0")
        self.assertEqual(v[0], {"nombre": "Rojo", "stock": 5}); self.assertIsNone(v[1]["stock"])
    def test_parseo_invalido(self):
        with self.assertRaises(ValueError): parsear_variantes("Rojo:abc")
    def test_agotado_por_variantes(self):
        ps = cargar_csv("nombre,precio,variantes\nX,10,\"A:0|B:0\"\n")
        self.assertTrue(ps[0].agotado)
    def test_precio_final_descuento(self):
        ps = cargar_csv("nombre,precio,descuento_pct\nX,100,10\n")
        self.assertEqual(ps[0].precio_final, Decimal("90.00"))

class TestI18n(unittest.TestCase):
    def test_tres_idiomas(self):
        for i in ("es", "en", "pt"):
            self.assertIn("enviar", textos(i))
    def test_idioma_invalido(self):
        with self.assertRaises(ValueError): textos("de")

class TestSeo(unittest.TestCase):
    def setUp(self): self.ps = cargar_csv("nombre,precio,descripcion\nZapato,100,Cuero\n")
    def test_jsonld(self):
        j = seo.json_ld(self.ps, "Tienda", "PEN"); self.assertIn('"@type": "Product"', j); self.assertIn("100.00", j)
    def test_sitemap(self): self.assertIn("https://mitienda.pe/index.html", seo.sitemap("https://mitienda.pe/"))
    def test_manifest(self):
        m = json.loads(seo.manifest("Tienda", "#4a00e0")); self.assertEqual(m["theme_color"], "#4a00e0")

class TestGeneradorV2(unittest.TestCase):
    def test_paquete_completo(self):
        ps = cargar_csv("nombre,precio,descuento_pct\nZapato,100,10\n")
        c = cargar_config(json.dumps(CONF))
        with tempfile.TemporaryDirectory() as d:
            f = generar_sitio(ps, salida=d, config=c, url_base="https://mitienda.pe")
            nombres = sorted(p.name for p in pathlib.Path(d).iterdir())
            self.assertEqual(nombres, ["index.html", "manifest.webmanifest", "productos.json", "robots.txt", "sitemap.xml"])
            h = pathlib.Path(f).read_text(encoding="utf-8")
            self.assertIn("application/ld+json", h); self.assertIn("DIEZ", h)
            pj = json.loads(pathlib.Path(d, "productos.json").read_text(encoding="utf-8"))
            self.assertEqual(pj[0]["precio_final"], "90.00")
    def test_config_en_reemplaza_args(self):
        ps = cargar_csv("nombre,precio\nZapato,100\n")
        c = cargar_config(json.dumps(CONF))
        with tempfile.TemporaryDirectory() as d:
            f = generar_sitio(ps, salida=d, config=c)
            self.assertIn("MiTienda", pathlib.Path(f).read_text(encoding="utf-8"))

if __name__ == "__main__": unittest.main()
