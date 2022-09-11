from dataclasses import dataclass
import pandas as pd

from db_api.mysql_model import MySqlModel


API_KEY = "awojxDd9RxR3XGm6FVt4sSJ1Iflz4bGR"
DB_HOST = '127.0.0.1'
DB_USER = "root"
DB_PASSWORD = "1234"
DATE_COL = "Date_"
CURRENCY_COL = "Currency"
NAME_COL = "Name"


def remove_spaces_form_cols_names(billing_df):
    billing_df.columns = billing_df.columns.str.replace(' ', '_')
    return billing_df


def modify_date_for_db(date: str) -> str:
    day, month, year = date.split("/")
    return f"DATE('{year}-{month}-{day}')"


def modify_all_dates_for_db(billing_df):
    billing_df[DATE_COL] = billing_df[DATE_COL].apply(modify_date_for_db)
    return billing_df


def modify_all_varchars_values_for_db(billing_df):
    billing_df[CURRENCY_COL] = billing_df[CURRENCY_COL].apply(lambda x: f"'{x}'")
    billing_df[NAME_COL] = billing_df[NAME_COL].apply(lambda x: f"'{x}'")
    return billing_df


def prepare_data_for_db(path):
    billing_df = pd.read_csv(path)
    billing_df_for_db = remove_spaces_form_cols_names(billing_df)
    billing_df_for_db = modify_all_dates_for_db(billing_df_for_db)
    billing_df_for_db = modify_all_varchars_values_for_db(billing_df_for_db)
    return billing_df_for_db


def insert_df_to_table(transforemd_df, db_name, table_name):
    db_model = MySqlModel(user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
    for index, row in transforemd_df.iterrows():
        col_dict = row.to_dict()
        db_model.insert_query(db_name, table_name, col_dict)


if __name__ == '__main__':
    path = '../spot_billings.csv'
    prepared_for_db_df = prepare_data_for_db(path)
    insert_df_to_table(prepared_for_db_df, "SPOT_DB", "BILLING_TABLE")



