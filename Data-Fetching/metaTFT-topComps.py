from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# Configure Chrome options
options = Options()
options.add_argument("--headless=new")  # Modern headless mode
options.add_argument("--disable-gpu")  
options.add_argument("--window-size=1920x1080")  
options.add_argument("--log-level=3")  
options.add_argument("--ignore-certificate-errors")  
options.add_argument("--disable-dev-shm-usage")  
options.add_argument("--no-sandbox")  

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.metatft.com/comps")

    # Wait for main container to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "CompRow"))
    )

    data = []

    # Find all compositions
    comp_divs = driver.find_elements(By.CLASS_NAME, "CompRow")

    for comp in comp_divs:
        comp_data = {}

        # Extract Tier Badge
        try:
            tier_badge = comp.find_element(By.CLASS_NAME, "CompRowTierBadge").text.strip()
        except Exception:
            tier_badge = "N/A"
        comp_data["tier"] = tier_badge

        # Extract Composition Name
        try:
            comp_name = comp.find_element(By.CLASS_NAME, "Comp_Title").text.strip()
        except Exception:
            comp_name = "Unknown"
        comp_data["name"] = comp_name

        # Extract Tags
        try:
            comp_tags = [tag.text.strip() for tag in comp.find_elements(By.CLASS_NAME, "CompRowTag")]
        except Exception:
            comp_tags = []
        comp_data["tags"] = comp_tags

        # Extract Units
        try:
            units_container = comp.find_element(By.CLASS_NAME, "UnitsContainer")
            units = units_container.find_elements(By.CLASS_NAME, "Unit_Wrapper")
        except Exception:
            units = []
        comp_data["units"] = []

        for unit in units:
            unit_data = {}

            # Extract Unit Name
            try:
                unit_data["name"] = unit.find_element(By.CLASS_NAME, "UnitNames").text.strip()
            except Exception:
                unit_data["name"] = "Unknown"

            # Extract Unit Star Level (if image exists)
            try:
                stars_div = unit.find_element(By.CLASS_NAME, "stars_div")
                star_images = stars_div.find_elements(By.TAG_NAME, "img")
                if star_images:
                    unit_data["stars"] = star_images[0].get_attribute("alt").strip()
            except Exception:
                unit_data["stars"] = "Unknown"

            # Extract Items
            try:
                item_div = unit.find_element(By.CLASS_NAME, "ItemsContainer_Inline")
                items = item_div.find_elements(By.CLASS_NAME, "display-contents")
                unit_data["items"] = [
                    item.find_element(By.TAG_NAME, "img").get_attribute("alt").strip()
                    for item in items if len(item.find_elements(By.TAG_NAME, "img")) > 0
                ]
            except Exception:
                unit_data["items"] = []

            comp_data["units"].append(unit_data)

        if comp_data in data:
            break
        data.append(comp_data)

    # Scroll to load all table rows
    actions = ActionChains(driver)

    for _ in range(10):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)

        # Find all compositions
        comp_divs = driver.find_elements(By.CLASS_NAME, "CompRow")

        for comp in comp_divs:
            comp_data = {}

            # Extract Tier Badge
            try:
                tier_badge = comp.find_element(By.CLASS_NAME, "CompRowTierBadge").text.strip()
            except Exception:
                tier_badge = "N/A"
            comp_data["tier"] = tier_badge

            # Extract Composition Name
            try:
                comp_name = comp.find_element(By.CLASS_NAME, "Comp_Title").text.strip()
            except Exception:
                comp_name = "Unknown"
            comp_data["name"] = comp_name

            # Extract Tags
            try:
                comp_tags = [tag.text.strip() for tag in comp.find_elements(By.CLASS_NAME, "CompRowTag")]
            except Exception:
                comp_tags = []
            comp_data["tags"] = comp_tags

            # Extract Units
            try:
                units_container = comp.find_element(By.CLASS_NAME, "UnitsContainer")
                units = units_container.find_elements(By.CLASS_NAME, "Unit_Wrapper")
            except Exception:
                units = []
            comp_data["units"] = []

            for unit in units:
                unit_data = {}

                # Extract Unit Name
                try:
                    unit_data["name"] = unit.find_element(By.CLASS_NAME, "UnitNames").text.strip()
                except Exception:
                    unit_data["name"] = "Unknown"

                # Extract Unit Star Level (if image exists)
                try:
                    stars_div = unit.find_element(By.CLASS_NAME, "stars_div")
                    star_images = stars_div.find_elements(By.TAG_NAME, "img")
                    if star_images:
                        unit_data["stars"] = star_images[0].get_attribute("alt").strip()
                except Exception:
                    unit_data["stars"] = "Unknown"

                # Extract Items
                try:
                    item_div = unit.find_element(By.CLASS_NAME, "ItemsContainer_Inline")
                    items = item_div.find_elements(By.CLASS_NAME, "display-contents")
                    unit_data["items"] = [
                        item.find_element(By.TAG_NAME, "img").get_attribute("alt").strip()
                        for item in items if len(item.find_elements(By.TAG_NAME, "img")) > 0
                    ]
                except Exception:
                    unit_data["items"] = []

                comp_data["units"].append(unit_data)
            
            if comp_data not in data:
                data.append(comp_data)
                print(comp_data)
            
            data_flag = {
                "tier": "",
                "name": "Unknown",
                "tags": [],
                "units": [
                    {
                        "name": "Unknown",
                        "stars": "Unknown",
                        "items": []
                    }
                ]
            }

            if data_flag == comp_data:
                break

    # Print collected data
    import json
    print(json.dumps(data, indent=4))

finally:
    driver.quit()
