from abc import ABC, abstractmethod


class BaseDBService(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def add_post(self, post):
        pass

    @abstractmethod
    def return_all(self):
        pass
