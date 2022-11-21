from abc import ABC, abstractmethod


class BaseDBService(ABC):
    @abstractmethod
    def add_post(self, post):
        pass

    @abstractmethod
    def return_all(self):
        pass
