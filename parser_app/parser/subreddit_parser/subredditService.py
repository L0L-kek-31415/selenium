from selenium.webdriver.common.by import By

from parser.class_names import ClassNames
from parser.driver import DriverService


class SubredditService(DriverService):
    def __init__(self, link):
        super().__init__()
        self.name = link
        self.link = "https://www.reddit.com/" + link
        self.start()

    def start(self):
        self.driver.get(self.link)
        data = self.get_data()
        print(data)

    def get_data(self):
        name = self.name
        members = self.get_attr(By.CLASS_NAME, ClassNames.MEMBERS)
        ranked_by_size = self.get_attr(By.CLASS_NAME, ClassNames.RANKED)
        description = self.get_attr(By.CLASS_NAME, ClassNames.DESCRIPTION)
        created = self.get_attr(By.CLASS_NAME, ClassNames.CREATED)
        data = {
            "name": name,
            "members": self.get_num(members),
            "ranked_by_size": self.get_num(ranked_by_size),
            "description": description,
            "created": " ".join(created.split()[1:]),
        }
        return data

    def add_to_db(self, data):
        pass

    @staticmethod
    def get_num(data):
        if data is not None:
            data = data.split()[0].replace("#", "")
            return SubredditService.replace_k_and_m(data)
        else:
            return 0

    @staticmethod
    def replace_k_and_m(data):
        if data.find("k") != -1:
            data = int(float(data.replace("k", "")) * 1000)
        elif data.find("m") != -1:
            data = int(float(data.replace("m", "")) * 1000000)
        return data
