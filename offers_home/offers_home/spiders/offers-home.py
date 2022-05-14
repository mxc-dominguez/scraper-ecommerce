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

            # FECHA
            current_product['date'] = date.today()
            
            # TITULO DE PRODUCTO
            product_titles = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]/div[@class="emproduct clear listiteminfogrid"]/div[@data-cp-complete-name="emproduct_cptitleBox"]//a/@title').get()
            current_product['product_title'] = product_titles
            
            # CÓDIGO DE PRODUCTO
            product_codes = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]/div[@class="emproduct clear listiteminfogrid"]//div[@class="emproduct_artnum"]/text()').get()
            current_product['product_code'] = product_codes

            # PRECIO ORIGINAL
            original_prices = float(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emproduct_price"]/span[@class="oldPrice"]/del/text()').get().replace(',', '').strip('\n$'))
            current_product['original_price'] = original_prices

            # PRECIO EN DESCUENTO
            discount_prices = float(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emproduct_price"]/label[@class="price"]/text()').get().replace(',', '').strip('\n$'))
            current_product['discount_price'] = discount_prices

            # DESCUENTO
            current_product['discount'] = original_prices - discount_prices
            
            # PORCENTAJE DE DESCUENTO APROXIMADO
            current_product['approximate_dicount_rate'] = ((original_prices - discount_prices) / original_prices) * 100
            
            # COSTE DE ENVÍO
            delivery_costs = float(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emdeliverycost"]/span[@class="deliveryvalue"]/text()').get().lstrip('$'))
            current_product['delivery_cost'] = delivery_costs
            
            # STOCK
            stock = int(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="moreinfo-section"]/div[@class="emstock"]/span/text()').get())
            current_product['stock'] = stock

            # REVIEWS
            reviews = int(response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product}"]//div[@class="emproduct_review"]//div[@class="reviews-total-txt"]/a/text()').get().strip('\nopiniones'))
            current_product['reviews'] = reviews


            all_products.append(current_product)
        
        products_home = pandas.DataFrame(data=all_products)
        products_home.to_csv('products_offers.csv', index=False, encoding='utf-8')  