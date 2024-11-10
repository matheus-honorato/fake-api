import requests
import logging

logging.basicConfig(level=logging.INFO)


class Api:

    def __init__(self, url):
        self.url = url

    def request(self, endpoint):
        """Método para realizar uma requisição GET utilizando endpoint e com tratamento de erros das requisições."""
        url = f"{self.url}/{endpoint}"
        try:
            response = requests.get(url, params=None)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição {url}: {e}")

    def users(self):
        """ Obtém a lista de usuários da api """
        return self.request("users")

    def carts(self):
        """ Obtém os carrinhos de produtos da api """
        return self.request("carts")


if __name__ == "__main__":
    api_teste = Api(url="https://fakestoreapi.com")
    users = api_teste.users()
    carts = api_teste.carts()



