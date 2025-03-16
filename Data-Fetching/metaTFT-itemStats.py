from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.add_argument("--headless=new")  # Use modern headless mode
options.add_argument("--disable-gpu")  # Prevent rendering issues
options.add_argument("--window-size=1920x1080")  # Set a standard window size
options.add_argument("--log-level=3")  # Reduce logging
options.add_argument("--ignore-certificate-errors")  # Ignore SSL issues
options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues in Linux
options.add_argument("--no-sandbox")  # Needed for some environments like Docker

links = ["https://www.metatft.com/items/normal", "https://www.metatft.com/items/artifact", "https://www.metatft.com/items/support", "https://www.metatft.com/items/radiant", "https://www.metatft.com/items/emblem"]
# links = ["https://www.metatft.com/items/artifact"]
all_items = {}

for link in links:

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        data = {}

        # Wait until the table is present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "StatTableContainer")))

        # Ensure elements are fully loaded
        time.sleep(2)

        # Find the table container
        table_container = driver.find_element(By.CLASS_NAME, "StatTableContainer")
        rows = table_container.find_elements(By.TAG_NAME, "tr")
        
        for row in rows:
            try:
                # Extract StatTierBadge text
                stat_tier_badge = row.find_element(By.CLASS_NAME, "StatTierBadge").text.strip()
                
                # Extract StatLink text
                stat_link = row.find_element(By.CLASS_NAME, "StatLink").text.strip()
                print(stat_tier_badge, stat_link)
                
                # Store data in dictionary
                if stat_tier_badge not in data:
                    data[stat_tier_badge] = []
                
                data[stat_tier_badge].append(stat_link)
            except:
                continue  # Skip row if elements are missing

        print(data)

        # Scroll to load all table rows
        actions = ActionChains(driver)

        for _ in range(3):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.5)
        
            # Find the table container
            table_container = driver.find_element(By.CLASS_NAME, "StatTableContainer")
            rows = table_container.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                try:
                    # Extract StatTierBadge text
                    stat_tier_badge = row.find_element(By.CLASS_NAME, "StatTierBadge").text.strip()
                    
                    # Extract StatLink text
                    stat_link = row.find_element(By.CLASS_NAME, "StatLink").text.strip()
                    print(stat_tier_badge, stat_link)
                    
                    # Store data in dictionary
                    if stat_tier_badge not in data:
                        data[stat_tier_badge] = []
                    
                    data[stat_tier_badge].append(stat_link)
                except:
                    continue  # Skip row if elements are missing
            
            print(data)

        for key, value in data.items():
            data[key] = list(set(value))
        
        print(data)

        all_items.update({link[30:]: data})
        
    finally:
        # Close the WebDriver
        driver.quit()

print(all_items)
