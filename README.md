# script-crawl-data

## Overview
`script-crawl-data` is a Python-based web scraping project that uses Selenium to automate the extraction of data from web pages. The extracted data is then saved into a CSV file for further analysis.

## Features
- Automates web scraping using Selenium.
- Handles dynamic content and interactions such as closing ads and navigating through pages.
- Saves extracted data into a CSV file with UTF-8 encoding.
- Logs important events and errors for easy debugging.

## Requirements
- Python 3.x
- Selenium 4.5.0

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/script-crawl-data.git
    cd script-crawl-data
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Update the script with the target URL and any necessary configurations.
2. Run the script:
    ```sh
    python script.py
    ```

## Example
Here's an example of how to use the script:

```python
from selenium import webdriver

# Initialize the WebDriver
driver = webdriver.Chrome()

# Navigate to the target URL
driver.get("http://example.com")

# Call the main function to start scraping
main(driver)

# Quit the driver after scraping
driver.quit()