from client.apilayer_clinet import get_currency_by_date
from client.spot_client import prepare_data_for_db, insert_df_to_table
from db_api.mysql_model import MySqlModel
from python_q.python_qestions import longet_uniuqe_substring

if __name__ == '__main__':
    # Task1: using Mysql model to create DB and table, later on with Task 2 will use more functionality

    db_obj = MySqlModel(user="root", host="127.0.0.1", password="1234")
    db_obj.create_db("SPOT_DB")
    db_obj.create_table(db_name="SPOT_DB", table_name="BILLING_TABLE",
                        columns_dict={"Date_": "DATE",
                                      "Bill_ID": "INT",
                                      "Currency": "varchar(3)",
                                      "Name": "varchar(20)",
                                      "Product1_revenue": "FLOAT",
                                      "Product2_revenue": "FLOAT"})

    # Task2: transformed the XL to DB form and use the Mysql model from bd_models package

    path = '../spot_billings.csv'
    prepared_for_db_df = prepare_data_for_db(path)
    insert_df_to_table(prepared_for_db_df, "SPOT_DB", "BILLING_TABLE")

    # Task3: insert rates form api layer to new RATES table:

    db_obj.create_table(db_name="SPOT_DB", table_name="RATES",
                        columns_dict={"ILS": "FLOAT", "GBP": "FLOAT", "EUR": "FLOAT"})

    rates_dict = get_currency_by_date(date="2021-01-01", symbols="ILS,EUR,GBP", base="USD")

    db_obj.insert_query(db_name="SPOT_DB", table_name="RATES", columns_values_dict=rates_dict)

    # Task4: flatten list of lists:

    list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flatten_list = [x for l in list_of_lists for x in l]

    print(f"flatten list of {list_of_lists} is {flatten_list}")

    # Task5: logenst substring with no double letter:

    print(f"longest uniuqe substring for {'abcabcbb'} is {longet_uniuqe_substring('abcabcbb')}")
    print(f"longest uniuqe substring for {'bbbb'} is {longet_uniuqe_substring('bbbb')}")
    print(f"longest uniuqe substring for {'pwwkew'} is {longet_uniuqe_substring('pwwkew')}")