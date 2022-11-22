from db.base_db_class import BaseDBService


class TxtDB(BaseDBService):
    def __init__(self):
        self.file_name = "db.txt"

    def __enter__(self):
        self.file = open(self.file_name, "a+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def add_post(self, post):
        self.file.write(str(post))

    def return_all(self):
        self.file.seek(0)
        return self.file.read()
