import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
import time

# Initialize the WebDriver for Chrome
driver = webdriver.Chrome()

# Function for random delays to mimic human behavior
def random_delay(min_time=2, max_time=5):
    delay = random.uniform(min_time, max_time)
    print(f"Waiting for {delay:.2f} seconds.")
    time.sleep(delay)

# Function to simulate human-like typing
def type_like_human(element, text, min_delay=0.05, max_delay=0.15):
    for char in text:
        element.send_keys(char)
        delay = random.uniform(min_delay, max_delay)
        print(f"Typed '{char}', waiting for {delay:.2f} seconds.")
        time.sleep(delay)

# Function for page scrolling to simulate user activity
def scroll_page(driver, scroll_height=400):
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    print(f"Scrolled by {scroll_height} pixels.")
    random_delay()

# Function for simulating mouse movements (basic simulation)
def simulate_mouse_movements(driver):
    actions = webdriver.ActionChains(driver)
    for _ in range(random.randint(2, 5)):
        x_offset = random.randint(0, driver.execute_script("return window.innerWidth"))
        y_offset = random.randint(0, driver.execute_script("return window.innerHeight"))
        actions.move_by_offset(x_offset, y_offset).perform()
        print(f"Moved mouse to ({x_offset}, {y_offset})")
        random_delay(0.5, 2)

# Open the image-to-text website
def open_image_to_text_website():
    try:
        driver.get("https://www.imagetotext.info/image-translator")
        driver.maximize_window()
        print("Opened the Image to Text Translator website successfully.")
        random_delay(3, 5)
        scroll_page(driver, 300)
    except Exception as e:
        print(f"Failed to open the image translator website: {e}")

# Handle cookie acceptance
def handle_translator_cookies():
    try:
        accept_all_div = driver.find_element(By.ID, "accept-choices")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", accept_all_div)
        random_delay(1, 2)
        driver.execute_script("arguments[0].click();", accept_all_div)
        print("Clicked on 'Accept all & visit the site' successfully.")
        random_delay(2, 4)
    except Exception as e:
        print(f"Could not find or click 'Accept all & visit the site': {e}")

# Click on the Image Translator link
def click_image_translator_link():
    try:
        translator_link = driver.find_element(By.XPATH, "//div[@class='nav-links tools']//a[@href='https://www.imagetotext.info/image-translator']")
        simulate_mouse_movements(driver)
        driver.execute_script("arguments[0].scrollIntoView(true);", translator_link)
        random_delay(1, 3)
        driver.execute_script("arguments[0].click();", translator_link)
        print("Clicked on the 'Image Translator' link successfully.")
        random_delay(3, 5)
    except Exception as e:
        print(f"Failed to click on 'Image Translator' link: {e}")

# Change languages to Indonesian (source) and English (destination)
def change_languages():
    try:
        # Source language change
        source_lang_div = driver.find_element(By.CLASS_NAME, "js-toggle-source-lang")
        source_lang_div.click()
        random_delay(1, 2)
        search_field = driver.find_element(By.ID, "js-search-slang")
        type_like_human(search_field, "Indonesian")
        random_delay(1, 2)
        indonesian_option = driver.find_element(By.XPATH, "//div[@data-slang='id' and contains(@class, 'source-lang-item')]")
        indonesian_option.click()
        print("Changed source language to Indonesian.")
        random_delay(2, 3)

        # Destination language change
        dest_lang_div = driver.find_element(By.CLASS_NAME, "js-toggle-dest-lang")
        dest_lang_div.click()
        random_delay(1, 2)
        search_field_dest = driver.find_element(By.ID, "js-search-dlang")
        type_like_human(search_field_dest, "English")
        random_delay(1, 2)
        english_option = driver.find_element(By.XPATH, "//div[@data-slang='en' and contains(@class, 'destination-lang-item')]")
        english_option.click()
        print("Changed destination language to English.")
        random_delay(2, 3)
    except Exception as e:
        print(f"Error changing languages: {e}")

# Read image files from a folder
def read_images_from_folder(folder_path="~/Desktop/collected_images", limit=2):
    folder_path = os.path.expanduser(folder_path)
    try:
        files = os.listdir(folder_path)
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        image_files.sort(key=lambda x: int(re.search(r'_(\d+)', x).group(1)))
        return [os.path.join(folder_path, image_file) for image_file in image_files[:limit]]
    except Exception as e:
        print(f"Error reading images from folder: {e}")
        return []

# Upload and process images
def upload_and_translate_images(image_files, driver):
    for image_file in image_files:
        try:
            upload_image(image_file)
            print(f"Uploaded image: {image_file}")
            random_delay(8, 12)

            # Wait for the "Translate" button to appear
            try:
                translate_button = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//div[contains(@style, 'cursor: pointer;') and .//span[text()='Translate']]"
                    ))
                )
                print("Translate button is visible.")
                input("Please click the 'Translate' button and press Enter here when done...")
            except Exception as e:
                print(f"Translate button not found for {image_file}: {e}")
                continue

            random_delay(15, 20)

        except Exception as e:
            print(f"Failed to process image {image_file}: {e}")
            continue

        random_delay(10, 15)

# Upload image helper
def upload_image(file_path):
    try:
        file_input = driver.find_element(By.ID, "file")
        file_input.send_keys(file_path)
        print(f"File image: {file_path}")
        random_delay(3, 5)
    except Exception as e:
        print(f"Error uploading file: {e}")

# Execution starts here
open_image_to_text_website()
handle_translator_cookies()
click_image_translator_link()
change_languages()
image_files = read_images_from_folder()
upload_and_translate_images(image_files, driver)
driver.quit()
