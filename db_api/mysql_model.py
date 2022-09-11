from .db_models import DBModel
import mysql.connector

from db_api.constants import CREATE_DB_QUERY, CREATE_TABLE_QUERY, SELECT_QUERY, FILTER_PART, PAGINATION_PART, \
    ORDER_PART, INSERT_QUERY


class MySqlModel(DBModel):
    def __init__(self, **kargs):
        self.dbs = {}
        self.user_name = kargs.get("user")
        self.password = kargs.get("password")
        self.host = kargs.get("host")
        self.connection = self.create_connection()

    # @property
    # def connection(self):
    #     return self._connection
    #
    # @connection.setter
    # def connection(self, value):
    #     self._connection = value
    #
    # @connection.deleter
    # def connection(self):
    #     del self._connection

    def create_connection(self, **kargs):
        try:
            db_name = kargs.get("db_name")
            if db_name:
                db_connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user_name,
                    password=self.password,
                    database=db_name
                )
            else:
                db_connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user_name,
                    password=self.password
                )
            return db_connection
        except Exception as e:
            print(f"Creating connection for user: {self.user_name} on host: {self.host} failed due to {e}")

    def create_db(self, db_name):
        try:
            if db_name in self.dbs.keys():
                raise Exception(f"DB {db_name} already exist")
            self.perform_query(CREATE_DB_QUERY.format(db_name))
            new_db_connection = self.create_connection(db_name=db_name)
            self.dbs[db_name] = new_db_connection
        except Exception as e:
            print(f"Failed create db {db_name} due to {e}")

    def create_table(self, db_name: str, table_name: str, columns_dict: dict):
        columns_part = ',\n'.join([f"{col_name} {col_type}" for col_name, col_type in columns_dict.items()])
        query = CREATE_TABLE_QUERY.format(table_name, columns_part)
        connection = self.create_connection(db_name=db_name)
        connection.cursor().execute(query)

    def select_query(self, db_name: str, table_name: str, columns: list[str], filter=None, pagination=None,
                     order=None) -> str:
        query = SELECT_QUERY.format(', '.join(columns), table_name)
        if filter:
            # filter_pattern_name, column, value = filter
            #
            # filter_pattern = FILTERS_DICT[filter_pattern_name]
            # filter_query_part =
            query += FILTER_PART.format(filter)
        if pagination:
            offset, limit = pagination
            query += PAGINATION_PART.format(offset, limit)
        if order:
            column_to_order_by, ase_or_desc = order
            query += ORDER_PART.format(column_to_order_by, ase_or_desc)
        connection = self.dbs.get(db_name)
        if not connection:
            connection = self.create_connection(db_name=db_name)
            self.dbs[db_name] = connection
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            query_result = cursor.fetchall()
        return query_result

    def insert_query(self, db_name: str, table_name: str, columns_values_dict):
        columns_as_str = ', '.join(list(columns_values_dict.keys()))
        values_as_str = ', '.join([str(val) for val in list(columns_values_dict.values())])
        query = INSERT_QUERY.format(table_name, columns_as_str, values_as_str)
        connection = self.dbs.get(db_name)
        if not connection:
            connection = self.create_connection(db_name=db_name)
            self.dbs[db_name] = connection
        connection.cursor(buffered=True).execute(query)
        connection.commit()

    def perform_query(self, query, db_name=None):
        # connection = self.create_connection(db_name=db_name)
        connection = self.connection if not db_name else self.dbs.get(db_name)
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.close()

    @DBModel.update_query
    def update_query(self, **kargs):
        pass

    @DBModel.delete_query
    def delete_query(self, **kargs):
        pass
