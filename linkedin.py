from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# LinkedIn credentials
USERNAME = "chauhansaloni54@gmail.com"
PASSWORD = "saloni123"

def initialize_driver():
    """
    Initialize the Selenium WebDriver with options.
    """
    options = Options()
    options.add_argument("--start-maximized")  # Open browser in maximized mode
    options.add_argument("--disable-notifications")  # Disable browser notifications
    options.add_argument("--incognito")  # Use incognito mode for privacy
    service = Service("path/to/chromedriver")  # Replace with the path to your ChromeDriver
    return webdriver.Chrome(service=service, options=options)

def login_to_linkedin(driver, username, password):
    """
    Log in to LinkedIn using provided credentials.
    """
    driver.get("https://www.linkedin.com/login")  # Open LinkedIn login page

    try:
        # Wait until the username field is available
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        # Fill in username and password
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)

        # Click the login button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait to ensure login is successful
        time.sleep(5)

        # Check if login was successful by looking for the profile icon
        if driver.current_url != "https://www.linkedin.com/feed/":
            raise Exception("Login failed! Please check your credentials.")

        print("Login successful!")

    except Exception as e:
        print(f"An error occurred during login: {e}")

def main():
    driver = initialize_driver()
    try:
        login_to_linkedin(driver, USERNAME, PASSWORD)
    finally:
        # Close the browser after completing the task
        driver.quit()

if __name__ == "__main__":
    main()
