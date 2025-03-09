import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from helpers.getSizes import getSizes 

def main():
    # Set up the WebDriver
     # Configure options for the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")  # Opens the browser in maximized mode
    # Remove incognito by not using `options.add_argument("--incognito")`

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.faire.com/?signIn=1")  # Replace with the login page URL

# Perform the login steps
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))  # Adjust the locator
    )
    email_input.send_keys("alyssanicole226@gmail.com")  # Replace with your actual email
    email_input.send_keys(Keys.RETURN)

    # Wait for the next step to appear (e.g., password input)
    time.sleep(2)  # Adjust this sleep if needed

    # Step 2: Enter Password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))  # Adjust the locator
    )
    password_input.send_keys("618Nicole3351850")  # Replace with your actual password
    password_input.send_keys(Keys.RETURN)

    # Wait for login to complete (time should be adjusted based on the actual site)
    time.sleep(5)  # Wait for login to complete and page to load

    # Navigate to the page
    url = 'https://www.faire.com/product/p_v9yxyrk6d8?bRefP=p_gu4vhntq38&refB=1'
    # url = 'https://www.faire.com/product/p_axvqddvhs9?bRefP=p_gu4vhntq38&refB=1'
    # url = 'https://www.faire.com/product/p_gu4vhntq38?impressionId=1740449095_3t7zt5rcchqzgy9'
    driver.get(url)

    # Wait for page to load completely
    time.sleep(10)  # Adjust according to the website's load time')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    # Extract product images
    image_sections = soup.find_all('picture')
    for image_section in image_sections:
        img = image_section.find('img')
        img_src = img['src']
        img_alt = img['alt']
        print(f'Image URL: {img_src}')
        print(f'Image Alt: {img_alt}')

    # Extract product name
    product_name = soup.find('h1', {'data-test-id': 'product-name'}).text
    print(f'Product Name: {product_name}')

    sizes = getSizes(soup)
    print(f'Sizes: {sizes}')

    product_price_section = soup.find('div', {'data-test-id': 'product-price'})
    if product_price_section:
        msrp_tag = product_price_section.find('p', {'data-test-id': 'product-tile-msrp'})
        if msrp_tag:
            spans = msrp_tag.find_all('span')

            if len(spans) >= 2:
                price = spans[0].text.strip()
                msrp = spans[1].text.strip()
                print(f'Price: {price}')
                print(f'MSRP: {msrp}')
            else:
                print("Not enough span elements found.")

    # Extract other relevant details as needed
    # Continue with more extraction based on the HTML structure

if __name__ == "__main__":
    main()