import time
from datetime import datetime, date

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

class KMCrawler:

    @staticmethod
    def crawl_cameras_data(column_names, resource_crawl_url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        column_names = column_names.split(',')

        driver.get(resource_crawl_url)
        while True:
            try:
                see_more_button = driver.find_element(By.CLASS_NAME, "btn-show-more")
                see_more_button.click()
                time.sleep(2)
            except Exception as e:
                print("No more cameras to load or error:", e)
                break

        product_items = driver.find_elements(By.CSS_SELECTOR, ".item__product.is--s4")
        product_links = [product_item.find_element(By.XPATH,'.//a[contains(@class, "item__name")]').get_attribute("href") for product_item in product_items]
        data = []
        for product_link in product_links:
            print(product_link)
            driver.get(product_link)
            product_name = driver.find_element(By.CSS_SELECTOR, '.product__title .item__title a').text
            product_images = driver.find_elements(By.CSS_SELECTOR, '.product__images .thumbnails img')
            product_images = [product_image.get_attribute("src") for product_image in product_images]

            try:
                product_image_zoom = driver.find_element(By.CSS_SELECTOR, '#imageZoom')
                if len(product_images) == 0 and product_image_zoom:
                    product_images.append(product_image_zoom.find_element(By.XPATH,".//a/img").get_attribute("src"))
            except Exception as e:
                print(e)

            try:
                product_id = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Mã sản phẩm")]/following-sibling::td/span[contains(@itemprop,"sku")]').text
            except Exception as e:
                print(e)
                product_id = None

            try:
                product_regular_price = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Giá bán")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_regular_price = None

            try:
                product_discounted_price = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Giá khuyến mãi")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_discounted_price = None

            try:
                product_brand = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Thương hiệu")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_brand = None

            try:
                product_warranty = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Bảo hành")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_warranty = None

            try:
                product_colors = driver.find_elements(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Màu sắc")]/following-sibling::td/ul[contains(@class,"list-color")]/li')
                product_color_pics = [product_color.find_element(By.XPATH, '//a/img[contains(@class, "img-color")]').get_attribute("src") for product_color in product_colors]
            except Exception as e:
                print(e)
                product_color_pics = None

            try:
                product_origin = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Xuất xứ")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_origin = None

            column_values = [
                product_id,
                product_name,
                product_link,
                product_regular_price,
                product_discounted_price,
                product_brand,
                product_warranty,
                product_images if product_images else None,
                product_origin,
                None,
                product_color_pics if product_color_pics else None,
                date.today().strftime("%m-%d-%Y")
            ]

            data.append(dict(zip(column_names, column_values)))

        driver.quit()

        return data
        # return file_name, file_size, records_count, data