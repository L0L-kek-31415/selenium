import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def worker(link, q):
    driver_location = "./chromedriver"
    driver = webdriver.Chrome(executable_path=driver_location)
    driver.get(link)
    action = ActionChains(driver)
    title = get_attr(driver, By.CLASS_NAME, "_eYtD2XCVieq6emjKBH3m")
    subreddit = get_attr(driver, By.CLASS_NAME, "_2VB8YvVdvxx0h0VGYVrpBX")
    user = get_attr(driver, By.CLASS_NAME, "_2tbHP6ZydRpjI44J3syuqC")
    comments = get_attr(driver, By.CLASS_NAME, "FHCV02u6Cp2zYL0fhQPsO")
    upvoted = get_attr(driver, By.CLASS_NAME, "t4Hq30BDzTeJ85vREX7_M")
    vote = get_attr(driver, By.CLASS_NAME, "_1rZYMD_4xY3gRcSS3p8ODO")
    time_my = driver.find_element(By.CLASS_NAME, "_2VF2J19pUIMSLJFky-7PEI")
    action.move_to_element(time_my).perform()
    time.sleep(1)
    time_my = get_attr(driver, By.CLASS_NAME, "u6HtAZu8_LKL721-EnKuR")

    data = {
        "title": title,
        "user": user,
        "subreddit": subreddit,
        "vote": vote,
        "comments": comments.split()[0],
        "upvoted": upvoted.split()[0],
        "time": time_my,
    }
    q.put(data)
    driver.close()


def get_attr(link, by, value):
    try:
        result = link.find_element(by, value)
        return result.text
    except NoSuchElementException:
        return None
