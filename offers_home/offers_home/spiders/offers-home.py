"""
    by joaquín domínguez [https://www.linkedin.com/in/mxc-dominguez/]

    spider 'offers_home', extrae los datos de los doce productos en oferta del home de cyberpuerta
"""

# STANDARD LIBRARY
from datetime import date, datetime
from typing import Dict, List
# THIRD PARTY IMPORTS
import numpy
import pandas
import scrapy



class OffersHomeSpider(scrapy.Spider):
    
    name: str = 'offers_home'
    # allowed_domains: List = ['https://www.cyberpuerta.mx']
    start_urls: List = ['https://www.cyberpuerta.mx']


    def parse(self, response) -> None:
        # LOS PRODUCTOS SERÁN EXTRAÍDOS COMO DICCIONARIOS Y PASADOS A UNA LISTA PARA POSTERIORMENTE CONSTRUIR EL DATAFRAME
        
        all_products: List = []

        for product in range(1, 13):

            current_product: Dict = {}
            
            # EXTRACCION DE DATOS
            # NÚMERO DE PRODUCTO
            current_product['product'] = product

            # DATETIME
            current_product['datetime'] = datetime.now()
            
            # TITULO DE PRODUCTO
            try:
                product_titles = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]/div[@class="emproduct clear listiteminfogrid"]/div[@data-cp-complete-name="emproduct_cptitleBox"]//a/@title').get()
                current_product['product_title'] = product_titles
            except TypeError:
                current_product['product_title'] = numpy.nan
            
            # CÓDIGO DE PRODUCTO
            try:
                product_codes = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]/div[@class="emproduct clear listiteminfogrid"]//div[@class="emproduct_artnum"]/text()').get()
                current_product['product_code'] = product_codes
            except TypeError:
                numpy.nan

            # PRECIO ORIGINAL
            try:
                original_prices = float(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emproduct_price"]/span[@class="oldPrice"]/del/text()').get().replace(',', '').strip('\n$'))
                current_product['original_price'] = original_prices
            
            except AttributeError:
                current_product['original_price'] = numpy.nan

            # PRECIO EN DESCUENTO
            try:
                discount_prices = float(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emproduct_price"]/label[@class="price"]/text()').get().replace(',', '').strip('\n$'))
                current_product['discount_price'] = discount_prices
            except AttributeError:
                current_product['discount_price'] = numpy.nan

            # DESCUENTO
            try:
                current_product['discount'] = original_prices - discount_prices
            except UnboundLocalError:
                current_product['discount'] = numpy.nan
            
            # PORCENTAJE DE DESCUENTO APROXIMADO
            try:
                current_product['approximate_dicount_rate'] = ((original_prices - discount_prices) / original_prices)
            except :
                current_product['approximate_dicount_rate'] = numpy.nan
            
            # COSTE DE ENVÍO
            try:
                delivery_costs = float(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emdeliverycost"]/span[@class="deliveryvalue"]/text()').get().lstrip('$'))
                current_product['delivery_cost'] = delivery_costs
            except AttributeError:
                current_product['delivery_cost'] = numpy.nan
            
            # STOCK
            try:
                stock = int(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emstock"]/span/text()').get())
                current_product['stock'] = stock
            except ValueError:
                stock = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emstock"]/span/text()').get()
                current_product['stock'] = stock
            except TypeError:
                numpy.nan

            # REVIEWS
            try:
                reviews = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="emproduct_review"]//div[@class="reviews-total-txt"]/a/text()').get().strip('\nopinioónes')
                current_product['reviews'] = reviews
            except AttributeError:
                current_product['reviews'] = numpy.nan

            # STARS
            for star in range(1, 6):
                try:
                    # EXTRACCIÓN EN BUCLE PARA LAS CINCO TIPOS DE ESTRELLAS POR CADA PRODUCTO
                    # DICCIONARIO PARA NOMBRAR COLUMNAS
                    column_name = {
                        1 : 'five_stars',
                        2 : 'four_stars',
                        3 : 'three_stars',
                        4 : 'two_stars',
                        5 : 'one_star'
                    }
                    # DICCIONARIO PARA IDENTIFICAR QUÉ TIPO DE REVIEW SE EXTRAE. EL NOMBRE ES DEBIDO A QUE EN EL DIV #1 SE ENCUANTRAN LAS PUNTUACIONES DE CINCO ESTRELLAS, EN EL SEGUNDO LAS DE CUATRO ESTRELLAS, ETC.
                    div_to_stars = {
                        1 : 5,
                        2 : 4,
                        3 : 3,
                        4 : 2,
                        5 : 1
                    }
                    # SE LIMPIAN DOS VECES LOS STRING CON STRIP, LA PRIMERA PARA ELIMINAR TODOS LOS CARACTERES HASTA LOS PARENTESIS (ESTO PARA QUE div_to_stars[stars] NO ELIMINE EL NÚMERO DE REVIEWS EN CASO DE QUE COINCIDAN) Y EL SEGUNDO PARA ELIMINAR LOS PARENTESIS DEJANDO SOLO EL NÚMERO
                    stars = int(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="emproduct_review"]//div[@class="cpreviews_starsdesc"]/div[{star}]/div[3]/text()').get().strip(f'{div_to_stars[star]} estrellas: \n').strip('()'))

                    current_product[column_name[star]] = stars
                
                except AttributeError:
                    current_product[column_name[star]] = numpy.nan

            all_products.append(current_product)
        
        products_home = pandas.DataFrame(data=all_products)
        products_home.to_csv(f'data-products-offers/products-offers-{date.today()}_{datetime.now().time()}.csv', index=False, encoding='utf-8')  