"""
    by joaquín domínguez [https://www.linkedin.com/in/mxc-dominguez/]

    spider 'offers_home', extrae los datos de los doce productos en oferta del home de cyberpuerta
"""

# STANDARD LIBRARY
from datetime import date
from typing import Dict, List
# THIRD PARTY IMPORTS
import pandas
import scrapy



class OffersHomeSpider(scrapy.Spider):
    
    name: str = 'offers_home'
    allowed_domains: List = ['https://www.cyberpuerta.mx']
    start_urls: List = ['https://www.cyberpuerta.mx']


    def parse(self, response) -> None:
        # LOS PRODUCTOS SERÁN EXTRAÍDOS COMO DICCIONARIOS Y PASADOS A UNA LISTA PARA POSTERIORMENTE CONSTRUIR EL DATAFRAME
        
        all_products: List = []

        for product in range(1, 13):

            current_product: Dict = {}
            
            # EXTRACCION DE DATOS
            # NÚMERO DE PRODUCTO COMO SE MUESTRA EN LA PÁGINA[1 - 12]
            current_product['product'] = product

            # FECHA DE EXTRACCIÓN
            current_product['extraction_date'] = date.today()
            
            # TITULO DE PRODUCTO
            product_titles = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]/div[@class="emproduct clear listiteminfogrid"]/div[@data-cp-complete-name="emproduct_cptitleBox"]//a/@title').get()
            current_product['product_title'] = product_titles
            
            # CÓDIGO DE PRODUCTO
            product_codes = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]/div[@class="emproduct clear listiteminfogrid"]//div[@class="emproduct_artnum"]/text()').get()
            current_product['product_code'] = product_codes

            # NORMAL PRICE
            normal_prices = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emproduct_price"]/span[@class="oldPrice"]/del/text()').get()
            current_product['normal_price'] = float(normal_prices.replace(',', '').strip('\n$'))

            # PRECIO EN DESCUENTO
            discount_prices = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emproduct_price"]/label[@class="price"]/text()').get()
            current_product['discount_price'] = discount_prices.replace(',', '').strip('\n$')

            all_products.append(current_product)
        
        products_home = pandas.DataFrame(data=all_products)
        products_home.to_csv('products_offers.csv', index=False, encoding='utf-8')  