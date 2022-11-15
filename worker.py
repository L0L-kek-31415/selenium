import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


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
        title = self.get_attr(By.CLASS_NAME, "_eYtD2XCVieq6emjKBH3m")
        subreddit = self.get_attr(By.CLASS_NAME, "_2VB8YvVdvxx0h0VGYVrpBX")
        user = self.get_attr(By.CLASS_NAME, "_2tbHP6ZydRpjI44J3syuqC")
        comments = self.get_attr(By.CLASS_NAME, "FHCV02u6Cp2zYL0fhQPsO")
        upvoted = self.get_attr(By.CLASS_NAME, "t4Hq30BDzTeJ85vREX7_M")
        vote = self.get_attr(By.CLASS_NAME, "_1rZYMD_4xY3gRcSS3p8ODO")
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
        time_my = self.get_attr(By.CLASS_NAME, "_2VF2J19pUIMSLJFky-7PEI")
        self.action.move_to_element(time_my).perform()
        time.sleep(0.5)
        time_my = self.get_attr(By.CLASS_NAME, "u6HtAZu8_LKL721-EnKuR")
        if time_my is None:
            time_my = self.get_attr(By.CLASS_NAME, "_2J_zB4R1FH2EjGMkQjedwc")
        return time_my

    def get_attr(self, by, value):
        try:
            result = self.driver.find_element(by, value)
            return result.text
        except NoSuchElementException:
            return None
