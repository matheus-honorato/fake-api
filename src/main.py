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
        result_df = self.con.execute(f"COPY ({sql_query}) TO 'output.json' (FORMAT 'json')")

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
    WITH
    users as (
        SELECT id userId FROM table_0
    ),
    carts as (
    SELECT 
        id as id_cart, 
        userId,
        date,
        unnest(products) AS product,
        product['productId'] AS productId,
        product['quantity'] AS product_Quantity
    FROM table_1),
    products as (
        SELECT id as productId, category FROM table_2
    ),
    join_1 as (
        SELECT 
            a.userId, 
            b.id_cart, 
            productId,
            CAST(b.date AS DATE) as data_carrinho,
            product_Quantity
        FROM users as a INNER JOIN carts as b 
        ON a.userId = b.userId
    ),
    join_final as (
    SELECT 
        a.*, 
        b.category 
    FROM join_1 as a INNER JOIN products as b 
    ON a.productId = b.productId),

    max_dates AS (
        SELECT 
            userId, 
            MAX(data_carrinho) AS data_carrinho
        FROM join_final
        GROUP BY userId
    ),
    rank_1 as (
        SELECT 
            userId, 
            category, 
            SUM(product_Quantity) product_Quantity
        FROM join_final
        GROUP BY ALL
    ),
    rank_2 as (
    SELECT 
        userId, category, 
        product_Quantity, ROW_NUMBER() OVER (PARTITION BY userId ORDER BY product_Quantity desc) rnk
    FROM rank_1)

    SELECT a.userId, b.data_carrinho , category FROM rank_2 as a
    JOIN max_dates as b ON a.userId = b.userId
    WHERE rnk = 1
    '''

    result_df = tratamento.query_data(sql_query)
    
    print(result_df)

