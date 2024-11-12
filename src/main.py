import requests
import logging
import pandas as pd
import duckdb as db

logging.basicConfig(level=logging.INFO)


class Tratamento_dados:
    
    def __init__(self, json_list): 
        self.json_list = json_list 
        self.con = db.connect()

    def load_data(self):
        for i, data in enumerate(self.json_list):
            df = pd.DataFrame(data)
            nome_tabela =f"table_{i}"
            self.con.register(nome_tabela, df)
            logging.info(f"Tabela '{nome_tabela}' carregada no DuckDB.")

    def query_data(self, sql_query):
        result_df = self.con.execute(sql_query).fetchdf()
        return result_df

class Api:

    def __init__(self, url):
        self.url = url
        #self.download_folder = download_folder

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
    
    def products(self):
        """ Obtém os produtos da api """
        return self.request("products")


if __name__ == "__main__":
    api_teste = Api(url="https://fakestoreapi.com")

    users = api_teste.users()
    carts = api_teste.carts()
    products = api_teste.products()

    tratamento = Tratamento_dados([users, carts, products])
    
    ## Faz o carregamento como tabelas 1, 2, 3, etc
    load = tratamento.load_data()
    
    sql_query = '''
 
    '''

    result_df = tratamento.query_data(sql_query)
    
    print(result_df)

