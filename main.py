import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from worker import worker


def load_posts(pages, driver, pool, q):
    while pages > 0:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_set = driver.find_elements(By.CLASS_NAME, "_1oQyIsiPHYt6nx7VOmd1sz")
        for i in new_set:
            if pages <= 0:
                break
            try:
                link = i.find_element(
                    By.CLASS_NAME, "SQnoC3ObvgnGjWt90zD9Z"
                ).get_attribute("href")
            except:
                print("pass")
            else:
                pages -= 1
                pool.apply_async(
                    worker,
                    (
                        link,
                        q,
                    ),
                )


def main(pages, workers):
    driver_location = "./chromedriver"
    driver = webdriver.Chrome(executable_path=driver_location)
    driver.get("https://reddit.com/top")
    m = multiprocessing.Manager()
    q = m.Queue()
    pool = multiprocessing.Pool(workers)

    load_posts(pages, driver, pool, q)
    driver.close()
    pool.close()
    pool.join()
    while q.empty() is False:
        print(q.get())


if __name__ == "__main__":
    main(2, 2)
