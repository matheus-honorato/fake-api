import pandas as pd
import logging
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
        logging.info("Iniciando a execução da consulta SQL.")
        result_df = self.con.execute(f"COPY ({sql_query}) TO 'arquivo_final.json' (FORMAT 'json')")
        logging.info("Consulta SQL executada e arquivo JSON exportado com sucesso.")