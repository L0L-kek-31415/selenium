import time
from selenium.webdriver.common.by import By

from parser.class_names import ClassNames
from parser.driver import DriverService
from parser.link_parser.producer import Producer


class SiteService(DriverService):
    def __init__(self, pages, link, database):
        super().__init__()
        self.pages = pages
        self.link = link
        self.database = database
        self.producer = Producer()

    def start(self):
        self.driver.get(self.link)
        self.posts()
        self.close_driver()

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
                body = str(link)
                self.producer.publish(body)

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
