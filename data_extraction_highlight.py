from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time

# Define your login credentials
USERNAME = 'jianing046@gmail.com'
PASSWORD = 'Maria010315'

# Define the base URL and login path
BASE_URL = "https://edit.tosdr.org"
LOGIN_PATH = "/users/sign_in"

# Define paths for saving data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Selenium setup with Chrome
options = Options()
options.headless = True  # Set to False if you want to see the browser window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to check if content is available
def has_content(soup):
    no_content_message = soup.find(text="There are no points to display at this time!")
    return no_content_message is None

# Function to find highlights within the Terms of Service section
def find_terms_of_service_highlights(driver):
    # Locate the Terms of Service section by its header
    try:
        # Find the "Terms of Service" header
        terms_header = driver.find_element(By.XPATH, "//h3[contains(., 'Terms of Service')]")
        if terms_header:
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView();", terms_header)
            time.sleep(2)  # Wait for any lazy-loaded content
            
            # Get the HTML of the parent of the parent of the `h3` tag
            grandparent_element = terms_header.find_element(By.XPATH, "../..")
            if grandparent_element:
                grandparent_html = grandparent_element.get_attribute('outerHTML')
                # Parse the grandparent HTML to find highlights
                grandparent_soup = BeautifulSoup(grandparent_html, "html.parser")
                return grandparent_soup.find_all(class_="hypothesis-highlight")
    except Exception as e:
        print(f"Error while trying to find Terms of Service highlights: {e}")
    return []

# Function to log in
def login(driver, username, password):
    driver.get(BASE_URL + LOGIN_PATH)
    username_field = driver.find_element(By.ID, "user_email")
    password_field = driver.find_element(By.ID, "user_password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    driver.find_element(By.NAME, "commit").click()
    time.sleep(5)  # Wait for login to complete

# Login to the site
login(driver, USERNAME, PASSWORD)

# Navigate to the documents page
driver.get(BASE_URL + "/documents")
time.sleep(5)  # Wait for the page to load

# Extract the list of services and their document pages
soup = BeautifulSoup(driver.page_source, "html.parser")
services = soup.find_all("tr")

for service in services[1:]:  # Skip the header row
    try:
        columns = service.find_all("td")
        service_name = columns[0].text.strip()
        service_type = columns[1].text.strip()
        if "Terms of Service" in service_type:
            service_link = columns[0].find("a")["href"]
            
            # Click on the service name link
            driver.get(BASE_URL + service_link)
            time.sleep(5)  # Wait for the service page to load

            # Check if "View Documents" link is present
            view_documents_elements = driver.find_elements(By.LINK_TEXT, "View Documents")
            if view_documents_elements:
                # Click on "View Documents" to go to the annotations page
                view_documents_elements[0].click()
                time.sleep(5)  # Wait for the documents to load

                # Use the function to find highlights specifically within the Terms of Service section
                highlighted_texts = find_terms_of_service_highlights(driver)

                # Check if highlights were found before writing to file
                if highlighted_texts:
                    filename = f"{service_name}_{service_type}.html"
                    filepath = os.path.join(DATA_DIR, filename)
                    with open(filepath, "w") as f:
                        f.write("<html><body>\n")
                        for highlight in highlighted_texts:
                            f.write(str(highlight) + "\n")
                        f.write("</body></html>")
                    print(f"Saved {filename} to {DATA_DIR}")
                else:
                    print(f"No highlights found in Terms of Service for {service_name}. Skipping.")
            else:
                print(f"No 'View Documents' link found for {service_name}. Skipping.")
    except Exception as e:
        print(f"Error processing service: {service_name}, Error: {e}")

# Close the Selenium browser
driver.quit()
