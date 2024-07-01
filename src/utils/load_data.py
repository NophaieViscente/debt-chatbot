import pandas as pd


class DataLoader:

    def __init__(self) -> None:
        pass

    def load_csv_data(self, path: str) -> pd.DataFrame:

        return pd.read_csv(path)

    def load_excel_data(self, path: str) -> pd.DataFrame:
        return pd.read_excel(path)
