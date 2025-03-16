from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless=new")  # Use modern headless mode
options.add_argument("--disable-gpu")  # Prevent rendering issues
options.add_argument("--window-size=1920x1080")  # Set a standard window size
options.add_argument("--log-level=3")  # Reduce logging
options.add_argument("--ignore-certificate-errors")  # Ignore SSL issues
options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues in Linux
options.add_argument("--no-sandbox")  # Needed for some environments like Docker

driver = webdriver.Chrome(options=options)
driver.get("https://www.metatft.com/augments")

try:
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
    # Close the WebDriver
    driver.quit()