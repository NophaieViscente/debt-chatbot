import os
import pandas as pd
import sqlite3


class DataBaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            if not os.path.exists(self.db_name):
                print(
                    f"Database file not found. Creating a new database at: {self.db_name}"
                )
                open(
                    self.db_name, "w"
                ).close()  # Create an empty file if it doesn't exist
            self.connection = sqlite3.connect(self.db_name)
            print("Connection established successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def create_tables(self):
        """Create the payment options and customers tables if they don't already exist."""
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS payment_options (
                    opcao_pagamento_id INTEGER PRIMARY KEY,
                    valor_entrada REAL,
                    valor_parcela REAL,
                    valor_desconto REAL,
                    valor_negociado REAL,
                    quantidade_parcelas INTEGER,
                    data_primeiro_boleto DATE,
                    cpf_cnpj TEXT
                )
            """
            )
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    consumidor_id INTEGER PRIMARY KEY,
                    cpf_cnpj TEXT,
                    nome TEXT,
                    data_nascimento DATE,
                    perfil TEXT,
                    divida_id INTEGER,
                    codigo_contrato TEXT,
                    data_origem DATE,
                    valor_vencido REAL,
                    valor_multa REAL,
                    valor_juros REAL,
                    produto TEXT,
                    loja TEXT
                )
            """
            )

    def insert_dataframe(self, df, table_name):
        """Insert a pandas DataFrame into the specified table."""
        with self.connection:
            df.to_sql(table_name, self.connection, if_exists="replace", index=False)

    def fetch_all(self, table_name):
        """Fetch all rows from the specified table."""
        with self.connection:
            return pd.read_sql(f"SELECT * FROM {table_name}", self.connection)

    def close(self):
        """Close the connection to the SQLite database."""
        if self.connection:
            self.connection.close()
