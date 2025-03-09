from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

# Initialize driver as None first
driver = None

try:
    # Initialize the driver with automatic ChromeDriver management and explicit version check
    service = Service(ChromeDriverManager(os_type="win32").install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Load the page
    url = "https://www.metatft.com/augments"
    driver.get(url)
    
    # Wait for content to load (adjust time if needed)
    time.sleep(5)
    
    data = {}
    
    # Find all tier rows
    tierlist_rows = driver.find_elements(By.CLASS_NAME, "TierListRow")
    
    for row in tierlist_rows:
        # Get tier title
        tier_title = row.find_element(By.CLASS_NAME, "TierListTierTitle").text.strip()
        
        # Get augments in this tier
        augments = [augment.text.strip() for augment in row.find_elements(By.CLASS_NAME, "AugmentLabel")]
        
        data[tier_title] = augments

    print(data)

finally:
    # Only quit if driver was successfully initialized
    if driver is not None:
        driver.quit()