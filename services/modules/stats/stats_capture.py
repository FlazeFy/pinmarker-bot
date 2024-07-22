from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium.webdriver.common.action_chains import ActionChains

from helpers.selenium import scroll_until_element_found, take_screenshot

async def get_stats_capture():
    driver = webdriver.Chrome()
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BASEURL = 'http://127.0.0.1:8080'
    # Test Data
    email = 'flazefy'
    password = 'admin'
    screenshot_path = f'Stats_Report_{date}.png'
   
    try:
        # Step 1 : Pengguna membuka halaman login
        driver.get(f'{BASEURL}/LoginController')

        # Step 2 : Pengguna mengisikan form login
        driver.find_element(By.ID, 'username').send_keys(email)
        driver.find_element(By.ID, 'password').send_keys(password)

        # Step 3 : Pengguna menekan button submit
        scroll_until_element_found(driver, 'sign-in')

        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'sign-in'))
        )

        actions = ActionChains(driver)
        actions.move_to_element(sign_in_button).click().perform()

        WebDriverWait(driver, 20).until(EC.url_contains('DashboardController'))
        
        scroll_until_element_found(driver, 'statistic_test_target')
        stats_holder = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'statistic_test_target'))
        )
        actions.move_to_element(stats_holder).perform()

        take_screenshot(driver, screenshot_path)

        return screenshot_path
    except Exception as e:
        print(f'Error occurred: {e}')
    finally:
        driver.quit()