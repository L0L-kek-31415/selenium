import multiprocessing
import time
from selenium.webdriver.common.by import By

from parser.class_names import ClassNames
from parser.db.mongodb import MongoService
from parser.db.postgres import PostgresService
from parser.db.txt_db import TxtDB
from parser.driver import DriverService
from parser.worker import Worker


class SiteService(DriverService):
    def __init__(self, pages, workers, link, database):
        super().__init__()
        self.pages = pages
        self.workers = workers
        self.link = link
        self.database = database
        self.manager = multiprocessing.Manager()
        self.queue = self.manager.Queue()
        self.pool = multiprocessing.Pool(self.workers)

    def start(self):
        self.driver.get(self.link)
        self.posts()
        self.close_driver()
        self.pool.close()
        self.pool.join()
        self.add_data_in_db()

    def add_data_in_db(self):
        databases = {
            "mongo": MongoService,
            "pg": PostgresService,
            "txt": TxtDB,
        }
        try:
            database = databases[self.database]
        except KeyError:
            database = databases["txt"]
        with database() as db:
            while self.queue.empty() is False:
                post = self.queue.get()
                db.add_post(post)
            print(db.return_all())

    def posts(self):
        while self.pages > 0:
            script = "window.scrollTo(0, document.body.scrollHeight);"
            self.driver.execute_script(script)
            time.sleep(1)
            new_posts = self.driver.find_elements(
                By.CLASS_NAME,
                ClassNames.POST,
            )
            self.post_to_worker(new_posts)

    def post_to_worker(self, new_posts):
        for post in new_posts:
            if self.pages <= 0:
                break
            link = self.get_post_link(post)
            if link:
                self.pages -= 1
                self.pool.apply_async(Worker, (link, self.queue))

    def get_post_link(self, post):
        link = self.get_attr(
            By.CLASS_NAME,
            ClassNames.LINK,
            text=True,
            driver=post,
        )
        if link:
            link = link.get_attribute("href")
        return link
