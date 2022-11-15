import multiprocessing
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from worker import Worker


class SiteService:
    def __init__(self, pages, workers, link):
        self.pages = pages
        self.workers = workers
        self.link = link
        self.manager = multiprocessing.Manager()
        self.queue = self.manager.Queue()
        self.pool = multiprocessing.Pool(self.workers)
        self.driver_location = "./chromedriver"
        self.driver = webdriver.Chrome(executable_path=self.driver_location)

    def start(self):
        self.driver.get(self.link)

        self.load_posts()
        self.driver.close()
        self.pool.close()
        self.pool.join()
        while self.queue.empty() is False:
            print(self.queue.get())

    def load_posts(self):
        counter = self.pages
        while counter > 0:
            script = "window.scrollTo(0, document.body.scrollHeight);"
            self.driver.execute_script(script)
            time.sleep(1)
            post_class = "_1oQyIsiPHYt6nx7VOmd1sz"
            new_posts = self.driver.find_elements(By.CLASS_NAME, post_class)
            for post in new_posts:
                if counter <= 0:
                    break
                try:
                    link = post.find_element(
                        By.CLASS_NAME, "SQnoC3ObvgnGjWt90zD9Z"
                    ).get_attribute("href")
                except NoSuchElementException:
                    print("pass")
                else:
                    counter -= 1
                    worker = Worker(link, self.queue)
                    self.pool.apply_async(worker.start())
