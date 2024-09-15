import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from time import sleep
# avagre the website will load 25 items per page
# URL to navigate to
url = "https://masothue.com/tra-cuu-ma-so-thue-theo-tinh/ho-chi-minh-23"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def go_to_website(url):
    # Setup Chrome driver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        logger.info("ChromeDriver initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize ChromeDriver: {e}")
        return None

    try:
        driver.get(url)
        logger.info(f"Navigated to {url} successfully.")
        return driver
    except Exception as e:
        logger.error(f"An error occurred while navigating to {url}: {e}")
        # driver.quit()
        return None

    

def click_to_detail(driver, state):
    if state == 0:
        try:
            # Using a more specific XPath based on the 'data-prefetch' attribute
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-prefetch]/h3/a"))
            )
            element.click()
            logger.info("Detail button was successfully clicked.")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"An error occurred while clicking to detail: {e}")
            return False
    else:
        try:
            # Using a more specific XPath based on the 'data-prefetch' attribute
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-prefetch]/h3/a"))
            )
            element.click()
            logger.info("Detail button was successfully clicked.")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"An error occurred while clicking to detail: {e}")
            return False


# Function to crawl data from the website
def crawl_data(driver):
    try:
        data = {}
        elements = [
            ('Tên', "//main//table[1]/thead/tr"),
            ('MST', "//main//section[1]//table[1]/tbody/tr[1]/td[2]/span"),
            ('Địa chỉ', "//main//section[1]//table[1]/tbody/tr[2]/td[2]/span"),
            ('Người đại diện', "//main//section[1]//table[1]/tbody/tr[3]/td[2]/span"),
            ('Điện thoại', "//main//section[1]//table[1]/tbody/tr[4]/td[2]/span"),
            ('Loại hình DN', "//main//section[1]//table[1]/tbody/tr[7]/td[2]/a"),
            ('Tình trạng', "//main//section[1]//table[1]/tbody/tr[8]/td[2]/a")
        ]
        for label, xpath in elements:
            try:
                # Wait for each element to be present
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                data[label] = element.text
            except (TimeoutException, NoSuchElementException) as e:
                logger.error(f"Error locating element for '{label}': {e}")
                data[label] = None  # Store None if the element is not found
            
        logger.info(f"Crawled data: {data}")
        driver.back()
        
    except Exception as e:
        logger.error(f"An error occurred while crawling data: {e}")
        driver.quit()

def navigate_back_and_go_to_next_page(driver):
    try:
        driver.back()
        logger.info("Navigated back successfully.")
        # Click to next page
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/main/section/div/nav/div/ul/li[2]/a"))
        )
        element.click()
        logger.info("Navigated to next page successfully.")
        return True
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"An error occurred while navigating back or to next page: {e}")
        return False

        

# Example usage
if __name__ == "__main__":
    driver = go_to_website(url)
    if driver:
        click_to_detail(driver)
        crawl_data(driver)
        navigate_back_and_go_to_next_page(driver)
