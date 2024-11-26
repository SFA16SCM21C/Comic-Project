from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import os
import time
import re

# Initialize the WebDriver for Chrome
driver = webdriver.Chrome()

def open_website(url):
    driver.get(url)
    driver.maximize_window()
    print(f"WebDriver successfully opened the website: {url}")
    time.sleep(5)

def handle_cookies():
    try:
        # Click any "Accept" or "Accept all & visit site" button
        accept_button = driver.find_element(By.XPATH, "//button[.//div[contains(text(), 'Accept') or contains(text(), 'Aceptar')]]")
        accept_button.click()
        print("Clicked on 'Accept All'")
        time.sleep(20)
    except Exception:
        print("'Accept All' button not found. No action taken.")

def search_for_item(search_key):
    try:
        search_bar = driver.find_element(By.NAME, "word")
        search_bar.click()
        search_bar.send_keys(search_key)
        search_bar.send_keys(Keys.RETURN)
        print(f"Search for '{search_key}' initiated.")
        time.sleep(5)
    except Exception as e:
        print(f"Search bar not found: {e}")

def collect_item_links():
    links = []
    try:
        result_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'item-title')]")
        for element in result_elements[:10]:  # Only take the first 10 links
            href = element.get_attribute("href")
            if href:
                links.append(href)
        links.reverse()  # Reverse the list of links
        print(f"Collected and reversed {len(links)} links.")
    except Exception as e:
        print(f"Error collecting links: {e}")
    return links

def find_highest_chapter(links):
    highest_chapter_number = 0
    highest_chapter_link = ""
    
    for link in links:
        driver.get(link)
        print(f"Opened link: {link}")
        time.sleep(3)

        try:
            chapter_element = driver.find_element(By.XPATH, "//a[contains(@class, 'visited chapt')]")
            chapter_text = chapter_element.text
            match = re.search(r'Ch\s*(\d+)', chapter_text)
            if match:
                chapter_number = int(match.group(1))
                if chapter_number > highest_chapter_number:
                    highest_chapter_number = chapter_number
                    highest_chapter_link = link
                    print(f"New highest chapter found: Chapter {highest_chapter_number}")
        except Exception as e:
            print(f"No chapters found or error on page {link}: {e}")

    return highest_chapter_number, highest_chapter_link

def open_highest_chapter_link(highest_chapter_link):
    if highest_chapter_link:
        print(f"Opening the highest chapter link: {highest_chapter_link}")
        driver.get(highest_chapter_link)
        time.sleep(5)

def collect_chapter_links():
    chapter_links = []
    try:
        chapter_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'visited chapt')]")
        for chapter_element in chapter_elements[:10]:  # Only take the first 10 links
            chapter_href = chapter_element.get_attribute("href")
            chapter_links.append(chapter_href)
        print(f"Collected first 10 chapter links.")
    except Exception as e:
        print(f"Error collecting chapter links: {e}")
    return chapter_links

def open_chapter_links(chapter_links):
    global all_collected_images  # Use the global variable to store all images
    for chapter_link in chapter_links:
        driver.get(chapter_link)
        print(f"Opened chapter link: {chapter_link}")
        time.sleep(3)

        # Handle the agree button once, then collect images for each chapter
        handle_agree_button_once()
        collected_images = collect_images()
        all_collected_images.extend(collected_images)  # Append to the global list

    print(f"Finished collecting images. Total images collected: {len(all_collected_images)}")
    print(all_collected_images)

def handle_agree_button_once():
    global agree_button_clicked
    if not agree_button_clicked:
        try:
            agree_button = driver.find_element(By.XPATH, "//button[span[text()='AGREE']]")
            agree_button.click()
            agree_button_clicked = True
            print("Clicked on the 'AGREE' button.")
            time.sleep(1)
        except Exception:
            print("No 'AGREE' button found, or it was already clicked.")

def collect_images():
    image_sources = []
    try:
        image_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'item invisible')]//img[@class='page-img']")
        for img in image_elements:
            src = img.get_attribute("src")
            image_sources.append(src)
        print(f"Collected {len(image_sources)} image sources.")
    except Exception as e:
        print(f"Error collecting image sources: {e}")
    time.sleep(3)  # Delay after collecting images
    return image_sources

def download_images(image_urls, folder_path="~/Desktop/collected_images"):
    folder_path = os.path.expanduser(folder_path)
    os.makedirs(folder_path, exist_ok=True)  # Create the directory if it doesn't exist
    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            file_path = os.path.join(folder_path, f"image_{idx + 1}.png")
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded image {idx + 1} to {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image {idx + 1}: {e}")

def open_image_to_text_website():
    try:
        driver.get("https://www.imagetotext.info/image-translator")
        driver.maximize_window()
        print("Opened the Image to Text Translator website successfully.")
        time.sleep(3)
    except Exception as e:
        print(f"Failed to open the image translator website: {e}")

def handle_translator_cookies():
    try:
        # Locate the "Accept all & visit the site" div element by its ID
        accept_all_div = driver.find_element(By.ID, "accept-choices")
        
        # Scroll the element into view to make sure it's clickable
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", accept_all_div)
        time.sleep(1)  # Brief pause to allow scrolling to complete

        # Click the element using JavaScript to avoid overlay issues
        driver.execute_script("arguments[0].click();", accept_all_div)
        time.sleep(2)  # Wait for element
        print("Clicked on 'Accept all & visit the site' successfully.")
        time.sleep(3)  # Wait for any page transition after clicking
    except Exception as e:
        print(f"Could not find or click 'Accept all & visit the site': {e}")

def click_image_translator_link():
    try:
        # Locate the "Image Translator" link within the navigation links
        translator_link = driver.find_element(By.XPATH, "//div[@class='nav-links tools']//a[@href='https://www.imagetotext.info/image-translator']")
        
        # Scroll to the element and click via JavaScript to bypass potential overlay issues
        driver.execute_script("arguments[0].scrollIntoView(true);", translator_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", translator_link)
        print("Clicked on the 'Image Translator' link successfully.")
        time.sleep(3)
    except Exception as e:
        print(f"Failed to click on 'Image Translator' link: {e}")
        
def change_languages():
    try:
        # Change source language to Indonesian
        source_lang_div = driver.find_element(By.CLASS_NAME, "js-toggle-source-lang")
        source_lang_div.click()  # Open the dropdown
        time.sleep(1)  # Wait for dropdown to open

        # Find the search field within the modal and type "Indonesian"
        search_field = driver.find_element(By.ID, "js-search-slang")
        search_field.send_keys("Indonesian")
        time.sleep(1)  # Wait for results to filter

        # Select the Indonesian option by `data-slang="id"`
        indonesian_option = driver.find_element(By.XPATH, "//div[@data-slang='id' and contains(@class, 'source-lang-item')]")
        indonesian_option.click()
        print("Changed source language to Indonesian.")
        time.sleep(2)  # Wait for the selection to register

        # Change destination language to English
        dest_lang_div = driver.find_element(By.CLASS_NAME, "js-toggle-dest-lang")
        dest_lang_div.click()  # Open the dropdown
        time.sleep(1)  # Wait for dropdown to open

        # Find the search field for destination language
        search_field_dest = driver.find_element(By.ID, "js-search-dlang")
        search_field_dest.send_keys("English")
        time.sleep(1)  # Wait for results to filter

        # Select the English option by `data-slang="en"`
        english_option = driver.find_element(By.XPATH, "//div[@data-slang='en' and contains(@class, 'destination-lang-item')]")
        english_option.click()
        print("Changed destination language to English.")
        time.sleep(2)  # Wait for the selection to register

    except Exception as e:
        print(f"Error changing languages: {e}")

def read_images_from_folder(folder_path="~/Desktop/collected_images", limit=2):
    folder_path = os.path.expanduser(folder_path)
    try:
        # List all files in the directory
        files = os.listdir(folder_path)
        
        # Filter out only the image files
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        # Sort the image files numerically based on the number in the filename
        image_files.sort(key=lambda x: int(re.search(r'_(\d+)', x).group(1)))

        # Limit to the first 'limit' files
        limited_image_files = image_files[:limit]

        # Return the full paths to the sorted images
        return [os.path.join(folder_path, image_file) for image_file in limited_image_files]
    except Exception as e:
        print(f"Error reading images from folder: {e}")
        return []

def upload_image(file_path):
    try:
        # Locate the file input element (it may be hidden, so we access it directly)
        file_input = driver.find_element(By.ID, "file")
        
        # Send the file path to the input element
        file_input.send_keys(file_path)
        print(f"File image: {file_path}")
        time.sleep(3)  # Wait for the upload to process
    except Exception as e:
        print(f"Error uploading file: {e}")


def upload_and_translate_images(image_files, driver):
    for image_file in image_files:
        try:
            # Upload the image
            upload_image(image_file)
            print(f"Uploaded image: {image_file}")
            time.sleep(15)  # Wait for the image upload to complete
            
            # Check for CAPTCHA (this is a simple approach)
            captcha_element = driver.find_elements(By.CLASS_NAME, "captcha_class_name")

            if captcha_element:
                print("Please solve the CAPTCHA manually.")
                input("Press Enter after solving the CAPTCHA...")

            # Wait for the translated image to be updated (by waiting for the img tag to appear)
            print("Waiting for translated image to appear...")
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#translatedImage[src]"))
            )
            print("Translated image found. Translation complete.")

        except Exception as e:
            print(f"Failed to process image {image_file}: {e}")
            continue  # Move to the next image if an error occurs

        time.sleep(15)  # Wait for translation to complete before processing the next image

# Main execution
agree_button_clicked = False  # Initialize to False at the start of the script
all_collected_images = []  # Global list to store all image sources

# Open the main site, handle cookies, search and collect data
# open_website("https://battwo.com/")
# handle_cookies()
# search_key = "the remarried empress"
# search_for_item(search_key)

# Collect item links and find the highest chapter
# item_links = collect_item_links()
# highest_chapter_number, highest_chapter_link = find_highest_chapter(item_links)

# Open the highest chapter and collect chapter links
# open_highest_chapter_link(highest_chapter_link)
# chapter_links = collect_chapter_links()

# Open the first 10 chapter links in reverse order and collect images from each
# open_chapter_links(chapter_links)

# Download all collected images to a folder on the desktop
# download_images(all_collected_images)

# Open the image-to-text website after all images are collected
open_image_to_text_website()

# Handle cookies on the translator site
handle_translator_cookies()

# Click on the Image Translator link
click_image_translator_link()

# Change the languages
change_languages()

# Read images from the collected_images folder
image_files = read_images_from_folder()

# Translate the images
upload_and_translate_images(image_files, driver)

# Close the browser after processing all links
driver.quit()
