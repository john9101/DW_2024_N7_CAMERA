from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, date
import time
import pandas as pd
import os

class BMDCrawler:

    @staticmethod
    def crawl_cameras_data(config, resource_name, resource_crawl_url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        column_names = config.get("column_names").split(',')

        driver.get(resource_crawl_url)

        last_page = int(driver.find_elements(By.CSS_SELECTOR, "ul.pagination li a").pop().text)
        product_links = []

        for page in range(1, last_page + 1):
            product_items = driver.find_elements(By.CLASS_NAME, "pro-item")

            for product_item in product_items:
                product_links.append(product_item.find_element(By.XPATH,'.//a[contains(@class, "setname")]').get_attribute("href"))

            if page < last_page:
                next_page_button = driver.find_element(By.CSS_SELECTOR, f"ul.pagination li a[href*='p={page + 1}']")
                next_page_button.click()
                time.sleep(2)

        data = []
        for product_link in product_links:
            print(product_link)
            driver.get(product_link)
            product_name = driver.find_element(By.CSS_SELECTOR, '.product-title .page-title a').text
            product_images = driver.find_elements(By.CSS_SELECTOR, '.proImg-list .thumbnails img')
            product_images = [product_image.get_attribute("src") for product_image in product_images]
            product_image_big = driver.find_element(By.CSS_SELECTOR, '.proImg-big .proImg-big-thumb')

            if len(product_images) == 0 and product_image_big:
                product_images.append(product_image_big.find_element(".//a/img").get_attribute("src"))

            try:
                product_id = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Mã sản phẩm")]/following-sibling::td/span[contains(@itemprop,"sku")]').text
            except Exception as e:
                print(e)
                product_id = None

            try:
                product_quantity_in_stock = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Số lượng")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_quantity_in_stock = None

            try:
                product_regular_price = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Giá Bán")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_regular_price = None

            try:
                product_discounted_price = driver.find_element(By.XPATH, '//td[contains(@class,"table-label") and contains(text(),"Giá Khuyến Mãi")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_discounted_price = None

            try:
                product_brand = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Thương hiệu")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_brand = None

            try:
                product_warranty = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Bảo Hành")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_warranty = None

            try:
                product_colors = driver.find_elements(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Màu sắc")]/following-sibling::td/ul[contains(@class,"list-color")]/li')
                product_color_texts = []
                product_color_pics = []
                for product_color in product_colors:
                    try:
                        product_color_text = product_color.find_element(By.XPATH, './/a').text
                        if product_color_text:
                            product_color_texts.append(product_color_text)
                    except:
                        pass

                    try:
                        product_color_pic = product_color.find_element(By.XPATH, './/a/img[contains(@alt, "ColorImage")]').get_attribute("src")
                        if product_color_pic:
                            product_color_pics.append(product_color_pic)
                    except:
                        pass
            except Exception as e:
                print(e)
                product_color_pics = None
                product_color_texts = None

            try:
                product_origin = driver.find_element(By.XPATH,'//td[contains(@class,"table-label") and contains(text(),"Xuất Xứ")]/following-sibling::td').text
            except Exception as e:
                print(e)
                product_origin = None

            column_values = [
                product_id,
                product_name,
                product_quantity_in_stock,
                product_link,
                product_regular_price,
                product_discounted_price,
                product_brand,
                product_warranty,
                product_images if len(product_images) > 0 else None,
                product_origin,
                product_color_texts if len(product_color_texts) > 0 else None,
                product_color_pics if len(product_color_pics) > 0 else None,
                date.today().strftime("%m-%d-%Y")
            ]
            data.append(dict(zip(column_names, column_values)))

        # df = pd.DataFrame(data)
        #
        # extension = config.get("extension")
        # seperator = config.get("seperator")
        # format = config.get("format")
        # source_file_location = config.get("source_file_location")
        # records_count = len(data)
        #
        # file_name = f"{resource_name}_data_{datetime.now().strftime(format)}.{extension}"
        # file_path = f"{source_file_location}/{file_name}"
        # df.to_csv(file_path, index=False, sep=seperator)
        # file_size = os.path.getsize(file_path)
        driver.quit()

        # return file_name, file_size, records_count
        return data

