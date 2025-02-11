import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

# LinkedIn credentials
USERNAME = "chauhansaloni54@gmail.com"  # Replace with your email
PASSWORD = "saloni123"  # Replace with your password
JOB_URL = "https://www.linkedin.com/jobs/search/?currentJobId=4123134087&distance=25&f_TPR=r2592000&geoId=107025191&keywords=senior%20software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"

def random_sleep(min_time=2, max_time=5):
    """Pause execution for a random duration between min_time and max_time seconds."""
    sleep_time = random.uniform(min_time, max_time)
    time.sleep(sleep_time)

def type_like_human(element, text, min_delay=0.1, max_delay=0.3):
    """Simulate human typing by sending keys one by one with random delay."""
    element.clear()  # Ensure the field is empty before typing
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))  # Random delay between keystrokes

def initialize_driver():
    """Initialize and return the Selenium WebDriver with options."""
    try:
        options = Options()
        options.add_argument("--start-maximized")  # Open browser in maximized mode
        options.add_argument("--disable-notifications")  # Disable browser notifications
        options.add_argument("--incognito")  # Open in incognito mode

        # Automatically install and manage ChromeDriver
        service = Service(ChromeDriverManager().install())  
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        return None  # Return None if initialization fails

def login_to_linkedin(driver, username, password):
    """Log in to LinkedIn using provided credentials."""
    try:
        driver.get("https://www.linkedin.com/login")
        random_sleep(3, 6)  # Wait after opening login page

        # Wait until the username field is available
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        random_sleep(2, 4)  # Mimic human reading time

        # Enter username (simulating human typing)
        username_field = driver.find_element(By.ID, "username")
        type_like_human(username_field, username)

        random_sleep(1, 3)  

        # Enter password (simulating human typing)
        password_field = driver.find_element(By.ID, "password")
        type_like_human(password_field, password)

        random_sleep(1, 3)  

        # Click the login button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        random_sleep(4, 7)  # Wait for login to process

        # Wait for the homepage to load
        WebDriverWait(driver, 10).until(
            EC.url_contains("feed")
        )

        print("Login successful!")
    except Exception as e:
        print(f"Error during login: {e}")
        
def navigate_to_job_page(driver):
    """Navigate to the job search URL."""
    try:
        driver.get(JOB_URL)
        print("Navigated to job search page.")
        random_sleep(10, 15)  # Simulate loading time
    except Exception as e:
        print(f"Error navigating to job page: {e}")

def wait_for_user_scroll(driver, timeout=30):
    """Wait for the user to manually scroll down before extracting job listings."""
    print("Waiting for user to scroll...")

    last_scroll_position = driver.execute_script("return window.scrollY;")
    start_time = time.time()

    while (time.time() - start_time) < timeout:
        time.sleep(2)  # Check every 2 seconds
        new_scroll_position = driver.execute_script("return window.scrollY;")

        if new_scroll_position != last_scroll_position:
            print("User is scrolling...")
            start_time = time.time()  # Reset timer if scrolling continues
        else:
            print("User stopped scrolling. Extracting job listings...")
            return  # Proceed to extraction

        last_scroll_position = new_scroll_position

def extract_job_links(driver):
    """Extract all job post links and their labels from the job search page."""
    try:
        job_links = []
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.job-card-container__link"))
        )
        job_elements = driver.find_elements(By.CSS_SELECTOR, "a.job-card-container__link")
        
        print("Extracted job links and titles:")
        
        for job in job_elements:
            job_href = job.get_attribute("href")
            job_label = job.get_attribute("aria-label")
            if job_href:
                print(f"{job_label} --------- {job_href}")
                job_links.append(job_href)
    except Exception as e:
        print(f"Error extracting job links: {e}")

def main():
    driver = initialize_driver()
    if driver:
        try:
            login_to_linkedin(driver, USERNAME, PASSWORD)
            navigate_to_job_page(driver)
            wait_for_user_scroll(driver)
            extract_job_links(driver)
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            try:
                driver.quit()  # Close the browser safely
                print("WebDriver closed.")
            except WebDriverException as e:
                print(f"Error while closing WebDriver: {e}")
            driver = None  # Ensure driver is set to None after quitting
    else:
        print("WebDriver could not be initialized. Exiting.")

if __name__ == "__main__":
    main()
