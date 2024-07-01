import pandas as pd
import re
from datetime import datetime
import slugify


class DataHandler:

    def __init__(self) -> None:
        pass

    def handle_cpf_cnpj(self, cpf: str) -> str:
        """
        Function to handle CPF that may have lost the leading zero.

        Args :
            - cpf : str : CPF in string format
        Return:
            - cpf : str: CPF with the leading zero if necessary
        """
        try:
            if type(cpf) != str:
                cpf = str(cpf)
            cpf = re.sub(pattern=r"[./-]", repl="", string=cpf)

            if len(cpf) > 0 and len(cpf) == 10:
                return f"0{cpf}"
            return cpf
        except Exception as error:
            return error.args

    def handle_dates(self, date: str) -> datetime:
        """
        Function to handle dates.

        Args:
            - date : str : String with a date in the format DD/MM/YYYY
        Return:
            - date : datetime: Date in datetime format
        """
        try:
            return datetime.strptime(date, "%d/%m/%Y")
        except Exception as error:
            return error.args

    def handle_numbers(self, value: str) -> float:
        """
        Function to handle monetary values.

        Args:
            - value: str : String with the value containing a comma for decimal places.
        Return:
            - value : float: Number in float format

        """
        try:
            return float(re.sub(pattern=r",", repl=".", string=value))
        except Exception as error:
            if type(value) == float or type(value) == int:
                return float(value)
            return error.args

    def handle_dataframe_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Handles data in a pandas DataFrame by applying specific functions to columns based on their names.

        Args:
            dataframe (pd.DataFrame): DataFrame to be handled.

        Returns:
            pd.DataFrame: DataFrame with handled data.
        """
        functions = {
            "cpf": self.handle_cpf_cnpj,
            "data": self.handle_dates,
            "valor": self.handle_numbers,
        }
        dataframe.columns = [
            slugify.slugify(text=col, separator="_") for col in dataframe.columns
        ]
        for column in dataframe.columns:

            split_column = column.split("_")[0]

            handle_function = functions.get(split_column, None)

            if handle_function:
                dataframe[column] = dataframe[column].apply(handle_function)
            else:
                continue

        return dataframe

    def separate_data_payment_options(
        self, dataframe: pd.DataFrame, cols: list = ["cpf_cnpj", "opcoes_pagamento"]
    ) -> pd.DataFrame:

        filtered_data = dataframe[cols]

        payment_options = pd.DataFrame()
        for _, row in filtered_data.iterrows():

            payment_options_row = eval(row["opcoes_pagamento"])
            cpf_cnpj = row["cpf_cnpj"]
            data = pd.DataFrame(payment_options_row)
            data["cpf_cnpj"] = cpf_cnpj

            payment_options = pd.concat([payment_options, data], axis=0)
        payment_options["data_primeiro_boleto"] = payment_options[
            "data_primeiro_boleto"
        ].apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))
        payment_options["valor_parcela"] = payment_options["valor_parcela"].apply(
            lambda x: float(x.replace(",", "."))
        )
        payment_options["valor_desconto"] = payment_options["valor_desconto"].apply(
            lambda x: float(x.replace(",", "."))
        )
        payment_options["valor_negociado"] = payment_options["valor_negociado"].apply(
            lambda x: float(x.replace(",", "."))
        )
        return payment_options
