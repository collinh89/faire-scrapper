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
from helpers.facebookHelper import facebookPost


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Replace with the login page URL
    driver.get("https://www.faire.com/?signIn=1")

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.NAME, "email"))  # Adjust the locator
    )
    # Replace with your actual email
    email_input.send_keys("alyssanicole226@gmail.com")
    email_input.send_keys(Keys.RETURN)

    time.sleep(2)  # Adjust this sleep if needed

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.NAME, "password"))  # Adjust the locator
    )
    # Replace with your actual password
    password_input.send_keys("618Nicole3351850")
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login to complete and page to load

    url = 'https://www.faire.com/product/p_v9yxyrk6d8?bRefP=p_gu4vhntq38&refB=1'
    # url = 'https://www.faire.com/product/p_axvqddvhs9?bRefP=p_gu4vhntq38&refB=1'
    # url = 'https://www.faire.com/product/p_gu4vhntq38?impressionId=1740449095_3t7zt5rcchqzgy9'
    driver.get(url)

    # Wait for page to load completely
    time.sleep(10)  # Adjust according to the website's load time')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    product = {
        'product_name': "Product Name",
        'img_urls': [],
        'price': "0",
        'sizes': "0"
    }
    # Extract product images
    image_sections = soup.find_all('picture')
    image_urls = []
    for image_section in image_sections:
        img = image_section.find('img')
        img_src = img['src']
        image_urls.append(img_src)
    product['img_urls'] = image_urls

    # Extract product name
    product_name = soup.find('h1', {'data-test-id': 'product-name'}).text
    product['product_name'] = product_name

    sizes = getSizes(soup)
    product['sizes'] = sizes

    product_price_section = soup.find('div', {'data-test-id': 'product-price'})
    if product_price_section:
        msrp_tag = product_price_section.find(
            'p', {'data-test-id': 'product-tile-msrp'})
        if msrp_tag:
            spans = msrp_tag.find_all('span')

            if len(spans) >= 2:
                price = spans[0].text.strip()
                msrp = spans[1].text.strip()
                product['price'] = msrp
            else:
                print("Not enough span elements found.")

    facebookPost(product)


if __name__ == "__main__":
    main()
