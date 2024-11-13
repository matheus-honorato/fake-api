import requests
import logging


class Api:

    def __init__(self, url):
        self.url = url

    def request(self, endpoint):
        """Método para realizar uma requisição GET utilizando endpoint e com tratamento de erros das requisições."""
        url = f"{self.url}/{endpoint}"
        try:
            logging.info(f"Realizando requisição para o endpoint: {url}")
            response = requests.get(url, params=None)
            response.raise_for_status()
            logging.info(f"Requisição para o endpoint {url} foi bem-sucedida.")
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição {url}: {e}")

    def users(self):
        """ Obtém a lista de usuários da api """
        return self.request("users")

    def carts(self):
        """ Obtém os carrinhos de produtos da api """
        return self.request("carts")

    def products(self):
        """ Obtém os produtos da api """
        return self.request("products")