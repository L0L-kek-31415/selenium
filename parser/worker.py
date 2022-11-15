import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from parser.class_names import ClassNames


class Worker:
    def __init__(self, link, queue):
        self.link = link
        self.queue = queue
        self.driver_location = "./chromedriver"
        self.driver = webdriver.Chrome(executable_path=self.driver_location)
        self.action = ActionChains(self.driver)

    def start(self):
        self.driver.get(self.link)
        data = self.get_data()
        self.queue.put(data)
        self.driver.close()

    def get_data(self):
        title = self.get_attr(By.CLASS_NAME, ClassNames.title)
        subreddit = self.get_attr(By.CLASS_NAME, ClassNames.subreddit)
        user = self.get_attr(By.CLASS_NAME, ClassNames.user)
        comments = self.get_attr(By.CLASS_NAME, ClassNames.comments)
        upvoted = self.get_attr(By.CLASS_NAME, ClassNames.upvoted)
        vote = self.get_attr(By.CLASS_NAME, ClassNames.vote)
        time_my = self.get_time()
        data = {
            "title": title,
            "user": user,
            "subreddit": subreddit,
            "vote": vote,
            "comments": comments.split()[0],
            "upvoted": upvoted.split()[0],
            "time": time_my,
        }
        return data

    def get_time(self):
        time_my = self.get_attr(By.CLASS_NAME, ClassNames.time_object, True)
        self.action.move_to_element(time_my).perform()
        time.sleep(0.5)
        time_my = self.get_attr(By.CLASS_NAME, ClassNames.time_all)
        return time_my

    def get_attr(self, by, value, text=False):
        try:
            result = self.driver.find_element(by, value)
            if text:
                return result
            else:
                return result.text
        except NoSuchElementException:
            return None
