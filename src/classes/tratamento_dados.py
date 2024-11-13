import pandas as pd
import logging
import duckdb as db

logging.basicConfig(level=logging.INFO)


class Tratamento_dados:
    
    def __init__(self, json_list): 
        """
        Inicializa a classe com a lista de JSONs e a conexão com o DuckDB.

        :param json_list: Lista de dados no formato JSON para serem carregados.
        """
        self.json_list = json_list 
        self.con = db.connect()

    def load_data(self):
        """
        Carrega os dados da lista de JSONs para o DuckDB, criando tabelas a partir de cada elemento da lista.
        Cada JSON é convertido em um DataFrame e registrado no banco de dados.
        """
        for i, data in enumerate(self.json_list):
            df = pd.DataFrame(data)
            nome_tabela =f"table_{i}"
            self.con.register(nome_tabela, df)
            logging.info(f"Tabela '{nome_tabela}' carregada no DuckDB.")

    def query_data(self, sql_query):
        """
        Executa uma consulta SQL no DuckDB e exporta o resultado para um arquivo JSON.

        :param sql_query: A consulta SQL que será executada.
        """
        try:
            logging.info("Iniciando a execução da consulta SQL.")
            self.con.execute(f"COPY ({sql_query}) TO 'arquivo_final.json' (FORMAT 'json')")
            logging.info("Consulta SQL executada e arquivo JSON exportado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao executar a consulta SQL: {e}")
            return None  # Retorna None em caso de erro
        finally:
            # Fechar a conexão após a execução para liberar recursos
            self.con.close()
            logging.info("Conexão com o DuckDB fechada.")