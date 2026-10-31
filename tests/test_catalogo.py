import sys, unittest
from decimal import Decimal
sys.path.insert(0, "src")
from catalogo_wa import cargar_csv, generar_sitio, formato_precio, mensaje_pedido, enlace_pedido
from catalogo_wa.productos import Producto

CSV_OK = "nombre,precio,descripcion,categoria,imagen_url,stock\nZapato cuero,209.90,Cuero genuino,Calzado,https://ejemplo.com/z.jpg,5\nSandalia,75.90,,Calzado,,0\n"

class TestDinero(unittest.TestCase):
    def test_formato_pen(self): self.assertEqual(formato_precio("209.9", "PEN"), "S/ 209.90")
    def test_formato_usd(self): self.assertEqual(formato_precio(10, "USD"), "$ 10.00")
    def test_moneda_invalida(self):
        with self.assertRaises(ValueError): formato_precio(10, "XXX")
    def test_precio_invalido(self):
        with self.assertRaises(ValueError): formato_precio("abc")

class TestProductos(unittest.TestCase):
    def test_carga_ok(self):
        ps = cargar_csv(CSV_OK); self.assertEqual(len(ps), 2)
        self.assertTrue(ps[1].agotado); self.assertEqual(ps[0].precio, Decimal("209.90"))
    def test_falta_columna(self):
        with self.assertRaises(ValueError): cargar_csv("nombre\nX\n")
    def test_error_con_fila(self):
        try:
            cargar_csv("nombre,precio\nBien,10\nMal,xyz\n"); self.fail("debio fallar")
        except ValueError as e: self.assertIn("Fila 3", str(e))
    def test_duplicado(self):
        with self.assertRaises(ValueError): cargar_csv("nombre,precio\nA,1\nA,2\n")
    def test_precio_negativo(self):
        with self.assertRaises(ValueError): Producto(nombre="X", precio=Decimal("-1"))

class TestPedidos(unittest.TestCase):
    def test_mensaje_y_total(self):
        m = mensaje_pedido([("Zapato", 2, "100.00"), ("Media", 1, "10.50")], "MiTienda")
        self.assertIn("Total: S/ 210.50", m)
    def test_enlace_codifica(self):
        u = enlace_pedido("987654321", [("Zapato ¿talle?", 1, "50")], "MiTienda")
        self.assertTrue(u.startswith("https://wa.me/51987654321?text=")); self.assertNotIn(" ", u)
    def test_pedido_vacio(self):
        with self.assertRaises(ValueError): mensaje_pedido([], "X")

class TestGenerador(unittest.TestCase):
    def test_sitio_y_escape(self):
        import tempfile, pathlib
        ps = cargar_csv(CSV_OK)
        with tempfile.TemporaryDirectory() as d:
            f = generar_sitio(ps, "Tienda <script>alert(1)</script>", "51987654321", d)
            h = pathlib.Path(f).read_text(encoding="utf-8")
            self.assertNotIn("<script>alert(1)</script> —", h)  # titulo escapado
            self.assertIn("Zapato cuero", h); self.assertIn("wa.me", h); self.assertIn("51987654321", h)
    def test_telefono_local(self):
        import tempfile, pathlib
        ps = cargar_csv(CSV_OK)
        with tempfile.TemporaryDirectory() as d:
            f = generar_sitio(ps, "MiTienda", "987 654 321", d)
            self.assertIn("51987654321", pathlib.Path(f).read_text(encoding="utf-8"))

if __name__ == "__main__": unittest.main()
