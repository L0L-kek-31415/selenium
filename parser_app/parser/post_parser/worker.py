import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from parser.class_names import ClassNames
from parser.driver import DriverService
from parser.rabbit.producer import BaseProducer


class Worker(DriverService):
    def __init__(self, link):
        super().__init__()
        self.link = link
        self.action = ActionChains(self.driver)
        self.producer = BaseProducer("syka")
        self.start()

    def start(self):
        print("worker started")
        self.driver.get(self.link)
        data = self.get_data()
        print(data)
        # self.close_driver()
        # self.queue.put(data)

    def get_data(self):
        title = self.get_attr(By.CLASS_NAME, ClassNames.TITLE)
        subreddit = self.get_attr(By.CLASS_NAME, ClassNames.SUBREDDIT)
        self.producer.publish(str(subreddit))
        self.producer.close()
        user = self.get_attr(By.CLASS_NAME, ClassNames.USER)
        comments = self.get_attr(By.CLASS_NAME, ClassNames.COMMENTS)
        upvoted = self.get_attr(By.CLASS_NAME, ClassNames.UPVOTED)
        vote = self.get_attr(By.CLASS_NAME, ClassNames.VOTE)
        time_my = self.get_time()
        data = {
            "title": title,
            "user": user,
            "subreddit": subreddit,
            "vote": str(self.get_num(vote)),
            "comments": str(self.get_num(comments)),
            "upvoted": str(self.get_num(upvoted)),
            "time": str(time_my),
        }
        return data

    def get_time(self):
        time_my = self.get_attr(By.CLASS_NAME, ClassNames.TIME_OBJECT, True)
        self.action.move_to_element(time_my).perform()
        time.sleep(0.5)
        time_my = self.get_attr(By.CLASS_NAME, ClassNames.TIME_ALL)
        return time_my

    @staticmethod
    def get_num(data):
        if data is not None:
            return Worker.replace_k(data.split()[0].replace("%", ""))
        else:
            return 0

    @staticmethod
    def replace_k(data):
        if data.find("k") != -1:
            data = int(float(data.replace("k", "")) * 1000)
        return data
