import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://tftacademy.com/tierlist/comps"

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Sending a GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Dictionary to store links grouped by tier
    tier_links = {}
    tier_ids = ["tier-S", "tier-A", "tier-B", "tier-C", "tier-X"]
    
    for tier in tier_ids:
        tier_div = soup.find("div", id=tier)
        if tier_div:
            tier_links[tier] = [link.get("href") for link in tier_div.find_all("a", href=True)]
else:
    print(f"Failed to retrieve page, status code: {response.status_code}")

comp_info = {
    "tier": None,
    "name": None,
    "playstyle": None,
    "augments": None,
    "augment-priority": None,
    "tips": None,
    "units": [{"name": None, "items": None, "star-level": None}],
    "early-comp": [{"name": None, "items": None, "star-level": None}],
    "item-priority": [],
    "positioning": None,
    "stage2-tips": None,
    "stage3-tips": None,
    "stage4-tips": None,
}

for key, item in tier_links.items():
    for link in item:
        response = requests.get("https://tftacademy.com" + link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            comp_info["tier"] = key
            comp_info["name"] = soup.find("h1", class_="z-0 text-balance text-lg font-bold uppercase leading-5").text.strip()
            comp_info["playstyle"] = soup.find("div", class_="flex flex-row items-center justify-center gap-x-1 pt-1 text-xs font-bold uppercase").text.strip()
            smooth_images = soup.find_all("div", class_="smooth h-[4.5rem] w-[4.5rem] cursor-pointer px-0 hover:scale-105")
            smooth_alts = [img.get("alt") for div in smooth_images for img in div.find_all("img") if img.get("alt")]
            comp_info['augments'] = smooth_alts
            aug_priority = soup.find_all("div", class_="text-sm font-semibold text-white")
            aug_priority_text = [div.text.strip() for div in aug_priority]
            comp_info['augment-priority'] = aug_priority_text
            comp_info['tips'] = soup.find("div", class_="relative mb-4 h-fit w-full text-pretty break-words rounded-[40px] border-2 border-[#064696] px-7 py-7 text-center font-semibold normal-case").text.strip()

            # Find the div with the specified class
            stage2_div = soup.find_all("div", class_="mb-4 border-b-2 border-[#064696] px-4 py-1 text-xl")
            for i in range(len(stage2_div)):
                if i == 0:
                    stage2_div_text = stage2_div[i].find_next("h2")
                    comp_info['stage2-tips'] = stage2_div_text.text.strip()
                elif i == 1:
                    stage2_div_text = stage2_div[i].find_next("h2")
                    comp_info['stage3-tips'] = stage2_div_text.text.strip()
                elif i == 2:
                    stage2_div_text = stage2_div[i].find_next("h2")
                    comp_info['stage4-tips'] = stage2_div_text.text.strip()

            comp_info['units'] = None
            comp_info['early-comp'] = None
            comp_info['item-priority'] = None
            comp_info['positioning'] = None
            print(comp_info)
            
            






