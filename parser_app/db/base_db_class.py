from abc import ABC, abstractmethod


class BaseDBService(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def add_post(self, post):
        pass

    @abstractmethod
    def return_all(self):
        pass
