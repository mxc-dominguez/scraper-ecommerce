"""
    joaquín domínguez

        . https://www.linkedin.com/in/mxc-dominguez/
        . @mxc_dominguez en twitter
"""

SCRAPER DE ECOMMERCE

Proyecto de web scraping en un ecommerce para extraer datos de productos en 
oferta y buscar relación relevante entre ellos.

variables:
    product         : orden en el que se muestra en la página [1 - 12].
    date            : fecha en la que se ofertó el producto.
    product_title   : titulo del producto.
    product_code    : SKU o código con el que el ecommerce identifica el producto.
    original_price  : precio antes de que estuviera en descuento
    discount_price  : precio en descuento
    discount        : descuento total
    approximate_discount_rate   : porcentaje de descuento aproximado
    delivery_cost   : coste de envío
    stock           : cantidad de productos en almacén disponibles para vender
    reviews         : reseñas con valoracion en estrellas [5 máximo, 1 mínimo]
        five_stars
        four_stars
        three_stars
        two_stars
        one_star


Esté proyecto se realiza con el fin de incluirlo a un portafolio profesional, 
toda la información extraída de este sitio esta apegada al archivo 'robots.txt', 
este proyecto no será distribuido ni púbilco. Eventualmente será eliminado. 
gracias
