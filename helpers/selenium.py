import base64
import time
from selenium.webdriver.common.by import By

def take_screenshot(driver, filename):
    screenshot = driver.get_screenshot_as_base64()
    with open(filename, "wb") as file:
        file.write(base64.b64decode(screenshot))

def scroll_until_element_found(driver, element_id):
    element = None
    while element is None:
        driver.execute_script("window.scrollBy(0, 100);")
        try:
            element = driver.find_element(By.ID, element_id)
        except:
            pass
        time.sleep(0.5) 