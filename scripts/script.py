import logging
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep

#Note
## Avagre the website will load 25 items per page

# Configure the gobal variable
url = "https://masothue.com/tra-cuu-ma-so-thue-theo-tinh/ho-chi-minh-23"
number_item_per_page = 2
countItemPerPage = 1
page_index = 2
data = {}


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def go_to_website(url):
    # Setup Chrome driver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        logger.info("ChromeDriver initialized successfully.")
        close_ads(driver)

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

    

def click_to_detail(driver):
    global countItemPerPage
    try:
        # Using a more specific XPath based on the 'data-prefetch' attribute
        xpath = f"(//div[@data-prefetch]/h3/a)[{countItemPerPage}]"
        print(xpath)
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        countItemPerPage += 1
        logger.info("Detail button was successfully clicked.")
        close_ads(driver)
        return True
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"An error occurred while clicking to detail: {e}")
        return False

def crawl_data(driver):
    global data
    try:
        source_table_data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-taxinfo"))
        )
        name_company = source_table_data.find_element(By.XPATH, "//main//table[1]/thead/tr").text
        data['Tên'] = name_company
        rows = source_table_data.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) == 2:
                data[columns[0].text] = columns[1].text
        logger.info(f"Crawled data: {data}")
        return data
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"An error occurred while crawling data: {e}")
        driver.quit()

def save_data(data, export_folder='../data', file_name='data.csv'):
    try:
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
        
        # Construct the file path
        file_path = os.path.join(export_folder, file_name)
        
        file_exists = os.path.isfile(file_path)
        
        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            
            # Write the header only if the file does not exist
            if not file_exists:
                writer.writeheader()
            
            # Write the data
            writer.writerow(data)
        
        logger.info(f"Data saved successfully to {file_path}.")
    except Exception as e:
        logger.error(f"An error occurred while saving data: {e}")
        driver.quit()

        

def navigate_back(driver):
    try:
        driver.back()
        close_ads(driver)
        if countItemPerPage == number_item_per_page:
            try:
                go_to_next_page(driver) 
            except Exception as e:
                logger.error(f"An error occurred while navigating to next page: {e}")
                driver.quit()
        logger.info("Navigated back successfully.")
    except Exception as e:
        logger.error(f"An error occurred while navigating back: {e}")
        driver.quit()
    except (TimeoutException, NoSuchElementException) as e:
        driver.quit()
        
def close_ads(driver):
    try:
        ads = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ad_position_box"))
        )
        if ads:
            find_close = driver.find_element(By.ID, "dismiss-button")
            find_close.find_element(By.XPATH, ".//div").click()
            logger.info("Ads was successfully closed.")
    except (TimeoutException, NoSuchElementException) as e:
        logger.info("No ads found or an error occurred while closing ads. Continuing the program.")
    
def go_to_next_page(driver):
    global countItemPerPage, page_index   
    countItemPerPage = 1
    try:
        next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{page_index}']"))
        )
        next_page.click()
        page_index += 1
        logger.info("Navigated to next page successfully.")
        return True
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"An error occurred while navigating to next page: {e}")
        return False

if __name__ == "__main__":
    driver = go_to_website(url)
    if driver:
        try:
            while countItemPerPage <= number_item_per_page:
                logger.info(f"Item per page: {countItemPerPage}") 
                try:
                    click_to_detail(driver)
                    crawl_data(driver)
                    save_data(data)
                    navigate_back(driver)
                    # Add a delay to avoid overwhelming the server
                    sleep(5)
                    
                except (NoSuchElementException, TimeoutException) as e:
                    logger.error(f"An error occurred: {e}")
                    break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        finally:
            driver.quit()
        
