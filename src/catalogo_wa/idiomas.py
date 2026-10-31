"""Textos de la tienda generada en es/en/pt (la interfaz, no el contenido)."""
TEXTOS = {
 "es": {"buscar": "Buscar producto...", "todas": "Todas las categorias", "agregar": "Agregar al carrito",
        "agotado": "Agotado", "vacio": "Carrito vacio", "ver": "Ver carrito", "enviar": "Enviar pedido por WhatsApp",
        "pedido": "Tu pedido", "total": "Total", "subtotal": "Subtotal", "descuento": "Descuento", "envio": "Envio",
        "gratis": "Gratis", "cupon": "Codigo de descuento", "aplicar": "Aplicar", "oferta": "OFERTA",
        "saludo": "Hola {negocio}, quiero hacer un pedido:", "gracias": "Gracias.", "ordenar": "Ordenar",
        "recientes": "Mas recientes", "precio_asc": "Precio: menor a mayor", "precio_desc": "Precio: mayor a menor", "nombre": "Nombre A-Z"},
 "en": {"buscar": "Search products...", "todas": "All categories", "agregar": "Add to cart",
        "agotado": "Sold out", "vacio": "Cart is empty", "ver": "View cart", "enviar": "Send order via WhatsApp",
        "pedido": "Your order", "total": "Total", "subtotal": "Subtotal", "descuento": "Discount", "envio": "Shipping",
        "gratis": "Free", "cupon": "Discount code", "aplicar": "Apply", "oferta": "SALE",
        "saludo": "Hi {negocio}, I would like to order:", "gracias": "Thank you.", "ordenar": "Sort",
        "recientes": "Newest", "precio_asc": "Price: low to high", "precio_desc": "Price: high to low", "nombre": "Name A-Z"},
 "pt": {"buscar": "Buscar produto...", "todas": "Todas as categorias", "agregar": "Adicionar ao carrinho",
        "agotado": "Esgotado", "vacio": "Carrinho vazio", "ver": "Ver carrinho", "enviar": "Enviar pedido pelo WhatsApp",
        "pedido": "Seu pedido", "total": "Total", "subtotal": "Subtotal", "descuento": "Desconto", "envio": "Entrega",
        "gratis": "Gratis", "cupon": "Codigo de desconto", "aplicar": "Aplicar", "oferta": "OFERTA",
        "saludo": "Ola {negocio}, quero fazer um pedido:", "gracias": "Obrigado.", "ordenar": "Ordenar",
        "recientes": "Mais recentes", "precio_asc": "Preco: menor para maior", "precio_desc": "Preco: maior para menor", "nombre": "Nome A-Z"},
}
def textos(idioma: str) -> dict:
    if idioma not in TEXTOS:
        raise ValueError(f"Idioma no soportado: {idioma}")
    return TEXTOS[idioma]
