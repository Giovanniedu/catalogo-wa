# catalogo-wa (English)

**A free static web store that takes orders on WhatsApp — no server, no dependencies.**

Most small businesses in Latin America sell on WhatsApp but have no website. `catalogo-wa` turns a simple product list (CSV) into a complete, publishable store page: search, categories, variants, discounts, a working cart, coupons, shipping rules, and an order button that sends the full order — items, quantities, totals — to the business's WhatsApp.

```bash
pip install .
catalogo-wa generar products.csv --config tienda.json --salida site
catalogo-wa preview site
```

Features: validated store config (JSON), per-product variants and % discounts, coupon codes, shipping cost with free-shipping threshold, Decimal money math (7 currencies), storefront UI in Spanish/English/Portuguese, SEO/PWA pack (sitemap, robots, web manifest, Open Graph, JSON-LD Product data), persistent cart, and 34 tests with GitHub Actions CI. MIT licensed. Spanish README: [README.md](README.md).
