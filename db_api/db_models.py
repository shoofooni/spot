from abc import ABC, abstractmethod


class DBModel(ABC):
    # @abstractmethod
    # def __init__(self, **kargs):
    #     pass

    @abstractmethod
    def create_connection(self, **kargs):
        pass

    @abstractmethod
    def create_db(self, **kargs):
        pass

    @abstractmethod
    def create_table(self, **kargs):
        pass

    @abstractmethod
    def perform_query(self, **kargs):
        pass

    @abstractmethod
    def insert_query(self, **kargs):
        pass

    @abstractmethod
    def select_query(self, **kargs):
        pass

    @abstractmethod
    def update_query(self, **kargs):
        pass

    @abstractmethod
    def delete_query(self, **kargs):
        pass
