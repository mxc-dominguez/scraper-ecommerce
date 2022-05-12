"""
    by joaquín domínguez [https://www.linkedin.com/in/mxc-dominguez/]

    spider 'offers_home', extrae los datos de los doce productos en oferta del home de cyberpuerta
"""

# STANDARD LIBRARY
from typing import Dict, List
# THIRD PARTY IMPORTS
import scrapy
import pandas



class OffersHomeSpider(scrapy.Spider):
    
    name: str = 'offers_home'
    allowed_domains: List = ['https://www.cyberpuerta.mx']
    start_urls: List = ['https://www.cyberpuerta.mx']


    def parse(self, response) -> None:
        # LOS DATOS EXTRAIDOS INICIALMENTE SE GUARDAN EN UN DICCIONARIO CON EL 
        # PROPOSITO DE CONVERTIRLOS EN UN OBJETO pandas.Series Y ASÍ CONSERVAR 
        # LA RELACION ENTRE EL NÚMERO DEL PRODUCTO Y SUS DATOS
        product_titles: Dict = {}

        for product_title in range(1, 13):
            # EXTRAYENDO TITULOS
            value = response.xpath(f'//ul[@id="cp-start-daily-offers"]//form[@name="tobasketemstartpagenew-{product_title}"]/div[@class="emproduct clear listiteminfogrid"]/div[@data-cp-complete-name="emproduct_cptitleBox"]//a/@title').get()
            # ASIGNANDO TITULOS
            product_titles[product_title] = value
        # CONVIRTIENDO DICCIONARIO A OBJETO pandas.Series
        product_titles = pandas.Series(data=product_titles, dtype=str, name='product_titles')
        # EXPORTANDO A CSV, ESTO PARA ESTAR SEGUROS QUE SE GUARDA LA RELACIÓN Y 
        # LOS TITULOS SE VISUALIZAN COMPLETOS, ESTO NO SERÁ NECESARIO EN LA VERSION FINAL
        product_titles.to_csv('products_offers.csv')