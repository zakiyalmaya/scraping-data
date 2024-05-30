from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import pandas as pd
import time

# Set up Chrome options and service
opt = webdriver.ChromeOptions()
opt.add_argument('--headless=new')
opt.add_argument('log-level=3')

service = Service('chromedriver.exe')

# Launch Chrome browser
driver = webdriver.Chrome(service=service, options=opt)

# Navigate to the initial page
url = 'https://reviews.femaledaily.com/products/treatment/serum-essence?brand=&order=popular&page=1'
driver.get(url)
time.sleep(5)  # Wait for the page to load

# Set window size for the screenshot
driver.set_window_size(1920, 1080)
driver.save_screenshot('screenshot.png')

# Initialize a list to store the ratings
serum_essence_ratings = []

# Function to scrape ratings from the current page
def scrape_ratings():
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    for data in soup.find_all('a', class_='jsx-3793288165 product-card product-brand full-line'):
        brand = data.find('p', class_='jsx-1897565266 fd-body-md-bold text-ellipsis word-break').get_text(strip=True)
        product = data.find('p', class_='jsx-1897565266 fd-body-md-regular text-ellipsis two-line word-break').get_text(strip=True)
        image = data.find('img')['src']
        rating = data.find('span', class_='jsx-1897565266 fd-body-sm-regular').get_text(strip=True) + "/5"
        total_reviewer = data.find('span', class_='jsx-1897565266 fd-body-sm-regular grey').get_text(strip=True).replace('(', '').replace(')', '')
        link_review = data.get('href')
        serum_essence_ratings.append({'Brand': brand, 'Product': product, 'Image': image, 'Rating': rating, 'Total Reviewer': total_reviewer, 'Link Review': link_review})

# Click the "Load More" button 3 times
for _ in range(3):
    try:
        # Wait for the "Load More" button to be clickable and click it
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-load-more'))
        )
        load_more_button.click()
        time.sleep(5)  # Wait for the new content to load
        # Scrape ratings from the newly loaded content
        scrape_ratings()
    except Exception as e:
        # If no "Load More" button is found or another exception occurs, print the error and break the loop
        print(f"Error encountered: {e}")
        break

# Close the browser
driver.close()

# Create a DataFrame and save the data to a CSV file
df = pd.DataFrame(serum_essence_ratings)
df.to_csv('serum_essence_ratings.csv', index=False)

# Optional: Display the DataFrame for verification
print(df)
