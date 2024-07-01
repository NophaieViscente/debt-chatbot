from decouple import Config, RepositoryEnv

# Our modules
from utils.clean_data import DataHandler
from utils.load_data import DataLoader
from utils.sql_handler import DataBaseHandler

# Start objects to data handle
data_handler = DataHandler()
data_loader = DataLoader()

# Appoint to enviroment variables
config = Config(RepositoryEnv("/home/nophaieviscente/my-projects/debt-chatbot/.env"))
RAW_DATA_PATH = config("RAW_DATA_PATH")
DATABASE = config("DATABASE")

# Load data from csv
df_costumers = data_loader.load_csv_data(path=RAW_DATA_PATH + "data-debt.csv")


# Clean and adjust data from csv
df_costumers = data_handler.handle_dataframe_data(dataframe=df_costumers)

# Separate payment options into other dataframe
payment_options = data_handler.separate_data_payment_options(dataframe=df_costumers)

# Drop column that contains payment options data to costumers table
df_costumers = df_costumers.drop(columns="opcoes_pagamento")

# Create database if dont exists
database_handler = DataBaseHandler(DATABASE)
# Connect to database
database_handler.connect()
# Create tables from csv file
database_handler.create_tables()
# Insert costumers table
database_handler.insert_dataframe(df=df_costumers, table_name="customers")
# Insert payment_opetions table
database_handler.insert_dataframe(df=payment_options, table_name="payment_options")
