
from classes.api import Api
from classes.tratamento_dados import Tratamento_dados

if __name__ == "__main__":
    
    api_teste = Api(url="https://fakestoreapi.com")

    users = api_teste.users()
    carts = api_teste.carts()
    products = api_teste.products()

    tratamento = Tratamento_dados([users, carts, products])

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