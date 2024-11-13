import requests
import logging


class Api:

    def __init__(self, url):
        """
        Inicializa a classe Api com a URL base.

        :param url: URL base da API.
        """
        self.url = url

    def request(self, endpoint):
        """
        Realiza uma requisição GET para o endpoint e trata erros de requisição.

        :param endpoint: O endpoint da API para onde a requisição será enviada.
        :return: Resposta em formato JSON ou None em caso de erro.
        """
        url = f"{self.url}/{endpoint}"
        try:
            logging.info(f"Realizando requisição para o endpoint: {url}")
            response = requests.get(url)
            response.raise_for_status()
            logging.info(f"Requisição para o endpoint {url} foi bem-sucedida.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição {url}: {e}")
            return None

    def users(self):
        """ Obtém a lista de usuários da api """
        return self.request("users")

    def carts(self):
        """ Obtém os carrinhos de produtos da api """
        return self.request("carts")

    def products(self):
        """ Obtém os produtos da api """
        return self.request("products")